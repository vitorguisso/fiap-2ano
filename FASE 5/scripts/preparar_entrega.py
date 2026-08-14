"""
CardioIA - Fase 5
Monta a pasta de entrega, pronta para subir ao GitHub.

POR QUE EXISTE
    A pasta de trabalho contem material que NAO deve ir para um repositorio
    publico: os PDFs das aulas (pessoais, marcados com nome e RM do aluno), o
    arquivo de credenciais .env, o enunciado e arquivos de apoio.

    Este script copia apenas o que compoe a entrega para a subpasta "FASE 5",
    no formato esperado pelo repositorio da disciplina
    (github.com/vitorguisso/fiap-2ano), e confere que nenhuma credencial
    escapou junto.

USO (a partir da raiz do projeto):
    python scripts/preparar_entrega.py

Depois, basta arrastar a pasta "FASE 5" gerada para o GitHub.
Rode novamente sempre que alterar qualquer arquivo do projeto.
"""

import re
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "FASE 5"

# Diretorios que nunca entram na entrega
PASTAS_EXCLUIDAS = {
    "FASE 5",           # a propria saida, para nao copiar dentro de si mesma
    "material de apoio",  # PDFs das aulas: pessoais, com nome e RM
    "__pycache__",
    ".git",
    ".claude",
    ".venv",
    "venv",
}

# Arquivos que nunca entram na entrega
ARQUIVOS_EXCLUIDOS = {
    ".env",                              # credenciais
    "CLAUDE.md",                         # instrucoes de trabalho, nao e entregavel
    "enunciado_atividade.txt",           # material de apoio
    "link git hub trabalho.txt",         # anotacao pessoal
    "TEMPLATE PADRÃO FIAP COMO EXEMPLO.md",  # referencia de formatacao
    # Documento interno de conferencia. Nao e entregavel do enunciado e contem
    # uma auto-estimativa de nota, que soaria presuncosa em repositorio publico.
    "AUDITORIA_FINAL.md",
}

EXTENSOES_EXCLUIDAS = {".pyc", ".log", ".tmp"}

# Padroes que indicam credencial vazada em texto
PADROES_SUSPEITOS = [
    re.compile(r"WATSON_API_KEY\s*=\s*\S+"),
    re.compile(r"\bapikey\b\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{20,}"),
]


def deve_copiar(caminho):
    rel = caminho.relative_to(RAIZ)
    if set(rel.parts) & PASTAS_EXCLUIDAS:
        return False
    if caminho.name in ARQUIVOS_EXCLUIDOS:
        return False
    if caminho.suffix in EXTENSOES_EXCLUIDAS:
        return False
    return True


def verificar_credenciais(pasta):
    """Ultima linha de defesa: procura credencial nos arquivos ja copiados."""
    problemas = []
    for arquivo in pasta.rglob("*"):
        if not arquivo.is_file():
            continue
        if arquivo.suffix not in {".py", ".md", ".json", ".txt", ".html", ".example", ""}:
            continue
        try:
            conteudo = arquivo.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for padrao in PADROES_SUSPEITOS:
            for achado in padrao.findall(conteudo):
                # .env.example tem a variavel vazia de proposito
                if achado.rstrip().endswith("="):
                    continue
                problemas.append((arquivo.relative_to(pasta), achado[:60]))
    return problemas


def main():
    if SAIDA.exists():
        shutil.rmtree(SAIDA)
    SAIDA.mkdir(parents=True)

    copiados = []
    for caminho in sorted(RAIZ.rglob("*")):
        if caminho.is_dir() or not deve_copiar(caminho):
            continue
        rel = caminho.relative_to(RAIZ)
        destino = SAIDA / rel
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(caminho, destino)
        copiados.append(rel)

    print("=" * 74)
    print("PASTA DE ENTREGA")
    print("=" * 74)
    print(f"\nDestino: {SAIDA}")
    print(f"\n{len(copiados)} arquivo(s) copiado(s):")
    for rel in copiados:
        print("   ", rel)

    print("\nFora da entrega, de proposito:")
    for nome in sorted(ARQUIVOS_EXCLUIDOS):
        print("   ", nome)
    print("    material de apoio/  (PDFs das aulas, pessoais)")

    print("\n" + "=" * 74)
    print("VERIFICACAO DE SEGURANCA")
    print("=" * 74)

    env_vazado = [p for p in SAIDA.rglob(".env")]
    problemas = verificar_credenciais(SAIDA)

    if env_vazado:
        print("  🔴 arquivo .env encontrado na entrega:", env_vazado)
    else:
        print("  🟢 nenhum arquivo .env na entrega")

    if problemas:
        print("  🔴 possivel credencial encontrada:")
        for arquivo, trecho in problemas:
            print(f"       {arquivo}: {trecho}")
    else:
        print("  🟢 nenhuma credencial encontrada nos arquivos")

    print("\n" + "=" * 74)
    if env_vazado or problemas:
        print("NAO SUBA ESTA PASTA. Corrija os problemas acima primeiro.")
        return 1

    print("Pasta pronta. Arraste a pasta \"FASE 5\" para o GitHub:")
    print("  github.com/vitorguisso/fiap-2ano  ->  Add file  ->  Upload files")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
