import csv
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAPA_PATH = os.path.join(BASE_DIR, "..", "assets", "data", "mapa_sintomas.csv")
FRASES_PATH = os.path.join(BASE_DIR, "..", "assets", "data", "frases.txt")


def carregar_mapa(caminho_csv):
    mapa = []

    with open(caminho_csv, mode="r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            mapa.append(linha)

    return mapa


def identificar_diagnostico(frase, mapa):
    frase = frase.lower()
    contagem_doencas = {}

    for item in mapa:
        sintoma1 = item["sintoma1"].lower()
        sintoma2 = item["sintoma2"].lower()
        doenca = item["doenca"]

        sintomas_encontrados_na_linha = 0

        if sintoma1 in frase:
            sintomas_encontrados_na_linha += 1

        if sintoma2 in frase:
            sintomas_encontrados_na_linha += 1

        if sintomas_encontrados_na_linha > 0:
            if doenca not in contagem_doencas:
                contagem_doencas[doenca] = 0

            contagem_doencas[doenca] += sintomas_encontrados_na_linha

    if len(contagem_doencas) == 0:
        return "Diagnóstico não identificado"

    maior_doenca = max(contagem_doencas, key=contagem_doencas.get)
    maior_qtd = contagem_doencas[maior_doenca]

    if maior_qtd >= 2:
        return maior_doenca

    return "Diagnóstico inconclusivo (poucos sintomas)"


def exibir_menu():
    print("\n=== CARDIOIA - CONSULTA INICIAL DE SINTOMAS ===")
    print("1 - Realizar consulta manual")
    print("2 - Ler arquivo de sintomas")
    print("3 - Sair")


def realizar_consulta_manual(mapa):
    print("\nDescreva os sintomas do paciente:")
    sintomas = input(">> ").strip()

    if sintomas == "":
        print("\nNenhum sintoma foi informado.")
        return

    diagnostico = identificar_diagnostico(sintomas, mapa)

    print("\nRESULTADO DA ANÁLISE")
    print(f"Sintomas informados: {sintomas}")
    print(f"Diagnóstico sugerido: {diagnostico}")
    print("\nAviso: este sistema é apenas um protótipo acadêmico e não substitui avaliação médica.")


def analisar_arquivo(caminho_txt, mapa):
    try:
        with open(caminho_txt, mode="r", encoding="utf-8") as arquivo:
            frases = arquivo.readlines()

        if len(frases) == 0:
            print("\nO arquivo de sintomas está vazio.")
            return

        print("\n=== RESULTADO DAS CONSULTAS DO ARQUIVO ===")

        contador_consultas = 0

        for frase in frases:
            frase = frase.strip()

            if frase == "":
                continue

            contador_consultas += 1
            diagnostico = identificar_diagnostico(frase, mapa)

            print(f"\nConsulta {contador_consultas}:")
            print(f"Sintomas informados: {frase}")
            print(f"Diagnóstico sugerido: {diagnostico}")

        print("\nLeitura do arquivo concluída com sucesso.")
        print("Aviso: este sistema é apenas um protótipo acadêmico e não substitui avaliação médica.")

    except FileNotFoundError:
        print("\nArquivo de sintomas não encontrado.")


def main():
    try:
        mapa = carregar_mapa(MAPA_PATH)
    except FileNotFoundError:
        print("\nErro: arquivo mapa_sintomas.csv não encontrado.")
        print(f"Caminho esperado: {MAPA_PATH}")
        return

    while True:
        exibir_menu()
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            realizar_consulta_manual(mapa)

        elif opcao == "2":
            analisar_arquivo(FRASES_PATH, mapa)

        elif opcao == "3":
            print("\nEncerrando o sistema CardioIA...")
            break

        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    main()