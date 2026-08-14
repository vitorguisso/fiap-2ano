"""
CardioIA - Fase 5
Auditoria de consistencia da entrega.

Verifica automaticamente aquilo que costuma passar despercebido na revisao manual:

  1. todo link relativo do README aponta para um arquivo que existe;
  2. os numeros citados no README batem com a skill real;
  3. nenhuma credencial foi versionada por engano;
  4. os arquivos esperados da entrega estao presentes.

Uso (a partir da raiz do projeto):
    python scripts/auditar_entrega.py
"""

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
README = RAIZ / "README.md"
SKILL = RAIZ / "config" / "watson" / "skill-cardioia-dialog.json"

ENTREGAVEIS = [
    ("Código do backend", "src/backend/app.py"),
    ("Cliente do Watson", "src/backend/watson_client.py"),
    ("Interface de interação", "src/backend/templates/index.html"),
    ("Dependências", "src/backend/requirements.txt"),
    ("Exemplo de configuração", "src/backend/.env.example"),
    ("Skill exportada (JSON)", "config/watson/skill-cardioia-dialog.json"),
    ("Relatório (PDF)", "document/RELATORIO_FLUXO_CONVERSACIONAL_FASE5.pdf"),
    ("Documento técnico do fluxo", "document/FLUXO_CONVERSACIONAL.md"),
    ("README", "README.md"),
    ("Gitignore", ".gitignore"),
]

problemas = []
alertas = []


def verificar_links_readme():
    texto = README.read_text(encoding="utf-8")

    # Comentarios HTML nao sao renderizados: um link de exemplo escrito dentro
    # de um comentario nao e link quebrado. Removemos antes de analisar.
    texto = re.sub(r"<!--.*?-->", "", texto, flags=re.DOTALL)

    # Captura [rotulo](destino) ignorando links externos e ancoras
    for rotulo, destino in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", texto):
        if destino.startswith(("http://", "https://", "#", "mailto:")):
            continue
        caminho = RAIZ / destino.split("#")[0]
        if not caminho.exists():
            problemas.append(f"Link quebrado no README: [{rotulo}]({destino})")

    # Imagens referenciadas via HTML (o logo do template FIAP)
    for src in re.findall(r'<img[^>]+src="([^"]+)"', texto):
        if src.startswith(("http://", "https://")):
            continue
        if not (RAIZ / src.lstrip("./")).exists():
            alertas.append(f"Imagem ausente: {src}")


def verificar_numeros():
    skill = json.loads(SKILL.read_text(encoding="utf-8"))
    texto = README.read_text(encoding="utf-8")

    reais = {
        "intenções": len(skill["intents"]),
        "exemplos": sum(len(i["examples"]) for i in skill["intents"]),
        "entidades": len(skill["entities"]),
        "nós": len(skill["dialog_nodes"]),
    }

    esperados = {
        "intenções": r"(\d+)\s+inten[çc]",
        "exemplos": r"(\d+)\s+exemplos de treino",
        "entidades": r"(\d+)\s+entidades customizadas",
        "nós": r"(\d+)\s+n[óo]s de di[áa]logo",
    }

    for chave, padrao in esperados.items():
        citados = {int(v) for v in re.findall(padrao, texto)}
        if not citados:
            alertas.append(f"README não cita a quantidade de {chave}")
        elif citados != {reais[chave]}:
            problemas.append(
                f"Divergência em {chave}: README cita {sorted(citados)}, "
                f"skill tem {reais[chave]}"
            )

    print("  Skill real:", ", ".join(f"{v} {k}" for k, v in reais.items()))


def verificar_credenciais():
    if (RAIZ / "src/backend/.env").exists():
        gitignore = (RAIZ / ".gitignore").read_text(encoding="utf-8")
        if ".env" not in gitignore:
            problemas.append(".env existe e NÃO está no .gitignore")
        else:
            print("  .env presente localmente e devidamente ignorado pelo Git")

    # Procura credencial escrita direto no codigo
    suspeitos = re.compile(
        r"(apikey|api_key|assistant_id|secret)\s*=\s*['\"][A-Za-z0-9_\-]{15,}['\"]",
        re.IGNORECASE,
    )
    for arquivo in RAIZ.rglob("*.py"):
        if "material de apoio" in str(arquivo) or ".venv" in str(arquivo):
            continue
        for numero, linha in enumerate(
            arquivo.read_text(encoding="utf-8").splitlines(), 1
        ):
            if suspeitos.search(linha):
                problemas.append(
                    f"Possível credencial em {arquivo.relative_to(RAIZ)}:{numero}"
                )


def verificar_entregaveis():
    for nome, caminho in ENTREGAVEIS:
        if not (RAIZ / caminho).exists():
            problemas.append(f"Entregável ausente: {nome} ({caminho})")


def verificar_pendencias():
    for arquivo in [README, RAIZ / "document/FLUXO_CONVERSACIONAL.md"]:
        texto = arquivo.read_text(encoding="utf-8")
        pendentes = len(re.findall(r"PENDENTE|pendente de", texto))
        if pendentes:
            alertas.append(
                f"{arquivo.name}: {pendentes} marcação(ões) de pendência "
                "— resolver antes da entrega final"
            )


def main():
    print("=" * 74)
    print("AUDITORIA DA ENTREGA — CardioIA Fase 5")
    print("=" * 74)

    verificar_entregaveis()
    verificar_links_readme()
    verificar_numeros()
    verificar_credenciais()
    verificar_pendencias()

    print()
    if problemas:
        print(f"🔴 {len(problemas)} problema(s) que impedem a entrega:")
        for item in problemas:
            print(f"   - {item}")
    else:
        print("🟢 Nenhum problema bloqueante encontrado.")

    if alertas:
        print(f"\n🟡 {len(alertas)} ponto(s) de atenção:")
        for item in alertas:
            print(f"   - {item}")

    print("\n" + "=" * 74)
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main())
