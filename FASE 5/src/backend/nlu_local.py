"""
CardioIA - Fase 5
Motor de NLU local - modo de demonstracao.

POR QUE ISSO EXISTE
    O requisito da atividade e integrar o assistente ao Watson Assistant, e essa
    e a integracao principal do projeto (ver watson_client.py). O problema: as
    credenciais da IBM Cloud sao pessoais e nao podem ser publicadas no GitHub
    (secao 25 do CLAUDE.md). Quem clonar o repositorio nao tem WATSON_API_KEY e,
    sem um plano B, veria apenas uma tela de erro.

    Este modulo le O MESMO arquivo de skill exportado (config/watson/) e resolve
    intencao, entidades e no de resposta localmente, devolvendo o MESMO contrato
    de dados que watson_client.normalizar_resposta(). A interface nao sabe qual
    motor esta respondendo.

    Base didatica: o proprio Cap10 apresenta NLU por regras e regex (ELIZA,
    secao 1.3) como abordagem legitima de sistema conversacional.

LIMITACOES REAIS (nao e um substituto do Watson)
    1. A classificacao de intencao usa similaridade de tokens com os exemplos de
       treino, nao aprendizado de maquina. Generaliza menos que o Watson.
    2. Avalia apenas nos de primeiro nivel da arvore: o dialogo de coleta em
       varias etapas (duracao -> intensidade) NAO acontece no modo local.
    3. Nao avalia toda a gramatica de condicoes do Watson, apenas o subconjunto
       usado nesta skill.

    Essas limitacoes estao registradas no README e no relatorio.
"""

import json
import math
import re
import unicodedata
from pathlib import Path

# Similaridade minima para aceitar uma intencao. Abaixo disso, cai no
# tratamento de excecao (anything_else).
#
# O valor 0.42 nao foi arbitrado: veio de uma varredura sobre 35 frases rotuladas
# (29 dentro do escopo, 6 fora), testando os limiares 0.34, 0.38, 0.42, 0.46 e
# 0.50. Em 0.34 entrava um falso positivo ("qual a previsao do tempo" casava com
# duvida_exame, score 0.375); em 0.50 comecava a rejeitar frase valida ("minha
# pressao deu 150/100", score 0.50). A faixa 0.38-0.46 acertou 34/35, e 0.42 e o
# ponto mais distante das duas bordas de erro.
LIMIAR_INTENCAO = 0.42

EXPRESSAO_SPEL = re.compile(r"<\?(.*?)\?>")


def normalizar(texto):
    """Minusculas, sem acento e sem pontuacao - para comparacao de texto."""
    texto = (texto or "").lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9\s/]", " ", texto)


# Palavras funcionais do portugues, removidas antes de comparar frases.
# "nao" NAO entra nesta lista de proposito: em relato clinico ela inverte o
# sentido ("nao consigo respirar") e precisa contar na comparacao.
PALAVRAS_VAZIAS = {
    "de", "do", "da", "dos", "das", "no", "na", "nos", "nas", "em", "um", "uma",
    "uns", "umas", "os", "as", "ao", "aos", "que", "com", "por", "para", "pra",
    "se", "sao", "ser", "esta", "este", "essa", "esse", "isso", "meu", "minha",
    "seu", "sua", "ele", "ela", "eu", "voce", "me", "te", "mais", "mas", "ja",
    "muito", "tem", "foi", "sobre", "como", "qual", "quais",
}


def tokenizar(texto):
    """Divide em tokens comparaveis: descarta palavras de 1 letra e vazias.

    O limite minimo e 2 caracteres, e nao 3, porque saudacoes reais do paciente
    sao curtas ("oi") - com limite 3 elas ficavam sem token nenhum e caiam no
    tratamento de excecao.
    """
    return [
        t
        for t in normalizar(texto).split()
        if len(t) >= 2 and t not in PALAVRAS_VAZIAS
    ]


