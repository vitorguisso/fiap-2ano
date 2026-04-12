# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# CardioIA — Sistema Inteligente de Triagem de Sintomas

## Nome do grupo

## 👨‍🎓 Integrantes: 
- <a href="#">Vitor Augusto Prado Guisso</a>
- <a href="#">Ryan Carlos Sousa Alves da Cunha</a>
- <a href="#">Vinícius Pereira Santana</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="#">Nome do Tutor</a>
### Coordenador(a)
- <a href="#">Nome do Coordenador</a>

---

## 📜 Descrição

O projeto **CardioIA** tem como objetivo simular um sistema inteligente de triagem de sintomas relacionados a doenças cardiovasculares, utilizando conceitos fundamentais de **Processamento de Linguagem Natural (NLP)** e **Machine Learning**.

A solução foi dividida em duas etapas principais:

### 🔹 Parte 1 — Sistema Base (Regra + Sintomas)

Nesta etapa, foi desenvolvido um sistema baseado em regras, onde o usuário descreve os sintomas e o sistema identifica possíveis diagnósticos com base em um arquivo estruturado (`mapa_sintomas.csv`).

O sistema:
- Analisa frases digitadas pelo usuário
- Identifica sintomas dentro da frase
- Exige pelo menos 2 sintomas para um diagnóstico mais assertivo
- Retorna um diagnóstico sugerido

Também possui:
- Consulta manual
- Leitura de múltiplas consultas via arquivo (`frases.txt`)

---

### 🔹 Parte 2 — Inteligência Artificial (Machine Learning)

Nesta etapa, foi desenvolvido um modelo de classificação utilizando:

- TF-IDF (transformação de texto em números)
- Regressão Logística (modelo de classificação)
- Separação de dados em treino e teste
- Avaliação com métricas reais

O modelo classifica as frases em:
- **Alto risco**
- **Baixo risco**

---

## 📊 Resultados do Modelo

### 📌 Acurácia do modelo:
- **0.875 (87,5%)**

### 📌 Relatório de classificação:
- Boa precisão geral
- Excelente recall para casos de alto risco

### 📌 Matriz de confusão:
- 1 erro de classificação identificado

### 📸 Avaliação do modelo:
![Avaliação do modelo](assets/img/avaliacao_modelo.PNG)

---

## 🧪 Testes do Modelo

Exemplos reais de classificação:

- "dor no peito e dificuldade para respirar" → **alto risco**
- "leve dor muscular nas costas" → **baixo risco**

### 📸 Aplicação do modelo:
![Aplicação do modelo](assets/img/aplicacao_modelo.PNG)

---

## 🧠 Interface do Sistema

O sistema desenvolvido na Parte 1 possui menu interativo:

### 📸 Menu do sistema:
![Menu](assets/img/menu_parte1.PNG)

Funcionalidades:
- Consulta manual de sintomas
- Análise de múltiplas frases via arquivo
- Diagnóstico automatizado

---

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: Configurações internas do GitHub (templates e automações)

- <b>assets</b>: Arquivos não estruturados do projeto
  - <b>data</b>: Base de dados utilizada (`frases.txt`, `mapa_sintomas.csv`, `risco.csv`)
  - <b>img</b>: Imagens e prints dos resultados

- <b>config</b>: Pasta reservada para configurações futuras do projeto

- <b>document</b>: Contém o notebook da Parte 2  
  - `classificacao_risco.ipynb`

- <b>scripts</b>: Scripts auxiliares (não utilizados nesta fase)

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

Instalação:

```bash
pip install pandas scikit-learn
