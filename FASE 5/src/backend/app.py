"""
CardioIA - Fase 5
Backend Flask do Assistente Cardiologico Conversacional.

Arquitetura (Cap10, secao 2.1 e 2.4 do material didatico):

    navegador (templates/index.html)
        |  POST /api/chat  {"message": "..."}
        v
    Flask (este arquivo)
        |-- ClienteWatson  -> IBM watsonx Assistant  (NLU: intencao + entidades)
        |     ou
        |-- MotorLocal     -> skill exportada, interpretada localmente
        |
        `-- triagem.py     -> regra de dominio sobre o valor extraido

Rotas:
    GET  /             interface de chat
    POST /api/iniciar  abre a conversa e devolve a saudacao
    POST /api/chat     envia mensagem e devolve a resposta
    POST /api/reset    encerra a conversa atual
    GET  /api/health   estado do servico e motor em uso

Execucao:
    pip install -r requirements.txt
    python app.py
    abrir http://127.0.0.1:5000
"""

import logging
import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, session

import triagem
from nlu_local import MotorLocal
from watson_client import (
    ClienteWatson,
    WatsonIndisponivel,
    WatsonNaoConfigurado,
)

BASE_DIR = Path(__file__).resolve().parent
SKILL_PATH = BASE_DIR.parent.parent / "config" / "watson" / "skill-cardioia-dialog.json"

load_dotenv(BASE_DIR / ".env")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("cardioia")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "cardioia-dev")

# ---------------------------------------------------------------------------
# Selecao do motor de NLU
# ---------------------------------------------------------------------------
# Com credenciais validas, usa o Watson Assistant (requisito da atividade).
# Sem credenciais, cai no motor local para que a aplicacao continue
# demonstravel por qualquer pessoa que clone o repositorio.

cliente_watson = None
motor_local = None
MODO = "local"

try:
    cliente_watson = ClienteWatson(
        api_key=os.getenv("WATSON_API_KEY"),
        url=os.getenv("WATSON_URL"),
        assistant_id=os.getenv("WATSON_ASSISTANT_ID"),
        versao=os.getenv("WATSON_VERSION", "2021-06-14"),
    )
    MODO = "watson"
    logger.info("Motor de NLU: IBM watsonx Assistant")
except WatsonNaoConfigurado as erro:
    logger.warning("Watson não configurado (%s). Iniciando em MODO LOCAL.", erro)

if MODO == "local":
    motor_local = MotorLocal(SKILL_PATH)
    logger.info("Motor de NLU: local, a partir de %s", SKILL_PATH.name)

# Sessoes ativas.
#   modo watson: id_conversa -> session_id do Watson
#   modo local:  id_conversa -> dicionario de contexto
# Estado em memoria: aceitavel para prototipo de uma instancia. Persistencia
# (Cap02) esta fora do escopo desta entrega - ver "Trabalhos futuros" no README.
CONVERSAS = {}

MENSAGEM_INDISPONIVEL = (
    "Não consegui falar com o serviço do assistente agora. Isso costuma ser "
    "instabilidade de conexão ou credencial expirada. Tente novamente em alguns "
    "instantes. Se você estiver passando mal neste momento, não aguarde: procure "
    "atendimento médico ou ligue 192."
)


def _id_conversa():
    """Identifica a conversa pelo cookie de sessao do Flask."""
    if "id_conversa" not in session:
        session["id_conversa"] = str(uuid.uuid4())
    return session["id_conversa"]


def _enriquecer(resposta, mensagem_usuario):
    """Aplica as regras de dominio sobre o que o NLU extraiu.

    Hoje: quando a entidade de pressao arterial e reconhecida, acrescenta a
    classificacao por faixa calculada em triagem.py. O Watson reconhece o
    formato; a regra clinica fica aqui, testavel e isolada.
    """
    tem_pressao = any(
        e.get("entidade") == "pressao_arterial" for e in resposta.get("entidades", [])
    )
    if not tem_pressao:
        return resposta

    analise = triagem.classificar_pressao(mensagem_usuario)
    if not analise:
        return resposta

    resposta["texto"] = f"{resposta['texto']}\n\n{analise['texto']}".strip()
    resposta["analise_pressao"] = {
        "valor": analise["valor"],
        "classificacao": analise["classificacao"],
    }
    if analise["urgencia"]:
        resposta["urgencia"] = True
    return resposta


