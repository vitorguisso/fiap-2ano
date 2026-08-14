"""
CardioIA - Fase 5
Regras de dominio aplicadas sobre as informacoes extraidas pelo assistente.

DIVISAO DE RESPONSABILIDADE (decisao arquitetural):
    - o Watson Assistant faz o NLU: identifica a INTENCAO e EXTRAI a entidade;
    - este modulo aplica a REGRA DE NEGOCIO sobre o valor extraido.

Motivo: a entidade @pressao_arterial e uma expressao regular. Regex reconhece o
formato "150/100", mas nao sabe se o valor e plausivel nem em que faixa ele cai.
Colocar faixa clinica dentro da arvore de dialogo exigiria um no por faixa e
tornaria a skill fragil. Aqui a regra fica testavel e isolada.

AVISO: as faixas abaixo sao REFERENCIA INFORMATIVA para adultos, nao diagnostico.
Uma medida isolada nao caracteriza hipertensao.
"""

import re

# Faixas de referencia para adultos (mmHg).
# Fonte: Diretrizes Brasileiras de Hipertensao Arterial - Sociedade Brasileira de
# Cardiologia. Usadas aqui apenas como informacao ao paciente.
FAIXAS = [
    # (rotulo, sistolica_max, diastolica_max)
    ("ótima", 119, 79),
    ("normal", 129, 84),
    ("pré-hipertensão", 139, 89),
]

# Limites de plausibilidade. Fora disso, a medida provavelmente foi digitada errada.
SISTOLICA_MIN, SISTOLICA_MAX = 60, 300
DIASTOLICA_MIN, DIASTOLICA_MAX = 30, 200

# Limiar a partir do qual a orientacao deixa de ser informativa e passa a ser
# de procura de atendimento.
CRISE_SISTOLICA = 180
CRISE_DIASTOLICA = 110

PADRAO_PRESSAO = re.compile(r"(\d{2,3})\s*(?:x|X|/|por)\s*(\d{1,3})")


def extrair_pressao(texto):
    """Extrai o par (sistolica, diastolica) de um texto livre.

    Normaliza a escala coloquial: o paciente costuma dizer "12 por 8" querendo
    dizer 120/80 mmHg. Quando os dois valores sao pequenos, multiplicamos por 10.

    Retorna None quando nao encontra nada com o formato esperado.
    """
    achado = PADRAO_PRESSAO.search(texto or "")
    if not achado:
        return None

    sistolica = int(achado.group(1))
    diastolica = int(achado.group(2))

    # "12 por 8" -> 120/80 ; "15x10" -> 150/100
    if sistolica <= 30 and diastolica <= 30:
        sistolica *= 10
        diastolica *= 10

    return sistolica, diastolica


def classificar_pressao(texto):
    """Devolve uma orientacao textual sobre a pressao informada.

    Retorna None quando nao ha medida reconhecivel no texto, para que o backend
    simplesmente nao acrescente nada a resposta do assistente.
    """
    medida = extrair_pressao(texto)
    if medida is None:
        return None

    sistolica, diastolica = medida

    plausivel = (
        SISTOLICA_MIN <= sistolica <= SISTOLICA_MAX
        and DIASTOLICA_MIN <= diastolica <= DIASTOLICA_MAX
        and sistolica > diastolica
    )
    if not plausivel:
        return {
            "valor": f"{sistolica}/{diastolica} mmHg",
            "classificacao": "valor implausível",
            "urgencia": False,
            "texto": (
                f"Observação: o valor {sistolica}/{diastolica} mmHg está fora da faixa "
                "plausível para pressão arterial em adultos, ou foi digitado de forma "
                "invertida. Pode conferir a medida?"
            ),
        }

    if sistolica >= CRISE_SISTOLICA or diastolica >= CRISE_DIASTOLICA:
        return {
            "valor": f"{sistolica}/{diastolica} mmHg",
            "classificacao": "muito elevada",
            "urgencia": True,
            "texto": (
                f"Observação sobre a medida {sistolica}/{diastolica} mmHg: esse valor é "
                "considerado muito elevado. Procure avaliação médica hoje. Se houver dor "
                "no peito, falta de ar, alteração na visão, fala ou força, procure "
                "atendimento de emergência imediatamente (192)."
            ),
        }

    classificacao = "hipertensão (a confirmar)"
    for rotulo, sis_max, dia_max in FAIXAS:
        if sistolica <= sis_max and diastolica <= dia_max:
            classificacao = rotulo
            break

    if classificacao == "hipertensão (a confirmar)":
        complemento = (
            "Valores repetidos nessa faixa precisam ser avaliados por um médico. "
            "Registre as medidas ao longo de alguns dias e leve na consulta."
        )
    elif classificacao == "pré-hipertensão":
        complemento = (
            "Vale acompanhar com medidas regulares e cuidar dos hábitos "
            "(sal, peso, atividade física)."
        )
    else:
        complemento = "Continue acompanhando periodicamente."

    return {
        "valor": f"{sistolica}/{diastolica} mmHg",
        "classificacao": classificacao,
        "urgencia": False,
        "texto": (
            f"Observação sobre a medida {sistolica}/{diastolica} mmHg: pelas faixas de "
            f"referência para adultos, ela se enquadra como {classificacao}. "
            f"{complemento} Uma medida isolada não define diagnóstico."
        ),
    }
