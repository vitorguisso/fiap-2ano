# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/">
<img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width="40%">
</a>
</p>

<br>

# CardioIA Vision – Classificação Inteligente de Eletrocardiogramas com Deep Learning

---

## 👨‍🎓 Integrantes

* Vitor Augusto Prado Guisso (RM562317)
* Vinícius Pereira Santana (RM564940)
* Isaac Maciel (RM98222)

---

## 👩‍🏫 Professores

### Tutor(a)

* Caique Nonato da Silva Bezerra

### Coordenador(a)

* Andre Godoi Chiovato

---

# 📜 Descrição

O CardioIA Vision é o módulo de Visão Computacional do ecossistema CardioIA, desenvolvido com o objetivo de investigar a aplicação de técnicas de Deep Learning na classificação automática de imagens de eletrocardiogramas (ECG).

Nesta fase do projeto foram utilizadas Redes Neurais Convolucionais (CNNs) e técnicas de Transfer Learning para identificar padrões presentes em exames cardíacos e classificá-los em diferentes categorias clínicas.

A solução foi construída utilizando um dataset público de imagens médicas e contempla todas as etapas de um pipeline de Visão Computacional:

```txt
Dataset → Pré-processamento → CNN → Transfer Learning → Avaliação → Protótipo
```

Foram avaliadas três abordagens distintas:

* CNN desenvolvida do zero;
* ResNet50 com Fine Tuning;
* VGG16 com Transfer Learning.

Após a comparação dos resultados, a arquitetura VGG16 apresentou o melhor desempenho geral e foi utilizada na construção do protótipo CardioIA Vision.

O sistema permite que o usuário envie uma imagem de eletrocardiograma e receba automaticamente uma classificação produzida pelo modelo treinado.


---

# 📚 Documentação do Projeto

Este repositório foi organizado para atender tanto aos requisitos acadêmicos da atividade quanto à necessidade de documentação técnica detalhada do projeto.

Foram disponibilizados três níveis de documentação:

### 📄 Relatório de Pré-processamento (Parte 1)

Documento resumido elaborado conforme solicitado no enunciado da atividade (SOMENTE 2 PÁGINAS - MUITO POUCO PARA UM RELATÓRIO DE NPIVEL SUPERIOR) 
 
O objetivo deste relatório é apresentar, de forma sucinta (1 a 2 páginas), as etapas de preparação dos dados, incluindo inspeção do dataset, pré-processamento das imagens e organização dos conjuntos de treinamento, validação e teste.

🔗 **Acessar Relatório de Pré-processamento:**  
[Inserir Link]

---

### 📘 Relatório Completo da Fase 4

Documento técnico contendo todo o desenvolvimento do projeto CardioIA Vision.

Inclui:

- Fundamentação teórica;
- Descrição do dataset;
- Pipeline de Visão Computacional;
- Desenvolvimento da CNN própria;
- Implementação da ResNet50 com Fine Tuning;
- Implementação da VGG16;
- Avaliação dos modelos;
- Matrizes de confusão;
- Métricas de desempenho;
- Comparação entre arquiteturas;
- Desenvolvimento do protótipo;
- Conclusões e trabalhos futuros.

🔗 **Acessar Relatório Completo:**  
[Inserir Link]

---

### 📓 Notebook Google Colab

Para uma análise ainda mais aprofundada, todo o desenvolvimento do projeto está disponível no notebook principal.

O notebook contém:

- Código-fonte completo;
- Pré-processamento das imagens;
- Treinamento dos modelos;
- Geração das métricas;
- Matrizes de confusão;
- Curvas de treinamento;
- Implementação do protótipo CardioIA Vision;
- Comentários e análises realizadas durante o desenvolvimento.

🔗 **Abrir Notebook Google Colab:**  
[Inserir Link]

---

### 🔍 Sugestão de Navegação