@app.route("/")
def index():
    return render_template("index.html", modo=MODO)


@app.route("/api/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "modo": MODO,
            "skill": SKILL_PATH.name,
            "conversas_ativas": len(CONVERSAS),
        }
    )


@app.route("/api/iniciar", methods=["POST"])
def iniciar():
    """Abre a conversa e devolve a saudacao do no de boas-vindas."""
    id_conversa = _id_conversa()

    if MODO == "watson":
        try:
            session_id = cliente_watson.criar_sessao()
            CONVERSAS[id_conversa] = session_id
            # Entrada vazia dispara a condicao 'welcome' da arvore de dialogo.
            resposta, session_id = cliente_watson.enviar_mensagem(session_id, "")
            CONVERSAS[id_conversa] = session_id
        except WatsonIndisponivel as erro:
            logger.error("Falha ao iniciar conversa: %s", erro)
            return (
                jsonify({"texto": MENSAGEM_INDISPONIVEL, "origem": "erro", "erro": True}),
                503,
            )
    else:
        CONVERSAS[id_conversa] = {"falhas": 0, "urgencia": False}
        resposta = motor_local.saudacao()

    resposta["origem"] = MODO
    return jsonify(resposta)


@app.route("/api/chat", methods=["POST"])
def chat():
    """Recebe a mensagem do paciente e devolve a resposta do assistente."""
    dados = request.get_json(silent=True) or {}
    mensagem = (dados.get("message") or "").strip()

    # Tratamento de excecao no backend (camada 3 do plano de excecoes).
    if not mensagem:
        return (
            jsonify(
                {
                    "texto": "Não recebi nenhuma mensagem. Pode escrever o que você está sentindo ou o que precisa?",
                    "origem": MODO,
                    "erro": True,
                }
            ),
            400,
        )

    if len(mensagem) > 500:
        return (
            jsonify(
                {
                    "texto": "Sua mensagem é muito longa para eu processar. Pode resumir em poucas frases?",
                    "origem": MODO,
                    "erro": True,
                }
            ),
            400,
        )

    id_conversa = _id_conversa()

    if MODO == "watson":
        session_id = CONVERSAS.get(id_conversa)
        try:
            if not session_id:
                session_id = cliente_watson.criar_sessao()
            resposta, session_id = cliente_watson.enviar_mensagem(session_id, mensagem)
            CONVERSAS[id_conversa] = session_id
        except WatsonIndisponivel as erro:
            logger.error("Erro ao conversar com o Watson: %s", erro)
            return (
                jsonify({"texto": MENSAGEM_INDISPONIVEL, "origem": "erro", "erro": True}),
                503,
            )
    else:
        contexto = CONVERSAS.get(id_conversa) or {"falhas": 0}
        resposta, contexto = motor_local.responder(mensagem, contexto)
        CONVERSAS[id_conversa] = contexto

    resposta = _enriquecer(resposta, mensagem)
    resposta["origem"] = MODO

    # Rede de seguranca: o paciente nunca deve receber um balao vazio. Se por
    # qualquer motivo a resposta vier sem texto, devolvemos o tratamento de
    # excecao em vez de silencio.
    if not (resposta.get("texto") or "").strip():
        logger.warning("Resposta sem texto para a mensagem: %r", mensagem[:80])
        resposta["texto"] = (
            "Desculpe, não consegui formular uma resposta para isso. Pode "
            "reformular? Eu ajudo com sintomas cardiovasculares, pressão "
            "arterial, exames, hábitos de prevenção e agendamento."
        )

    logger.info(
        "conversa=%s intent=%s urgencia=%s entidades=%s",
        id_conversa[:8],
        resposta.get("intent"),
        resposta.get("urgencia"),
        [e.get("entidade") for e in resposta.get("entidades", [])],
    )

    return jsonify(resposta)


@app.route("/api/reset", methods=["POST"])
def reset():
    """Encerra a conversa atual."""
    id_conversa = _id_conversa()
    anterior = CONVERSAS.pop(id_conversa, None)
    if MODO == "watson" and isinstance(anterior, str):
        cliente_watson.encerrar_sessao(anterior)
    return jsonify({"status": "encerrada"})


if __name__ == "__main__":
    porta = int(os.getenv("PORT", "5000"))
    logger.info("CardioIA rodando em http://127.0.0.1:%s (modo: %s)", porta, MODO)
    app.run(host="127.0.0.1", port=porta, debug=True)
