"""
CardioIA - Fase 5
Cliente do IBM watsonx Assistant.

Base didatica: Cap10 - Arquitetura Cognitiva dos LLMs Modernos, secao 2.4
(Codigo-fonte 10), que demonstra o uso de AssistantV2 + IAMAuthenticator.

DIVERGENCIA DELIBERADA EM RELACAO AO MATERIAL:
    O exemplo do capitulo chama create_session() a cada mensagem recebida. Isso
    cria uma sessao nova por turno e, como consequencia, DESCARTA as variaveis de
    contexto ($sintoma_relatado, $duracao, $falhas...) entre uma mensagem e a
    seguinte. Com isso, o fluxo de coleta em varias etapas projetado na arvore de
    dialogo nao funcionaria: o assistente perguntaria a duracao e, no turno
    seguinte, ja teria esquecido o sintoma.

    Aqui a sessao e CRIADA UMA VEZ e REAPROVEITADA. Sessoes do Watson expiram por
    inatividade (padrao de 5 minutos no plano Lite); quando isso acontece a API
    responde 404 e nos recriamos a sessao de forma transparente.

Justificativa registrada no relatorio, secao de decisoes tecnicas.
"""

import logging

from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import AssistantV2

logger = logging.getLogger(__name__)


class WatsonNaoConfigurado(Exception):
    """Credenciais ausentes ou incompletas."""


class WatsonIndisponivel(Exception):
    """Falha de comunicacao com o servico (rede, credencial invalida, cota)."""


class ClienteWatson:
    """Encapsula a conversa com o watsonx Assistant.

    Uma instancia atende varias conversas: o session_id e mantido por
    conversa (ver mapa de sessoes em app.py).
    """

    def __init__(self, api_key, url, assistant_id, versao="2021-06-14"):
        if not (api_key and url and assistant_id):
            raise WatsonNaoConfigurado(
                "WATSON_API_KEY, WATSON_URL e WATSON_ASSISTANT_ID são obrigatórios."
            )

        self.assistant_id = assistant_id

        autenticador = IAMAuthenticator(api_key)
        self._assistant = AssistantV2(version=versao, authenticator=autenticador)
        self._assistant.set_service_url(url)

    def criar_sessao(self):
        """Abre uma sessao e devolve o session_id."""
        try:
            resposta = self._assistant.create_session(
                assistant_id=self.assistant_id
            ).get_result()
            return resposta["session_id"]
        except ApiException as erro:
            logger.error("Falha ao criar sessão no Watson: %s", erro)
            raise WatsonIndisponivel(str(erro)) from erro

    def encerrar_sessao(self, session_id):
        """Encerra a sessao. Falha silenciosa: encerrar e melhor esforco."""
        if not session_id:
            return
        try:
            self._assistant.delete_session(
                assistant_id=self.assistant_id, session_id=session_id
            )
        except ApiException as erro:
            logger.warning("Não foi possível encerrar a sessão %s: %s", session_id, erro)

    def enviar_mensagem(self, session_id, texto):
        """Envia a mensagem do paciente e devolve (resposta_normalizada, session_id).

        Se a sessao tiver expirado, cria outra e reenvia uma unica vez.
        """
        try:
            bruta = self._chamar(session_id, texto)
        except ApiException as erro:
            if erro.code == 404:
                # Sessao expirada por inatividade: recria e tenta de novo.
                logger.info("Sessão expirada. Criando nova sessão.")
                session_id = self.criar_sessao()
                try:
                    bruta = self._chamar(session_id, texto)
                except ApiException as erro_retry:
                    raise WatsonIndisponivel(str(erro_retry)) from erro_retry
            else:
                logger.error("Erro na API do Watson: %s", erro)
                raise WatsonIndisponivel(str(erro)) from erro

        return normalizar_resposta(bruta), session_id

    def _chamar(self, session_id, texto):
        # return_context e OBRIGATORIO aqui. Sem essa opcao, a resposta do
        # Watson v2 traz apenas "output" e "user_id" - o campo "context" volta
        # vazio, e as variaveis de contexto definidas na arvore de dialogo
        # ($urgencia, $sintoma_relatado, $falhas...) ficam invisiveis para o
        # backend. O dialogo continuaria funcionando, porque o Watson mantem o
        # estado na sessao, mas a interface perderia o destaque de urgencia.
        #
        # Constatado em teste real: sem return_context, uma mensagem de
        # emergencia retornava urgencia=False.
        return self._assistant.message(
            assistant_id=self.assistant_id,
            session_id=session_id,
            input={
                "message_type": "text",
                "text": texto,
                "options": {"return_context": True},
            },
        ).get_result()


def normalizar_resposta(bruta):
    """Reduz o JSON do Watson ao que a interface precisa.

    Le output.generic, output.intents e output.entities - exatamente os campos
    usados no Codigo-fonte 10 do Cap10 - e devolve um dicionario estavel. Esse
    formato e o MESMO produzido pelo modo local (nlu_local.py), o que permite
    trocar o motor de NLU sem alterar o app nem a interface.
    """
    saida = bruta.get("output", {}) if isinstance(bruta, dict) else {}

    textos = [
        item["text"]
        for item in saida.get("generic", [])
        if item.get("response_type") == "text" and item.get("text")
    ]
    # Respostas com multiplos valores aparecem em "values".
    for item in saida.get("generic", []):
        if item.get("response_type") == "text" and not item.get("text"):
            for valor in item.get("values", []):
                if valor.get("text"):
                    textos.append(valor["text"])

    # O Watson pode responder com tipos diferentes de texto - por exemplo
    # "suggestion", usado pela desambiguacao quando a confianca e baixa. Sem
    # tratar esses casos, a interface recebia texto vazio e exibia um balao em
    # branco. Constatado em teste com frases fora do dominio.
    if not textos:
        for item in saida.get("generic", []):
            if item.get("response_type") == "suggestion":
                opcoes = [
                    s.get("label")
                    for s in item.get("suggestions", [])
                    if s.get("label")
                ]
                pergunta = item.get("title") or "Nao tenho certeza do que voce precisa."
                if opcoes:
                    textos.append(pergunta + "\n\n- " + "\n- ".join(opcoes))
                else:
                    textos.append(pergunta)

    intents = saida.get("intents", [])
    entities = saida.get("entities", [])
    contexto = (bruta.get("context", {}) or {}).get("skills", {})

    variaveis = {}
    for skill in contexto.values():
        variaveis.update((skill.get("user_defined") or {}))

    return {
        "texto": "\n\n".join(textos).strip(),
        "intent": intents[0]["intent"] if intents else None,
        "confianca": round(intents[0]["confidence"], 3) if intents else None,
        "entidades": [
            {"entidade": e.get("entity"), "valor": e.get("value")} for e in entities
        ],
        "contexto": variaveis,
        "urgencia": bool(variaveis.get("urgencia")),
    }