class MotorLocal:
    """Interpreta a skill exportada do Watson sem chamar a nuvem."""

    def __init__(self, caminho_skill):
        self.caminho_skill = Path(caminho_skill)
        with open(self.caminho_skill, encoding="utf-8") as arquivo:
            self.skill = json.load(arquivo)

        self._preparar_intencoes()
        self._preparar_entidades()
        self._preparar_nos()

    # ------------------------------------------------------------------ setup

    def _preparar_intencoes(self):
        """Indexa os exemplos de treino e calcula o peso IDF de cada termo.

        POR QUE PONDERAR: sem peso, todas as palavras valem igual e termos
        genericos dominam a comparacao. Na pratica isso produziu erro real -
        "sinto palpitacao forte" era classificada como emergencia porque
        compartilhava "sinto" e "forte" com um exemplo de emergencia, enquanto a
        palavra que de fato importa ("palpitacao") tinha o mesmo peso.

        A solucao e o IDF (inverse document frequency): termos que aparecem em
        muitos exemplos pesam pouco, termos raros pesam muito. Mesmo principio
        do TF-IDF classico, aplicado a um corpus pequeno.
        """
        self.intencoes = {}
        frequencia = {}
        total_exemplos = 0

        for intencao in self.skill.get("intents", []):
            exemplos = []
            for exemplo in intencao.get("examples", []):
                tokens = set(tokenizar(exemplo["text"]))
                if not tokens:
                    continue
                exemplos.append((normalizar(exemplo["text"]).strip(), tokens))
                total_exemplos += 1
                for token in tokens:
                    frequencia[token] = frequencia.get(token, 0) + 1
            self.intencoes[intencao["intent"]] = exemplos

        self.peso = {}
        for token, ocorrencias in frequencia.items():
            self.peso[token] = math.log(1 + total_exemplos / ocorrencias)
        # Peso atribuido a termo nunca visto no treino: alto, porque termo raro
        # e informativo - mas so entra no calculo do tamanho da entrada.
        self.peso_desconhecido = math.log(1 + total_exemplos)

    def _pesar(self, tokens):
        """Soma o peso IDF de um conjunto de tokens."""
        return sum(self.peso.get(t, self.peso_desconhecido) for t in tokens)

    def _preparar_entidades(self):
        self.sinonimos = {}   # entidade -> [(valor, sinonimo_normalizado)]
        self.padroes = {}     # entidade -> [(valor, regex)]
        for entidade in self.skill.get("entities", []):
            nome = entidade["entity"]
            for valor in entidade.get("values", []):
                if valor.get("type") == "patterns":
                    for padrao in valor.get("patterns", []):
                        self.padroes.setdefault(nome, []).append(
                            (valor["value"], re.compile(padrao))
                        )
                else:
                    termos = [valor["value"].replace("_", " ")]
                    termos += valor.get("synonyms", [])
                    for termo in termos:
                        self.sinonimos.setdefault(nome, []).append(
                            (valor["value"], normalizar(termo).strip())
                        )
            # sinonimos mais longos primeiro: "dor no peito" antes de "peito"
            if nome in self.sinonimos:
                self.sinonimos[nome].sort(key=lambda par: len(par[1]), reverse=True)

    def _preparar_nos(self):
        """Ordena os nos de primeiro nivel seguindo a cadeia previous_sibling."""
        todos = {no["dialog_node"]: no for no in self.skill.get("dialog_nodes", [])}
        raizes = [no for no in todos.values() if no.get("parent") is None]

        por_anterior = {no.get("previous_sibling"): no for no in raizes}
        ordenados = []
        atual = por_anterior.get(None)
        while atual is not None:
            ordenados.append(atual)
            atual = por_anterior.get(atual["dialog_node"])

        # Rede de seguranca: se a cadeia estiver quebrada, nao perde nenhum no.
        if len(ordenados) != len(raizes):
            vistos = {no["dialog_node"] for no in ordenados}
            ordenados += [no for no in raizes if no["dialog_node"] not in vistos]

        self.nos = ordenados
        self.nos_por_id = todos

        # Indice de filhos, tambem na ordem de irmaos, para o dialogo de varias
        # etapas (perguntar duracao -> perguntar intensidade -> resumir).
        self.filhos = {}
        for pai_id in {no.get("parent") for no in todos.values() if no.get("parent")}:
            irmaos = [no for no in todos.values() if no.get("parent") == pai_id]
            por_anterior = {no.get("previous_sibling"): no for no in irmaos}
            sequencia, atual = [], por_anterior.get(None)
            while atual is not None:
                sequencia.append(atual)
                atual = por_anterior.get(atual["dialog_node"])
            if len(sequencia) != len(irmaos):
                vistos = {no["dialog_node"] for no in sequencia}
                sequencia += [no for no in irmaos if no["dialog_node"] not in vistos]
            self.filhos[pai_id] = sequencia

    # ----------------------------------------------------------------- publico

    def saudacao(self):
        """Resposta do no de boas-vindas (condicao 'welcome')."""
        for no in self.nos:
            if no.get("conditions") == "welcome":
                return self._montar_resposta(no, "", None, [], {})
        return {
            "texto": "Olá! Como posso ajudar?",
            "intent": None,
            "confianca": None,
            "entidades": [],
            "contexto": {},
            "urgencia": False,
        }

    def responder(self, texto, contexto=None):
        """Processa a mensagem e devolve (resposta, contexto_atualizado)."""
        contexto = dict(contexto or {})
        contexto.setdefault("falhas", 0)

        intencao, confianca = self._classificar(texto)
        entidades = self._extrair_entidades(texto)

        # BACKSTOP POR ENTIDADE: se a similaridade nao alcancou o limiar mas o
        # paciente nomeou um sintoma cardiologico reconhecido, a mensagem e
        # tratada como relato de sintoma em vez de cair no "nao entendi".
        # Exemplo real que motivou a regra: "meu cansaco esta forte" nao casava
        # com nenhum exemplo de treino por dois termos, mas contem @sintoma.
        # No Watson esse papel e cumprido pelo classificador estatistico.
        if intencao is None and any(e["entidade"] == "sintoma" for e in entidades):
            intencao = "informar_sintoma"

        no = self._selecionar_no(intencao, entidades, contexto)

        # Aplica as atribuicoes de contexto do no escolhido e resolve saltos
        # (next_step jump_to / selector body) antes de montar a resposta.
        no = self._resolver_salto(no, texto, entidades, contexto)

        resposta = self._montar_resposta(no, texto, intencao, entidades, contexto)

        if confianca is not None:
            resposta["confianca"] = confianca

        for chave, valor in (no.get("context") or {}).items():
            contexto[chave] = self._resolver_valor(valor, texto, entidades)

        # Se o no tem filhos, a proxima mensagem do paciente e avaliada dentro
        # dele: e isso que sustenta o dialogo de varias etapas.
        contexto["_no_atual"] = (
            no["dialog_node"] if self.filhos.get(no["dialog_node"]) else None
        )

        resposta["contexto"] = dict(contexto)
        resposta["urgencia"] = bool(contexto.get("urgencia"))
        return resposta, contexto

    # ------------------------------------------------------------- internos

    def _classificar(self, texto):
        tokens = set(tokenizar(texto))
        normalizado = normalizar(texto).strip()
        if not tokens:
            return None, None

        peso_entrada = self._pesar(tokens)
        melhor_intencao, melhor_score = None, 0.0

        for intencao, exemplos in self.intencoes.items():
            for exemplo_texto, exemplo_tokens in exemplos:
                # Frase praticamente identica a um exemplo de treino: aceita direto.
                if exemplo_texto and exemplo_texto in normalizado:
                    if 0.95 > melhor_score:
                        melhor_intencao, melhor_score = intencao, 0.95
                    continue

                comuns = tokens & exemplo_tokens
                if not comuns:
                    continue

                # Media harmonica-like entre cobertura do exemplo e cobertura da
                # entrada, ambas ponderadas por IDF. Penaliza tanto exemplo longo
                # (casou pouco do exemplo) quanto entrada longa (casou pouco do
                # que o paciente escreveu).
                peso_comum = self._pesar(comuns)
                peso_exemplo = self._pesar(exemplo_tokens)
                if not peso_exemplo or not peso_entrada:
                    continue

                score = 0.5 * (peso_comum / peso_exemplo + peso_comum / peso_entrada)
                if score > melhor_score:
                    melhor_intencao, melhor_score = intencao, score

        if melhor_score < LIMIAR_INTENCAO:
            return None, round(melhor_score, 3)
        return melhor_intencao, round(melhor_score, 3)

    @staticmethod
    def _radical(palavra):
        """Monta um padrao que tolera variacao de flexao da palavra.

        A skill declara fuzzy_match: true nas entidades, recurso que o Watson
        resolve internamente. O motor local precisa emular isso.

        MOTIVO CONCRETO: no primeiro teste no navegador, a frase "minhas pernas
        estao inchando no fim do dia" NAO ativou @sintoma. O sinonimo cadastrado
        era "pernas inchadas" e o paciente escreveu "inchando" - comparacao
        literal falha em flexao verbal.

        Regra: palavras com 5 caracteres ou mais casam pelo radical (5 primeiras
        letras seguidas de qualquer sufixo); palavras curtas exigem correspondencia
        exata. O limite de 5 evita falso positivo em palavras curtas ambiguas -
        sem ele, "leve" casaria com "levei" e "levar".
        """
        if len(palavra) >= 5:
            return re.escape(palavra[:5]) + r"[a-z]*"
        return re.escape(palavra) + r"\b"

    def _casa_sinonimo(self, sinonimo, normalizado):
        """Verifica se o sinonimo ocorre no texto, tolerando flexao."""
        palavras = sinonimo.split()
        if not palavras:
            return False

        # 1) frase completa, na ordem (caso mais confiavel)
        padrao_frase = r"\b" + r"\s+".join(self._radical(p) for p in palavras)
        if re.search(padrao_frase, normalizado):
            return True

        # 2) sinonimo de varias palavras: aceita os termos dispersos na frase
        #    ("pernas inchadas" casa com "pernas estao inchando")
        if len(palavras) > 1:
            return all(
                re.search(r"\b" + self._radical(p), normalizado) for p in palavras
            )

        return False

    def _extrair_entidades(self, texto):
        normalizado = normalizar(texto)
        encontradas = []

        for entidade, pares in self.sinonimos.items():
            for valor, sinonimo in pares:
                if sinonimo and self._casa_sinonimo(sinonimo, normalizado):
                    encontradas.append({"entidade": entidade, "valor": valor})
                    break  # um valor por entidade, o mais especifico

        for entidade, pares in self.padroes.items():
            for valor, regex in pares:
                achado = regex.search(texto or "")
                if achado:
                    encontradas.append(
                        {
                            "entidade": entidade,
                            "valor": valor,
                            "literal": achado.group(0),
                        }
                    )
                    break

        return encontradas

    def _selecionar_no(self, intencao, entidades, contexto):
        """Escolhe o no que vai responder.

        Se a conversa esta dentro de um fluxo de coleta, os FILHOS do no atual
        sao avaliados primeiro - e assim que "ha quanto tempo?" consegue
        interpretar "uns tres dias" como resposta, e nao como assunto novo.

        EXCECAO DE SEGURANCA: emergencia sempre interrompe a coleta. Sem esta
        regra, um paciente que piorasse no meio do fluxo ("a dor esta
        insuportavel agora") teria a mensagem consumida pelo no de coleta, que
        casa com qualquer entrada, e receberia a pergunta seguinte do
        questionario em vez da orientacao de urgencia.
        """
        atual = contexto.get("_no_atual")
        if atual and intencao != "emergencia_cardiaca":
            for filho in self.filhos.get(atual, []):
                if self._avaliar(
                    filho.get("conditions") or "", intencao, entidades, contexto
                ):
                    return filho

        for no in self.nos:
            condicao = no.get("conditions") or ""
            if condicao == "welcome":
                continue
            if self._avaliar(condicao, intencao, entidades, contexto):
                return no
        # Ultimo recurso: o proprio no de falha.
        return self.nos[-1]

    def _resolver_salto(self, no, texto, entidades, contexto):
        """Segue next_step jump_to com selector 'body' (salto para a resposta).

        Usado pelos nos de captura: quando o paciente informa o sintoma so na
        segunda mensagem, a conversa salta para a resposta do no principal em vez
        de duplicar o texto em dois lugares da skill.
        """
        visitados = set()
        while True:
            passo = no.get("next_step") or {}
            if (
                passo.get("behavior") != "jump_to"
                or passo.get("selector") != "body"
                or no["dialog_node"] in visitados
            ):
                return no

            visitados.add(no["dialog_node"])
            # O contexto do no de origem precisa valer antes do salto.
            for chave, valor in (no.get("context") or {}).items():
                contexto[chave] = self._resolver_valor(valor, texto, entidades)

            destino = self.nos_por_id.get(passo.get("dialog_node"))
            if destino is None:
                return no
            no = destino

    def _avaliar(self, condicao, intencao, entidades, contexto):
        """Avalia o subconjunto de condicoes usado nesta skill.

        Suporta: 'true', 'anything_else', '#intent', '@entidade',
        '@entidade:valor' e '$variavel > numero', combinados por '&&'.
        """
        for termo in [t.strip() for t in condicao.split("&&") if t.strip()]:
            if termo == "true":
                continue
            if termo == "anything_else":
                if intencao is not None:
                    return False
                continue
            if termo.startswith("#"):
                if intencao != termo[1:]:
                    return False
                continue
            if termo.startswith("@"):
                alvo = termo[1:]
                if ":" in alvo:
                    nome, valor = alvo.split(":", 1)
                    if not any(
                        e["entidade"] == nome and e["valor"] == valor for e in entidades
                    ):
                        return False
                elif not any(e["entidade"] == alvo for e in entidades):
                    return False
                continue
            comparacao = re.match(r"\$(\w+)\s*(>|>=|==)\s*(\d+)", termo)
            if comparacao:
                variavel, operador, numero = comparacao.groups()
                atual = contexto.get(variavel) or 0
                numero = int(numero)
                if operador == ">" and not atual > numero:
                    return False
                if operador == ">=" and not atual >= numero:
                    return False
                if operador == "==" and not atual == numero:
                    return False
                continue
            return False  # condicao nao suportada: nao arrisca casar errado
        return True

    def _montar_resposta(self, no, texto, intencao, entidades, contexto):
        valores = []
        for item in (no.get("output") or {}).get("generic", []):
            if item.get("response_type") != "text":
                continue
            for valor in item.get("values", []):
                if valor.get("text"):
                    valores.append(valor["text"])

        # Contexto provisorio para resolver as expressoes do proprio no.
        provisorio = dict(contexto)
        for chave, valor in (no.get("context") or {}).items():
            provisorio[chave] = self._resolver_valor(valor, texto, entidades)

        resolvido = [
            self._resolver_expressoes(v, texto, provisorio, entidades) for v in valores
        ]

        return {
            "texto": "\n\n".join(resolvido).strip(),
            "intent": intencao,
            "confianca": None,
            "entidades": entidades,
            "contexto": provisorio,
            "urgencia": bool(provisorio.get("urgencia")),
            "no": no.get("title"),
        }

    def _resolver_valor(self, valor, texto, entidades):
        """Resolve o lado direito de uma atribuicao de contexto da skill."""
        if not isinstance(valor, str):
            return valor
        if valor.startswith("@"):
            return self._valor_entidade(valor[1:], entidades)
        return self._resolver_expressoes(valor, texto, {}, entidades)

    @staticmethod
    def _valor_entidade(referencia, entidades):
        """Resolve '@entidade' ou '@entidade.literal'.

        Sem sufixo, devolve o VALOR da entidade - que nesta skill e um rotulo
        legivel em portugues ("inchaço", "dor no peito"), porque esse texto vai
        direto para a resposta ao paciente.

        Com '.literal', devolve o trecho exato que o paciente digitou. E o que a
        entidade de regex precisa: o valor dela e apenas "medida", enquanto o
        literal e "150/100".
        """
        nome, _, sufixo = referencia.partition(".")
        for entidade in entidades or []:
            if entidade["entidade"] != nome:
                continue
            if sufixo == "literal":
                return entidade.get("literal") or entidade["valor"]
            return entidade["valor"]
        return None

    def _resolver_expressoes(self, texto_saida, entrada, contexto, entidades=None):
        """Substitui as expressoes <? ... ?> do Watson pelos valores disponiveis."""

        def trocar(achado):
            expressao = achado.group(1).strip()
            if expressao in ("input.text", "input.text()"):
                return entrada or ""
            if expressao.startswith("$"):
                valor = contexto.get(expressao[1:])
                if valor is None:
                    return "não informado"
                return str(valor)
            if expressao.startswith("@"):
                valor = self._valor_entidade(expressao[1:], entidades)
                return str(valor) if valor is not None else ""
            return ""

        return EXPRESSAO_SPEL.sub(trocar, texto_saida)