| Objetivo | Documento Recomendado |
|-----------|----------------------|
| Entender rapidamente o pré-processamento exigido pela atividade | Relatório de Pré-processamento |
| Compreender todo o projeto e suas análises | Relatório Completo |
| Ver códigos, implementações e experimentos realizados | Notebook Google Colab |


---

# 🏥 Objetivo do Projeto

Desenvolver um Assistente Cardiológico Virtual capaz de:

* Processar imagens médicas de eletrocardiogramas;
* Identificar padrões cardíacos por meio de Inteligência Artificial;
* Classificar exames em diferentes categorias clínicas;
* Demonstrar a aplicação prática da Visão Computacional na saúde;
* Disponibilizar um protótipo interativo para análise dos resultados.

---

# 📊 Dataset Utilizado

Foi utilizado o dataset público:

## ECG Images Dataset of Cardiac Patients

🔗 Kaggle:

https://www.kaggle.com/datasets/umeradnaan/ecg-images-dataset-of-cardiac-patients

O conjunto de dados contém imagens de eletrocardiogramas distribuídas em quatro categorias:

* Abnormal Heartbeat ECG Images
* Myocardial Infarction ECG Images
* Normal ECG Images
* Post MI History ECG Images

Total de imagens utilizadas:

```txt
928 imagens
```

---

# 🧠 Arquiteturas Avaliadas

Durante o desenvolvimento foram avaliadas três arquiteturas de Deep Learning.

## 1️⃣ CNN Desenvolvida do Zero

Rede Neural Convolucional construída especificamente para o projeto contendo:

* Camadas convolucionais;
* MaxPooling;
* Flatten;
* Camadas densas;
* Softmax.

---

## 2️⃣ ResNet50 com Fine Tuning

Modelo pré-treinado na base ImageNet utilizando:

* Transfer Learning;
* Fine Tuning das camadas superiores;
* Ajuste para classificação de ECGs.

---

## 3️⃣ VGG16

Modelo pré-treinado na ImageNet utilizado como extrator de características.

Após os experimentos, apresentou o melhor desempenho geral do projeto.

---

# 📈 Resultados Obtidos

| Modelo                 | Accuracy |
| ---------------------- | -------- |
| CNN Própria            | 31%      |
| ResNet50 + Fine Tuning | 25%      |
| VGG16                  | 49%      |

O modelo VGG16 apresentou:

* Melhor capacidade de generalização;
* Melhor equilíbrio entre treinamento e validação;
* Melhor desempenho nas classes relacionadas a anormalidades cardíacas e infarto do miocárdio.

---

# 📊 Matrizes de Confusão

## CNN Desenvolvida do Zero

![CNN](assets/matriz_cnn.png)

---

## ResNet50

![ResNet50](assets/matriz_resnet50.png)

---

## VGG16

![VGG16](assets/matriz_vgg16.png)

---

# 📈 Curvas de Treinamento

As curvas de treinamento e validação foram apresentadas para o modelo VGG16 por ter sido a arquitetura com melhor desempenho geral.

## Accuracy

![Accuracy](assets/vgg_accuracy.png)

---

## Loss

![Loss](assets/vgg_loss.png)

---

# 🖥 Protótipo CardioIA Vision

Após a seleção do melhor modelo foi desenvolvido um protótipo interativo utilizando Google Colab.

O sistema permite:

* Informar o nome do paciente;
* Enviar uma imagem de ECG;
* Processar a imagem utilizando o modelo VGG16;
* Exibir a classificação prevista;
* Informar o nível de confiança da predição.

## Exemplo de utilização

![Protótipo](assets/prototipo_cardioia_vision.png)

⚠️ Importante:

O protótipo possui finalidade acadêmica e demonstrativa. Seu objetivo é apresentar a aplicação prática do modelo desenvolvido, não representar a acurácia real da solução, a qual foi avaliada separadamente por meio das métricas apresentadas no projeto.

---

# 🚀 Notebook Google Colab

## Notebook Principal

