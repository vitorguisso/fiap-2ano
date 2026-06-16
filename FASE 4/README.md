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

# 📚 Como Navegar pela Documentação

Este repositório foi estruturado para permitir diferentes níveis de aprofundamento no projeto CardioIA Vision.

Dependendo do objetivo do leitor, diferentes materiais podem ser consultados.

---

## 📖 README (Este Documento)

O README foi desenvolvido como uma leitura dinâmica do projeto CardioIA Vision.

Além de cumprir sua função tradicional de documentação inicial para desenvolvedores e avaliadores, este documento centraliza os principais recursos do projeto, servindo como ponto de partida para navegação entre os materiais disponibilizados.

Seu objetivo é apresentar, de forma rápida e organizada, os principais elementos da solução desenvolvida, incluindo:

* Contexto do problema;
* Objetivos do projeto;
* Dataset utilizado;
* Pipeline de Visão Computacional;
* Arquiteturas avaliadas;
* Resultados obtidos;
* Comparação entre modelos;
* Protótipo desenvolvido;
* Principais conclusões.

Também são disponibilizados links para os documentos complementares do projeto, permitindo ao leitor aprofundar sua análise conforme o nível de detalhe desejado.

A leitura deste documento permite compreender a visão geral do CardioIA Vision em poucos minutos, enquanto os relatórios e o notebook fornecem análises técnicas, experimentos, métricas e implementações completas.

Para análises mais detalhadas, recomenda-se consultar os documentos complementares apresentados a seguir.


## 📄 Relatório de Pré-processamento (Parte 1)

Documento elaborado especificamente para atender ao entregável da Parte 1 da atividade.

Conforme solicitado no enunciado, este relatório possui caráter resumido (1 a 2 páginas) e apresenta:

- Descrição do dataset;
- Inspeção inicial das imagens;
- Pré-processamento realizado;
- Divisão dos conjuntos de dados;
- Justificativas das escolhas adotadas.

🔗 **Acessar Relatório de Pré-processamento:**  
[Inserir Link]

---

## 📘 Relatório Completo da Fase 4

Documento técnico contendo todo o desenvolvimento do CardioIA Vision.

Neste material são apresentadas análises aprofundadas sobre:

- Fundamentação teórica;
- Dataset utilizado;
- Pipeline completo;
- CNN desenvolvida do zero;
- ResNet50 com Fine Tuning;
- VGG16;
- Métricas de avaliação;
- Matrizes de confusão;
- Curvas de treinamento;
- Comparação entre arquiteturas;
- Desenvolvimento do protótipo;
- Conclusões e trabalhos futuros.

🔗 **Acessar Relatório Completo:**  
[Inserir Link]

---

## 📓 Notebook Google Colab

O notebook contém a implementação completa do projeto.

Este é o material mais detalhado disponível e permite visualizar todo o processo de desenvolvimento realizado pela equipe.

Nele estão disponíveis:

- Códigos-fonte completos;
- Pré-processamento das imagens;
- Treinamento dos modelos;
- Implementação do Fine Tuning;
- Avaliações e métricas;
- Geração de gráficos;
- Matrizes de confusão;
- Desenvolvimento do protótipo CardioIA Vision;
- Comentários técnicos e análises realizadas durante os experimentos.

🔗 **Abrir Notebook Google Colab:**  
[Inserir Link]

---

## 🔍 Guia Rápido

| Se você deseja... | Consulte |
|-------------------|-----------|
| Entender rapidamente o projeto | README |
| Ver apenas o entregável da Parte 1 | Relatório de Pré-processamento |
| Analisar todo o trabalho desenvolvido | Relatório Completo |
| Ver códigos, experimentos e implementação detalhada | Notebook Google Colab |

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

O conjunto de dados utilizado neste projeto foi obtido a partir da plataforma Kaggle e contém imagens de eletrocardiogramas (ECG) distribuídas em quatro categorias clínicas utilizadas para treinamento e avaliação dos modelos de Deep Learning.

🔗 **Kaggle (fonte original):**  
[Acessar Dataset Utilizado](https://www.kaggle.com/datasets/erhmrai/ecg-image-data)

🔗 **Google Drive (dataset original utilizado no projeto):**  
[Acessar Dataset Original](https://drive.google.com/drive/folders/1ph4yYmpLv6MYzpFIoFPi8bj2a2t3_Z_5?usp=drive_link)

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
## 📂 Materiais Complementares

Os arquivos utilizados durante o desenvolvimento foram disponibilizados no Google Drive.

A pasta contém:

- Dataset original;
- Dataset processado;
- Modelos treinados (.keras);
- Arquivos auxiliares do projeto.

🔗 Pasta CardioIA Vision:
[Google Drive](https://drive.google.com/drive/folders/1EUozAz7xARDM7x4axd_glI4zG7Ph4BjI?usp=sharing)

> Observação: o modelo VGG16 foi utilizado na implementação do protótipo CardioIA Vision por apresentar o melhor desempenho entre as arquiteturas avaliadas.


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
