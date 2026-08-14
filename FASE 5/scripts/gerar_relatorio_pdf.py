"""
CardioIA - Fase 5
Gera o PDF do relatorio a partir do arquivo Markdown.

Por que existe: o relatorio e um entregavel em PDF, mas manter o conteudo em
Markdown permite versionar, revisar e regerar o documento sem reescrever nada.
Quando os resultados dos testes no Watson forem obtidos, basta atualizar o .md e
rodar este script novamente.

Uso (a partir da raiz do projeto):
    pip install reportlab
    python scripts/gerar_relatorio_pdf.py

Suporta o subconjunto de Markdown usado no relatorio: titulos (#, ##),
paragrafos, negrito, italico, codigo inline, listas numeradas, citacao (>) e
regua horizontal (---).
"""

import re
import sys
from pathlib import Path

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "document" / "RELATORIO_FLUXO_CONVERSACIONAL_FASE5.md"
SAIDA = RAIZ / "document" / "RELATORIO_FLUXO_CONVERSACIONAL_FASE5.pdf"

VINHO = "#8D0E22"
CINZA = "#3C4650"


def montar_estilos():
    base = getSampleStyleSheet()
    return {
        "titulo": ParagraphStyle(
            "TituloDoc",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=19,
            textColor=VINHO,
            spaceAfter=8,
        ),
        "secao": ParagraphStyle(
            "Secao",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=13,
            textColor=VINHO,
            spaceBefore=9,
            spaceAfter=3,
        ),
        "corpo": ParagraphStyle(
            "Corpo",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.7,
            leading=11.6,
            alignment=TA_JUSTIFY,
            textColor=CINZA,
            spaceAfter=4,
        ),
        "identificacao": ParagraphStyle(
            "Identificacao",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.2,
            leading=11,
            textColor=CINZA,
            spaceAfter=1,
        ),
        "citacao": ParagraphStyle(
            "Citacao",
            parent=base["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=8.4,
            leading=11,
            leftIndent=10,
            borderPadding=3,
            textColor=VINHO,
            spaceBefore=3,
            spaceAfter=4,
        ),
        "rodape": ParagraphStyle(
            "Rodape",
            parent=base["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=7.6,
            leading=10,
            textColor="#6B7580",
            spaceBefore=5,
        ),
    }


def inline(texto):
    """Converte a marcacao inline do Markdown para as tags do ReportLab."""
    texto = texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    texto = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", texto)
    texto = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", texto)
    texto = re.sub(r"`(.+?)`", r'<font face="Courier" size="8">\1</font>', texto)
    return texto


def converter(linhas, estilos):
    elementos = []
    lista_pendente = []
    identificacao = True

    def descarregar_lista():
        if not lista_pendente:
            return
        elementos.append(
            ListFlowable(
                [
                    ListItem(Paragraph(item, estilos["corpo"]), leftIndent=14)
                    for item in lista_pendente
                ],
                bulletType="1",
                bulletFontSize=8.7,
                leftIndent=12,
            )
        )
        elementos.append(Spacer(1, 2))
        lista_pendente.clear()

    for linha in linhas:
        crua = linha.rstrip()
        texto = crua.strip()

        if not texto:
            continue

        if texto.startswith("# "):
            descarregar_lista()
            elementos.append(Paragraph(inline(texto[2:]), estilos["titulo"]))
            continue

        if texto.startswith("## "):
            descarregar_lista()
            identificacao = False
            elementos.append(Paragraph(inline(texto[3:]), estilos["secao"]))
            continue

        if texto.startswith("---"):
            descarregar_lista()
            elementos.append(Spacer(1, 3))
            elementos.append(
                HRFlowable(width="100%", thickness=0.6, color="#DFE4EA")
            )
            elementos.append(Spacer(1, 3))
            continue

        if texto.startswith("> "):
            descarregar_lista()
            elementos.append(Paragraph(inline(texto[2:]), estilos["citacao"]))
            continue

        numerada = re.match(r"^\d+\.\s+(.*)", texto)
        if numerada:
            lista_pendente.append(inline(numerada.group(1)))
            continue

        descarregar_lista()

        if texto.startswith("*") and texto.endswith("*") and not texto.startswith("**"):
            elementos.append(Paragraph(inline(texto), estilos["rodape"]))
            continue

        estilo = estilos["identificacao"] if identificacao else estilos["corpo"]
        elementos.append(Paragraph(inline(texto), estilo))

    descarregar_lista()
    return elementos


def numerar_pagina(canvas, documento):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor("#8A929B")
    canvas.drawRightString(
        A4[0] - 1.6 * cm, 1.1 * cm, f"Página {documento.page}"
    )
    canvas.drawString(1.6 * cm, 1.1 * cm, "CardioIA — Fase 5 — Fluxo Conversacional")
    canvas.restoreState()


def main():
    if not ENTRADA.exists():
        print(f"Arquivo não encontrado: {ENTRADA}")
        return 1

    estilos = montar_estilos()
    linhas = ENTRADA.read_text(encoding="utf-8").splitlines()

    documento = SimpleDocTemplate(
        str(SAIDA),
        pagesize=A4,
        leftMargin=1.6 * cm,
        rightMargin=1.6 * cm,
        topMargin=1.4 * cm,
        bottomMargin=1.6 * cm,
        title="Relatório do Fluxo Conversacional — CardioIA Fase 5",
        author="CardioIA — FIAP",
    )
    documento.build(
        converter(linhas, estilos),
        onFirstPage=numerar_pagina,
        onLaterPages=numerar_pagina,
    )

    print(f"PDF gerado: {SAIDA.relative_to(RAIZ)}")
    print(f"Páginas: {documento.page}")
    if documento.page > 2:
        print(
            "AVISO: o enunciado pede de 1 a 2 páginas. "
            "Reduza o conteúdo do Markdown."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