🔗 Colab:

https://colab.research.google.com/drive/SEU_LINK_AQUI

O notebook contém:

* Pré-processamento;
* Organização dos dados;
* CNN própria;
* ResNet50;
* VGG16;
* Avaliação dos modelos;
* Protótipo interativo.

---

# 📄 Relatório Acadêmico

## Relatório Completo da Fase 4

🔗 PDF:

document/RELATORIO_FASE4_FIAP.pdf

O relatório contém:

* Fundamentação teórica;
* Visão Computacional;
* Deep Learning;
* Transfer Learning;
* Pré-processamento;
* Avaliação dos modelos;
* Comparação dos resultados;
* Protótipo desenvolvido;
* Conclusões.

---

# 🚀 Tecnologias Utilizadas

## Inteligência Artificial

* TensorFlow
* Keras
* NumPy
* Scikit-Learn

## Visão Computacional

* OpenCV
* PIL
* Matplotlib

## Ambiente

* Google Colab
* Python 3

---

# 🧠 Conceitos Aplicados

* Visão Computacional
* Deep Learning
* Redes Neurais Convolucionais
* Transfer Learning
* Fine Tuning
* Classificação de Imagens
* Inteligência Artificial aplicada à Saúde
* Avaliação de Modelos
* Machine Learning

---

# 📊 Funcionalidades Implementadas

## ✅ Pré-processamento

* Redimensionamento;
* Normalização;
* Organização dos dados;
* Divisão treino/validação/teste.

## ✅ CNN Desenvolvida do Zero

* Construção da arquitetura;
* Treinamento;
* Avaliação.

## ✅ Transfer Learning

* ResNet50;
* VGG16.

## ✅ Avaliação

* Accuracy;
* Precision;
* Recall;
* F1-score;
* Matriz de confusão.

## ✅ Protótipo

* Upload de ECG;
* Nome do paciente;
* Classificação automática;
* Nível de confiança.

---

# 📁 Estrutura de Pastas

## 📂 assets

Imagens utilizadas na documentação:

* matrizes de confusão;
* gráficos;
* protótipo;
* exemplos do dataset;
* logo FIAP.

## 📂 document

Documentação acadêmica:

* relatório da fase;
* referências bibliográficas.

## 📂 notebooks

* CardioIA_Vision_Fase4.ipynb

## 📄 README.md

Arquivo principal de documentação do projeto.

---

# ▶️ Como Executar

## 1. Abrir o Notebook

Acesse:

```txt
Notebook Google Colab
```

ou

```txt
notebooks/CardioIA_Vision_Fase4.ipynb
```

---

## 2. Executar as células

Executar o notebook sequencialmente.

---

## 3. Utilizar o protótipo

Ao final do notebook:

* Informar o nome do paciente;
* Fazer upload de uma imagem ECG;
* Clicar em "Analisar ECG";
* Visualizar o resultado produzido pela Inteligência Artificial.

---

# 📚 Referências

* TensorFlow Documentation: https://www.tensorflow.org/
* Keras Documentation: https://keras.io/
* Kaggle ECG Dataset: https://www.kaggle.com/datasets/umeradnaan/ecg-images-dataset-of-cardiac-patients
* Goodfellow, I.; Bengio, Y.; Courville, A. Deep Learning. MIT Press.
* Chollet, F. Deep Learning with Python.

---

# 🏁 Conclusão

O CardioIA Vision demonstrou a viabilidade da aplicação de técnicas de Visão Computacional e Deep Learning na classificação automática de eletrocardiogramas.

Entre os modelos avaliados, o VGG16 apresentou o melhor desempenho, sendo utilizado na construção de um protótipo funcional capaz de receber imagens médicas e produzir classificações automáticas.

A solução representa mais um passo na evolução do ecossistema CardioIA e demonstra como a Inteligência Artificial pode contribuir para o desenvolvimento de ferramentas de apoio à análise de exames médicos.
