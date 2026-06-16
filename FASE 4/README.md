# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="./assets/logos/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" width="40%">
  </a>
</p>


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
# 📊 Dataset Utilizado

Foi utilizado o dataset público:

## ECG Images Dataset of Cardiac Patients

O conjunto de dados utilizado neste projeto foi obtido a partir da plataforma Kaggle e contém imagens de eletrocardiogramas (ECG) distribuídas em quatro categorias clínicas utilizadas para treinamento e avaliação dos modelos de Deep Learning.

🔗 **Kaggle (fonte original):**  
[Acessar Dataset Utilizado no Kaggle](https://www.kaggle.com/datasets/erhmrai/ecg-image-data)

🔗 **Google Drive (dataset original utilizado no projeto):**  
[Acessar Dataset Utilizado no Drive](https://drive.google.com/drive/folders/1ph4yYmpLv6MYzpFIoFPi8bj2a2t3_Z_5?usp=drive_link)

```txt
928 imagens
```
--- 
## 🔄 Pipeline do Projeto

O CardioIA Vision foi desenvolvido seguindo um pipeline completo de Visão Computacional, desde a obtenção dos dados até a construção do protótipo final.

O fluxo contempla as etapas de preparação das imagens, treinamento de diferentes arquiteturas de Deep Learning, avaliação dos resultados e implementação de uma interface interativa para demonstração da solução.

<p align="center">
  <img src="./assets/fluxograma/fluxograma_fase4.png" alt="Pipeline CardioIA Vision" width="1000">
</p>

### Etapas do Pipeline

| Etapa | Descrição |
|---------|---------|
| 1. Dataset Público | Utilização do dataset ECG Images Dataset of Cardiac Patients. |
| 2. Inspeção dos Dados | Verificação das classes, quantidade de imagens, resolução e formato das imagens. |
| 3. Pré-processamento | Conversão para RGB, redimensionamento para 224x224 pixels e normalização dos pixels. |
| 4. Organização dos Dados | Divisão em conjuntos de treinamento (70%), validação (15%) e teste (15%). |
| 5. Data Augmentation | Aplicação de rotações, zoom e deslocamentos para aumentar a variabilidade dos dados. |
| 6. Treinamento dos Modelos | Implementação de CNN própria, ResNet50 com Fine Tuning e VGG16 com Transfer Learning. |
| 7. Avaliação | Análise utilizando Accuracy, Precision, Recall, F1-Score e Matriz de Confusão. |
| 8. Comparação | Comparação quantitativa entre os modelos desenvolvidos. |
| 9. Seleção do Melhor Modelo | Escolha da VGG16 como arquitetura de melhor desempenho. |
| 10. Protótipo CardioIA Vision | Interface interativa para classificação de exames de ECG. |
| 11. Resultado Interpretável | Exibição da classe prevista e nível de confiança para apoio à tomada de decisão. |

### Resultado Final

Após a comparação das arquiteturas avaliadas, a **VGG16 com Transfer Learning** apresentou o melhor desempenho geral, alcançando aproximadamente **49% de acurácia**, sendo selecionada para compor o protótipo CardioIA Vision.

O protótipo permite que o usuário realize o upload de uma imagem de eletrocardiograma e receba automaticamente uma classificação produzida pelo modelo treinado, demonstrando de forma prática a aplicação de técnicas de Inteligência Artificial na análise de exames médicos.

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
- [Relatório de Pré-processamento - Entrega 1](https://github.com/vitorguisso/fiap-2ano/blob/main/FASE%204/document/RELAT%C3%93RIO_PRE-PROCESSAMENTO_FASE4_ENTREGA.pdf)

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
- [Relatório Completo da Fase 4](https://github.com/vitorguisso/fiap-2ano/blob/main/FASE%204/document/RELAT%C3%93RIO%20COMPLETO%20-%20FASE4.pdf)

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

- [Notebook Principal - CardioIA Vision Fase 4](https://github.com/vitorguisso/fiap-2ano/blob/main/FASE%204/notebooks/CardioIA_Vision_Fase4.ipynb)

- [Abrir diretamente no Google Colab](https://colab.research.google.com/github/vitorguisso/fiap-2ano/blob/main/FASE%204/notebooks/CardioIA_Vision_Fase4.ipynb)

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


# 📊 Matrizes de Confusão e Métricas

## CNN Desenvolvida do Zero

![Matriz de Confusão CNN](assets/cnn/matriz_cnn.png)

![Relatório CNN](assets/cnn/relatorio_cnn.png)

A matriz de confusão da CNN desenvolvida do zero evidenciou limitações significativas na capacidade de classificação das imagens de eletrocardiograma.

O modelo apresentou acurácia global de aproximadamente 31%, valor próximo ao esperado em um cenário de classificação aleatória entre quatro classes. A análise da matriz demonstrou que todas as imagens do conjunto de teste foram classificadas como pertencentes à classe normal_ecg_images, independentemente de sua classe real.

Como consequência, as classes:

abnormal_heartbeat_ecg_images;
myocardial_infarction_ecg_images;
post_mi_history_ecg_images;

apresentaram precisão, recall e F1-score iguais a zero.

Por outro lado, a classe normal_ecg_images obteve recall igual a 1,00, indicando que todas as imagens dessa categoria foram corretamente identificadas. Entretanto, esse resultado não representa uma boa capacidade de classificação, pois o modelo passou a prever a mesma classe para todas as amostras avaliadas.

Esse comportamento sugere que a rede neural não conseguiu aprender características discriminantes suficientes para separar adequadamente as quatro categorias presentes no dataset.

Entre os possíveis fatores que contribuíram para esse resultado destacam-se:

Quantidade limitada de imagens disponíveis para treinamento;
Complexidade relativamente baixa da arquitetura proposta;
Dificuldade da CNN em extrair características visuais mais sofisticadas dos eletrocardiogramas;
Similaridade visual entre algumas classes do dataset;
Possível convergência para um mínimo local durante o treinamento.

Os resultados obtidos justificaram a utilização de arquiteturas mais robustas baseadas em Transfer Learning nas etapas seguintes do projeto.

---

## ResNet50 com Fine Tuning


![Matriz de Confusão ResNet50](assets/resnet50/matriz_resnet50_fine_tuning.png)

![Relatório ResNet50](assets/resnet50/relatorio_resnet50_fine_tuning.png)

A matriz de confusão da ResNet50 após o Fine Tuning demonstrou que o modelo concentrou grande parte de suas previsões na classe abnormal heartbeat ecg images.

Dos 35 exemplos dessa categoria, 34 foram classificados corretamente, resultando em recall aproximado de 97%. Entretanto, as demais classes apresentaram desempenho muito reduzido, sendo frequentemente classificadas como abnormal heartbeat ecg images.

Esse comportamento evidencia forte viés para uma única classe, prejudicando a capacidade de classificação multiclasse do modelo.

Os resultados observados corroboram a análise das curvas de treinamento, que indicaram sinais de overfitting. Embora o Fine Tuning tenha aumentado a capacidade de aprendizado da arquitetura, a ResNet50 apresentou dificuldade para generalizar adequadamente para imagens não vistas.

Os principais fatores associados a esse comportamento incluem a quantidade limitada de imagens disponíveis, a similaridade visual entre algumas categorias de ECG e a dificuldade de adaptação da arquitetura ao domínio médico.

---

## VGG16

![Matriz de Confusão VGG16](assets/vgg16/MTRAIZ_VGG16.png)

![Relatório VGG16](assets/vgg16/relatorio_VGG16.png)

A matriz de confusão da VGG16 confirmou o melhor desempenho geral entre os modelos avaliados.

Dos 35 exames pertencentes à classe abnormal heartbeat ecg images, 32 foram classificados corretamente. Já na classe myocardial infarction ecg images, 33 dos 36 exames foram corretamente identificados.

Esses resultados demonstram que a arquitetura conseguiu reconhecer de forma consistente padrões associados a anormalidades cardíacas e infarto do miocárdio.

Por outro lado, o desempenho foi mais limitado nas classes normal ecg images e post mi history ecg images. Na categoria normal ecg images, apenas 3 dos 43 exames foram classificados corretamente, enquanto a classe post mi history ecg images não apresentou classificações corretas.

Apesar dessas limitações, a VGG16 apresentou melhor equilíbrio entre aprendizado e generalização quando comparada aos demais modelos, alcançando aproximadamente 49% de acurácia no conjunto de teste.

A análise da matriz de confusão reforça os resultados observados nas curvas de treinamento e no relatório de classificação, consolidando a VGG16 como a arquitetura mais adequada para compor o protótipo CardioIA Vision.

---

## Resumo dos Resultados

| Modelo | Acurácia no Teste | Principal Comportamento Observado |
|----------|----------|----------|
| CNN Própria | 31% | Classificou praticamente todas as imagens como normal_ecg_images, apresentando indícios de underfitting. |
| ResNet50 com Fine Tuning | 25% | Demonstrou overfitting e forte viés para a classe abnormal_heartbeat_ecg_images. |
| VGG16 | 49% | Melhor equilíbrio entre aprendizado e generalização, apresentando o melhor desempenho global. |

---


## Comparação Geral das Matrizes de Confusão

A análise conjunta das matrizes de confusão reforça os resultados obtidos ao longo do desenvolvimento do projeto.

A CNN própria apresentou forte limitação na capacidade de diferenciação entre as classes, classificando todas as imagens como normal_ecg_images.

A ResNet50 com Fine Tuning apresentou evolução durante o treinamento, porém concentrou grande parte das previsões em uma única categoria, demonstrando forte viés de classificação e sinais de overfitting.

A VGG16 apresentou a melhor distribuição das previsões entre as classes avaliadas, maior estabilidade durante o treinamento e melhor capacidade de generalização, justificando sua seleção como modelo final do CardioIA Vision.

---

# 📈 Curvas de Treinamento

Com o objetivo de compreender o comportamento dos modelos durante o processo de aprendizado, foram analisadas as curvas de acurácia e perda obtidas ao longo do treinamento.

Como o modelo VGG16 apresentou o melhor desempenho geral entre as arquiteturas avaliadas, suas curvas foram comparadas com as da CNN própria, utilizada como modelo de referência para o projeto.

---

## CNN Própria

### Acurácia e Perda

![CNN](assets/cnn/grafico_acuracia_perda_cnn.png)

A análise dos gráficos demonstrou que a acurácia da CNN permaneceu próxima de 30% tanto no treinamento quanto na validação.

Esse resultado indica que o modelo apresentou dificuldade para aprender padrões suficientemente discriminativos entre as quatro classes de eletrocardiogramas.

A função de perda apresentou redução inicial nas primeiras épocas, porém rapidamente se estabilizou. Esse comportamento sugere que a rede atingiu um limite de aprendizado, sem conseguir melhorar significativamente seu desempenho ao longo do treinamento.

Não foram observados sinais claros de overfitting, pois as curvas de treinamento e validação permaneceram relativamente próximas. Entretanto, o desempenho geral foi baixo, indicando um possível caso de underfitting.

Dessa forma, a CNN própria foi importante como linha de base para comparação, mas não conseguiu capturar com eficiência a complexidade visual das imagens de ECG.

---

## VGG16

### Acurácia

![Acurácia VGG16](assets/vgg16/grafico_acuracia_VGG16.png)

### Loss

![Loss VGG16](assets/vgg16/grafico_loss_VGG16.png)

A análise das curvas de treinamento da VGG16 demonstrou comportamento mais estável em relação aos modelos anteriores.

A acurácia de treinamento apresentou crescimento gradual ao longo das épocas, enquanto a acurácia de validação, apesar de oscilar, manteve tendência geral positiva.


A função de perda também apresentou comportamento positivo, com redução consistente tanto no treinamento quanto na validação.

Esse resultado sugere que a VGG16 conseguiu aproveitar melhor os padrões visuais aprendidos previamente na ImageNet, mesmo em um problema específico de imagens médicas.

A arquitetura apresentou melhor equilíbrio entre aprendizado e generalização, tornando-se a melhor alternativa entre os modelos avaliados.

---

## Comparação entre CNN Própria e VGG16

A comparação das curvas de treinamento reforça os resultados obtidos durante a avaliação dos modelos.

Enquanto a CNN própria apresentou acurácia próxima de 30% e sinais de underfitting, a VGG16 demonstrou crescimento progressivo da acurácia e redução consistente da função de perda.

Além disso, a VGG16 apresentou maior estabilidade entre os conjuntos de treinamento e validação, indicando melhor capacidade de generalização para imagens não vistas.

Esses resultados contribuíram para a escolha da VGG16 como modelo final do CardioIA Vision, uma vez que apresentou o melhor equilíbrio entre aprendizado, estabilidade e desempenho geral.


## Conclusão da Avaliação dos Modelos

A análise conjunta das curvas de treinamento, matrizes de confusão e relatórios de classificação permitiu comparar o comportamento das três arquiteturas avaliadas.

A CNN própria demonstrou limitações na extração de características discriminativas, apresentando desempenho próximo ao de uma classificação aleatória.

A ResNet50 com Fine Tuning apresentou evolução durante o treinamento, porém sofreu com overfitting e forte concentração das previsões em uma única classe.

A VGG16 apresentou o melhor equilíbrio entre aprendizado e capacidade de generalização, alcançando aproximadamente 49% de acurácia no conjunto de teste e apresentando desempenho superior na identificação de exames associados a anormalidades cardíacas e infarto do miocárdio.

Dessa forma, a VGG16 foi selecionada como modelo final do CardioIA Vision, sendo utilizada na construção do protótipo desenvolvido nesta fase do projeto.

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

![Protótipo CardioIA Vision](assets/prototipo/prototipo_VGG16.png)

⚠️ Importante:

O protótipo possui finalidade acadêmica e demonstrativa. Seu objetivo é apresentar a aplicação prática do modelo desenvolvido, não representar a acurácia real da solução, a qual foi avaliada separadamente por meio das métricas apresentadas no projeto.

---
# 🧪 Execução do Protótipo CardioIA Vision

O protótipo do CardioIA Vision utiliza o modelo VGG16 treinado durante esta fase para realizar a classificação automática de imagens de eletrocardiograma.

O modelo selecionado foi a arquitetura VGG16, pois apresentou o melhor desempenho geral entre os modelos avaliados, alcançando aproximadamente 49% de acurácia no conjunto de teste.

---

## Executar usando modelo salvo no Google Drive

Caso o arquivo do modelo não esteja disponível diretamente no GitHub, ele pode ser carregado pelo Google Drive.

### 1. Montar o Google Drive no Colab

```python
from google.colab import drive

drive.mount('/content/drive')
```

---

### 2. Definir o caminho do modelo no Drive

Altere o caminho abaixo conforme a pasta onde o modelo estiver salvo:

```python
modelo_path = "/content/drive/MyDrive/CardioIA/models/vgg16_cardioia.keras"
```

---

### 3. Carregar o modelo

```python
from tensorflow.keras.models import load_model

modelo = load_model(modelo_path)
print("Modelo VGG16 carregado com sucesso a partir do Google Drive!")
```

---

### 4. Fazer upload da imagem de ECG

```python
from google.colab import files

uploaded = files.upload()
```

---

### 5. Executar a predição

```python
import numpy as np
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt

classes = [
    "abnormal_heartbeat_ecg_images",
    "myocardial_infarction_ecg_images",
    "normal_ecg_images",
    "post_mi_history_ecg_images"
]

nome_arquivo = list(uploaded.keys())[0]

img = image.load_img(nome_arquivo, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = img_array / 255.0
img_array = np.expand_dims(img_array, axis=0)

predicao = modelo.predict(img_array)

indice_classe = np.argmax(predicao)
classe_prevista = classes[indice_classe]
confianca = predicao[0][indice_classe] * 100

plt.imshow(img)
plt.axis("off")
plt.title(f"Classe prevista: {classe_prevista}\nConfiança: {confianca:.2f}%")
plt.show()

print("Resultado da classificação:")
print("Classe prevista:", classe_prevista)
print(f"Confiança: {confianca:.2f}%")

print("\nProbabilidades por classe:")
for classe, probabilidade in zip(classes, predicao[0]):
    print(f"{classe}: {probabilidade * 100:.2f}%")
```

---

## Observação Importante

O CardioIA Vision é um protótipo acadêmico desenvolvido para fins educacionais.

O sistema não substitui avaliação médica profissional e não deve ser utilizado como ferramenta de diagnóstico clínico real.

A proposta do projeto é demonstrar a aplicação de técnicas de Visão Computacional e Deep Learning na classificação automatizada de imagens de eletrocardiograma.
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
