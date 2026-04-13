# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# CardioIA — Sistema Inteligente de Triagem de Sintomas

## Nome do grupo

## 👨‍🎓 Integrantes: 
- <a href="#">Vitor Augusto Prado Guisso</a>
- <a href="#">Vinícius Pereira Santana</a>

## 👩‍🏫 Professores:

### Tutor(a)
- [Caique Nonato da Silva Bezerra](.)

### Coordenador(a)
- [Andre Godoi Chiovato](https://www.linkedin.com/company/inova-fusca)
---

## 🎥 Vídeo de Apresentação

[Acesse aqui o vídeo de explicação do projeto](https://youtu.be/ao-GGlWf8IA)

---

## 📜 Descrição

O projeto **CardioIA** tem como objetivo simular um sistema inteligente de triagem de sintomas relacionados a doenças cardiovasculares, utilizando conceitos fundamentais de **Processamento de Linguagem Natural (NLP)** e **Machine Learning**.

A solução foi dividida em duas etapas principais:


  ### 🔹 Parte 1 — Sistema Base (Regra + Sintomas)

Nesta etapa, foi desenvolvido um sistema baseado em regras, onde o usuário descreve os sintomas e o sistema identifica possíveis diagnósticos com base em um arquivo estruturado ([mapa_sintomas.csv](assets/data/mapa_sintomas.csv)).

O sistema:
- Analisa frases digitadas pelo usuário
- Identifica sintomas dentro da frase
- Exige pelo menos 2 sintomas para um diagnóstico mais assertivo
- Retorna um diagnóstico sugerido

Também possui:
- Consulta manual
- Leitura de múltiplas consultas via arquivo ([frases.txt](assets/data/frases.txt))


## 🧠 Interface do Sistema

O sistema desenvolvido na Parte 1 possui menu interativo:

### 📸 Menu do sistema:
![Menu](assets/img/menu_parte1.PNG)

Funcionalidades:
- Consulta manual de sintomas: o usuário escreve os sintomas e recebe uma resposta para aqueles sintomas. Para efeito de estudos iniciais, foram usados como base 2 sintomas no mínimo para a detecção de uma passível causa.
- Análise de múltiplas frases via arquivo: o programa lê um arquivo com diversos casos, simulando um banco de dados de consultas. 

---

### 🔹 Parte 2 — Inteligência Artificial (Machine Learning)

📎 [Abrir notebook no Google Colab](https://colab.research.google.com/github/vitorguisso/fiap-2ano/blob/main/FASE%202/document/classificacao_risco.ipynb) ou 
💾 [Acessar arquivo notebook (.ipynb)](document/classificacao_risco.ipynb)

Nesta etapa, foi desenvolvido um modelo de classificação de risco baseado em sintomas descritos em linguagem natural, utilizando técnicas de **Processamento de Linguagem Natural (NLP)** e **Machine Learning**.
Foram utilizando:

- TF-IDF (transformação de texto em números)
- Regressão Logística (modelo de classificação)
- Separação de dados em treino e teste
- Avaliação com métricas reais

O modelo classifica as frases em:
- **Alto risco**
- **Baixo risco**
---

## 🧠 Etapas do desenvolvimento

O processo foi dividido em etapas bem definidas:

### 🔹 1. Leitura e análise dos dados

Foi utilizada a base de dados [risco.csv](assets/data/risco.csv), contendo frases e suas respectivas classificações:

- `alto risco`
- `baixo risco`

Inicialmente, foram realizadas:
- Leitura da base com **pandas**
- Visualização das primeiras linhas
- Contagem de exemplos por classe

👉 Resultado:
- Base balanceada (mesma quantidade de exemplos para cada classe)

---

### 🔹 2. Vetorização dos textos (TF-IDF)

As frases foram transformadas em dados numéricos utilizando:

- **TF-IDF (Term Frequency - Inverse Document Frequency)**

Essa técnica permite:
- Identificar a importância de cada palavra
- Converter texto em vetores numéricos
- Tornar os dados compreensíveis para o modelo

---

### 🔹 3. Separação dos dados

Os dados foram divididos em:

- **70% treino**
- **30% teste**

Utilizando:
- `train_test_split`
- `stratify=y` (mantendo o equilíbrio entre classes)

👉 Resultado:
- 16 exemplos para treino  
- 8 exemplos para teste  

---
### 🔹 4. Treinamento do modelo

Foi utilizado o algoritmo:

- **Regressão Logística**

Motivo da escolha:
- Simples  
- Eficiente para classificação de texto  
- Muito utilizado em problemas reais de NLP  

O modelo foi treinado com:

```python
modelo.fit(X_train, y_train)
```

---

### 🔹 5. Avaliação do modelo

O modelo foi avaliado com:

- Acurácia  
- Precision  
- Recall  
- F1-score  
- Matriz de confusão  

---

## 📊 Resultados obtidos

### 📌 Acurácia:
- **0.875 (87,5%)**

---

### 📌 Relatório de classificação:

| Classe       | Precision | Recall | F1-score |
|-------------|----------|--------|----------|
| Alto risco  | 0.80     | 1.00   | 0.89     |
| Baixo risco | 1.00     | 0.75   | 0.86     |

---

### 📌 Matriz de confusão:

```
[[4 0]
 [1 3]]
```

👉 **Interpretação:**
- 4 acertos de alto risco  
- 3 acertos de baixo risco  
- 1 erro de classificação  

---

### 📸 Avaliação do modelo:

![Avaliação do modelo](assets/img/avaliacao_modelo.PNG)

---

## 🧪 Testes práticos

Por fim, o modelo foi testado com frases reais digitadas pelo usuário:

**Exemplos:**

- "dor no peito e dificuldade para respirar" → **alto risco**  
- "leve dor muscular nas costas" → **baixo risco**  
- "febre" → **alto risco (erro esperado)**

  ### 📸 Exemplo de aplicação do modelo:

![Aplicação do modelo](assets/img/aplicacao_modelo.PNG)

---

## ⚠️ Discussão dos resultados

Apesar da boa acurácia, foram observadas limitações importantes:

### 🔹 1. Base de dados pequena
- Apenas 24 exemplos no total  
- Limita a capacidade de generalização  

### 🔹 2. Falta de contexto nas frases
- Palavras isoladas como "febre" ou "sede" podem gerar interpretações incorretas  

### 🔹 3. Modelo sensível a palavras-chave
- O modelo aprende padrões simples  
- Pode classificar errado frases fora do padrão de treino  

---

## ✅ Conclusões da Parte 2

O modelo demonstrou que:

- É possível classificar sintomas com NLP  
- Mesmo modelos simples podem atingir bons resultados  
- A qualidade e quantidade dos dados impactam diretamente o desempenho  

---

## 🚀 Possíveis melhorias futuras

- Aumentar a base de dados  
- Incluir mais variações de frases  
- Utilizar modelos mais robustos (ex: Random Forest, XGBoost)  
- Aplicar técnicas mais avançadas de NLP
  
---

## 🧠 Conclusão Geral do Projeto

O desenvolvimento do projeto **CardioIA** permitiu a aplicação prática de conceitos fundamentais de Inteligência Artificial, especialmente no contexto de **Processamento de Linguagem Natural (NLP)** e **classificação de dados textuais**.

Na **Parte 1**, foi possível compreender a lógica por trás de sistemas baseados em regras, onde a identificação de padrões ocorre por meio de correspondência direta entre palavras-chave e sintomas previamente definidos. Essa abordagem demonstrou ser eficiente para cenários controlados, porém limitada quando exposta à variabilidade da linguagem natural.

Já na **Parte 2**, o uso de técnicas de Machine Learning representou um avanço significativo, permitindo que o sistema aprendesse padrões a partir dos dados. A utilização de **TF-IDF** para vetorização e **Regressão Logística** como modelo de classificação mostrou-se adequada para o problema proposto, atingindo uma acurácia de **87,5%**, mesmo com uma base de dados reduzida.

Durante os testes, observou-se que o modelo apresentou bom desempenho na identificação de padrões relacionados a sintomas de maior risco. No entanto, também foram identificadas limitações importantes, como a dificuldade em interpretar palavras isoladas ou fora do contexto de treinamento, evidenciando a dependência do modelo em relação à qualidade e diversidade dos dados utilizados.

Um dos principais desafios enfrentados no desenvolvimento foi justamente a **limitação da base de dados**, tanto em quantidade quanto em variedade de expressões linguísticas. Isso impacta diretamente na capacidade de generalização do modelo, tornando-o mais suscetível a erros em situações não previstas durante o treinamento.

Além disso, o projeto evidenciou que, embora modelos simples possam apresentar bons resultados iniciais, sistemas reais exigem:
- Bases de dados mais robustas
- Maior diversidade de exemplos
- Técnicas mais avançadas de NLP
- Integração com conhecimento de domínio (neste caso, médico)

De forma geral, o projeto atingiu plenamente os objetivos propostos pela atividade, permitindo não apenas a implementação técnica de um modelo de classificação, mas também a compreensão crítica sobre suas limitações e possibilidades de evolução.

Por fim, conclui-se que a combinação entre **lógica baseada em regras** e **aprendizado de máquina** representa uma abordagem complementar e eficaz, sendo amplamente utilizada em sistemas reais de triagem e apoio à decisão — reforçando a relevância prática dos conceitos abordados nesta fase do curso.

---

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:


- <b>assets</b>: Arquivos não estruturados do projeto
  - <b>data</b>: Base de dados utilizada (`frases.txt`, `mapa_sintomas.csv`, `risco.csv`)
  - <b>img</b>: Imagens e prints dos resultados

- <b>config</b>: Pasta reservada para configurações futuras do projeto

- <b>document</b>: Contém o notebook da Parte 2  
  - `classificacao_risco.ipynb`


- <b>src</b>: Código principal do sistema  
  - `diagnostico.py`

- <b>README.md</b>: Documentação do projeto

---

## 🔧 Como executar o código

### 🔹 Pré-requisitos

- Python 3.10+
- Bibliotecas:
  - pandas
  - scikit-learn

### 🔹 Parte 1 — Sistema de Diagnóstico

1. Baixe o repositório completo clicando em **Code > Download ZIP** no GitHub.  
2. Extraia os arquivos no seu computador.  
3. Abra o terminal na pasta **FASE 2**.  
4. Execute o comando: python src/diagnostico.py


> ⚠️ Importante: o sistema depende da estrutura completa do projeto. Não execute o arquivo `.py` isoladamente.

---

### 🔹 Parte 2 — Modelo de IA

Acesse o notebook:

📎 [Abrir notebook no Google Colab](https://colab.research.google.com/github/vitorguisso/fiap-2ano/blob/main/FASE%202/document/classificacao_risco.ipynb) ou 
💾 [Acessar arquivo notebook (.ipynb)](document/classificacao_risco.ipynb)

Execute no:

- Google Colab  
- Jupyter Notebook  

---

## 🗃 Histórico de lançamentos

* 0.2.0 - 11/04/2026  
    * Implementação do modelo de Machine Learning  

* 0.1.0 - 10/04/2026  
    * Sistema base de diagnóstico por sintomas  

---

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
