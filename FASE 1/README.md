# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width="40%" height="40%"></a>
</p>

<br>

# CardioIA – Fase 1: Batimentos de Dados

## Nome do grupo

**CardioIA**

## 👨‍🎓 Integrantes

- [Vinícius Pereira Santana]()
- [Vitor Augusto Prado Guisso]()

## 👩‍🏫 Professores

### Tutor(a)

- [Caique Nonato da Silva Bezerra](.)

### Coordenador(a)

- [Andre Godoi Chiovato](https://www.linkedin.com/company/inova-fusca)

## 📜 Descrição

O projeto **CardioIA** foi proposto como uma jornada acadêmica voltada à integração entre tecnologia, ciência de dados e saúde, com o objetivo de simular um ecossistema moderno de cardiologia inteligente. Ao longo das sete fases previstas no curso, a proposta envolve a construção de soluções baseadas em Inteligência Artificial para apoiar processos como triagem, monitoramento, análise de exames, assistência remota e previsão de eventos cardiovasculares.

Nesta **Fase 1 – Batimentos de Dados**, o foco do grupo está na construção da base de dados inicial do projeto. Essa etapa é fundamental, pois os dados organizados aqui servirão como insumo para as próximas fases, nas quais serão desenvolvidos modelos de Machine Learning, aplicações de Processamento de Linguagem Natural, Visão Computacional e outras soluções computacionais voltadas à saúde cardiovascular.

A atividade foi dividida em três frentes principais. A primeira consiste na organização de **dados numéricos clínicos**, reunindo informações relevantes para a análise de risco cardiovascular, como idade, sexo, tipo de dor no peito, pressão arterial, colesterol, frequência cardíaca e diagnóstico de doença cardíaca. Para isso, foi utilizado como base o **UCI Heart Disease Dataset**, uma das bases mais tradicionais da área, complementada por um dataset sintético e por dados adicionais de sinais cardíacos oriundos do **MIT-BIH Arrhythmia Database**.

A segunda frente envolve os **dados textuais**, utilizados para explorar possibilidades de aplicação de técnicas de **Processamento de Linguagem Natural (NLP)**. Foram selecionados textos científicos relacionados a doenças cardiovasculares, fatores de risco, prevenção e saúde pública. Esses materiais poderão, futuramente, ser utilizados em tarefas como extração de entidades médicas, classificação de tópicos e mineração de fatores de risco.

A terceira frente contempla os **dados visuais**, com foco em **imagens de eletrocardiogramas (ECG)**. Foram reunidos datasets públicos contendo imagens médicas que poderão ser analisadas por algoritmos de Visão Computacional, permitindo, em etapas futuras, a identificação de padrões, reconhecimento de anomalias e classificação automática de batimentos cardíacos.

Além da organização técnica dos dados, esta fase também considera aspectos importantes de **governança, ética e responsabilidade no uso de dados em saúde**, priorizando bases públicas, uso acadêmico e ausência de identificação pessoal dos pacientes.

Assim, esta entrega representa a fundação do projeto CardioIA, estabelecendo uma base sólida e bem documentada para o desenvolvimento progressivo de soluções inteligentes aplicadas à cardiologia ao longo do curso.

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- **.github**: nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.

- **assets**: aqui estão os arquivos relacionados a elementos não estruturados deste repositório, como imagens, logotipos e materiais visuais de apoio.

- **config**: pasta reservada para arquivos de configuração utilizados em etapas futuras do projeto.

- **document**: aqui estão todos os documentos do projeto. Nesta fase, foram organizados os materiais textuais utilizados nas análises de NLP, além de documentos complementares na subpasta `other`.

- **scripts**: pasta destinada a scripts auxiliares para tarefas específicas do projeto, como limpeza de dados, conversões de formatos e automatizações futuras.

- **src**: diretório reservado para o código-fonte que será desenvolvido ao longo das próximas fases do CardioIA.

- **README.md**: arquivo que serve como guia e explicação geral sobre o projeto.


## 📊 Organização dos dados da Fase 1

Nesta fase, os dados do projeto foram organizados em três categorias principais: **numéricos**, **textuais** e **visuais**.

---

## Parte 1 – Dados Numéricos

O dataset principal utilizado foi obtido a partir do **UCI Machine Learning Repository**, por meio da base **UCI Heart Disease Dataset**, uma das mais tradicionais em pesquisas acadêmicas na área de Ciência de Dados e Inteligência Artificial aplicada à saúde.

Essa base reúne dados clínicos reais de pacientes avaliados em hospitais participantes de estudos sobre doenças cardiovasculares. Os dados foram coletados em diferentes centros médicos, incluindo:

- Cleveland Clinic Foundation (EUA)
- Hungarian Institute of Cardiology (Hungria)
- University Hospital Zurich (Suíça)
- VA Medical Center Long Beach (EUA)

Para este projeto, foi utilizada uma base com **920 registros de pacientes**, contendo variáveis clínicas relevantes para análise e aplicação em modelos de Inteligência Artificial voltados à saúde cardiovascular.

O dataset utilizado neste projeto pode ser acessado no repositório:

📊 [heart_disease_uci.csv](https://github.com/vitorguisso/fiap-2ano/blob/main/FASE%201/assets/datasets/heart_disease_uci.csv)

## Parte 1.2– Geração de Dataset Sintético (Google Colab)

Para complementar a base de dados do projeto, foi desenvolvido um notebook em **Python utilizando o Google Colab** com o objetivo de gerar um dataset sintético baseado na distribuição estatística da base real de pacientes cardiológicos.

### Notebook utilizado

O notebook completo pode ser acessado no link abaixo:

🔗 [Notebook Google Colab – Geração do Dataset Sintético](https://colab.research.google.com/drive/19iOr93Yp4Nm8TdAb1WNDxTdbSLkygErS)

### Etapas realizadas no notebook


### 1.2.1. Leitura do dataset original

Inicialmente foi carregado o dataset **UCI Heart Disease Dataset**, contendo **920 pacientes** e **16 variáveis clínicas**, incluindo informações como idade, pressão arterial, colesterol, frequência cardíaca máxima, entre outras.

📊 Dataset original:  
[heart_disease_uci.csv](https://github.com/vitorguisso/fiap-2ano/blob/main/FASE%201/assets/datasets/heart_disease_uci.csv)

### 1.2.2. Verificação da estrutura dos dados

Foram realizadas análises exploratórias iniciais para compreender a estrutura da base de dados, incluindo:

- visualização das primeiras linhas da base
- verificação do número de registros e variáveis
- inspeção dos nomes das colunas
- identificação de valores ausentes

Para essa etapa foram utilizadas principalmente as bibliotecas:

- **Pandas**
- **NumPy**

### 1.2.3. Simulação de novos pacientes

A partir da distribuição estatística das variáveis da base original, foram gerados **1000 pacientes simulados**, preservando características estatísticas semelhantes às da base real.

Essa simulação permite:

- ampliar o volume de dados disponível
- testar algoritmos de Inteligência Artificial
- realizar experimentos futuros de modelagem preditiva

### 1.2.4. Exportação do dataset sintético

Após a geração dos dados simulados, foi criado o arquivo:

Dataset sintético:  
📊 [heart_disease_simulado.csv](https://github.com/vitorguisso/fiap-2ano/blob/main/FASE%201/assets/datasets/heart_disease_simulado.csv)

Esse dataset será utilizado nas próximas fases do projeto para testes de modelos de aprendizado de máquina e análises preditivas.


### Variáveis clínicas utilizadas

| Variável | Descrição |
|---|---|
| `age` | Idade do paciente |
| `sex` | Sexo do paciente |
| `cp` | Tipo de dor no peito |
| `trestbps` | Pressão arterial em repouso |
| `chol` | Nível de colesterol no sangue |
| `fbs` | Nível de glicose em jejum |
| `restecg` | Resultado do eletrocardiograma em repouso |
| `thalch` | Frequência cardíaca máxima atingida |
| `exang` | Presença de angina induzida por exercício |
| `oldpeak` | Depressão do segmento ST no ECG |
| `slope` | Inclinação do segmento ST |
| `ca` | Número de artérias coronárias principais afetadas |
| `thal` | Resultado do teste de talassemia |
| `num` | Diagnóstico de doença cardíaca |

### Variáveis mais relevantes do ponto de vista clínico

As variáveis mais importantes para um projeto de IA voltado à saúde cardiovascular são:

- **Idade (`age`)**: importante fator de risco para doenças cardiovasculares.
- **Pressão arterial (`trestbps`)**: relacionada à hipertensão e a complicações cardiovasculares.
- **Colesterol (`chol`)**: associado à formação de placas nas artérias.
- **Tipo de dor no peito (`cp`)**: forte indicador clínico de isquemia e doença arterial coronariana.
- **Frequência cardíaca máxima (`thalch`)**: indicador da capacidade cardiovascular do paciente.
- **Angina induzida por exercício (`exang`)**: sugere possível insuficiência de oxigenação cardíaca durante esforço.
- **Número de artérias afetadas (`ca`)**: variável fortemente relacionada à gravidade da doença coronariana.
- **Diagnóstico de doença cardíaca (`num`)**: variável alvo para treinamento de modelos de Machine Learning.

### Dataset complementar de sinais cardíacos

Além do dataset clínico, também foi incorporado ao projeto um conjunto adicional de dados provenientes do **MIT-BIH Arrhythmia Database**, um dos bancos de dados mais tradicionais da literatura científica para estudo de eletrocardiogramas e arritmias.

**Fonte do dataset:**  
🔗 [MIT-BIH Arrhythmia Database](https://drive.google.com/drive/u/1/folders/1T4ynNIcFw0yh5qoqNrQTstz6ugt1r8yn)

**Autores:**  
George B. Moody e Roger G. Mark

**Instituições:**  
Massachusetts Institute of Technology (MIT) e Beth Israel Hospital (Boston, EUA)

**Publicação de referência:**  
Moody, G. B., & Mark, R. G. (2001).  
*The impact of the MIT-BIH Arrhythmia Database.*  
IEEE Engineering in Medicine and Biology Magazine, 20(3), 45–50.

**Disponível em:**  
https://physionet.org/content/mitdb/1.0.0/

Esse banco contém:

- 48 registros de ECG
- cerca de 30 minutos por registro
- sinais de 47 pacientes
- 2 canais de ECG por gravação
- digitalização a 360 amostras por segundo
- aproximadamente 110.000 anotações clínicas de batimentos cardíacos

Esses dados foram processados e organizados em formato `.csv`, possibilitando sua integração com o dataset principal e futuras análises envolvendo detecção de arritmias, classificação de batimentos e correlação entre dados clínicos e sinais cardíacos.

### Relevância para Inteligência Artificial na Saúde

A partir desses dados, é possível treinar modelos capazes de:

- identificar padrões clínicos associados a doenças cardíacas
- auxiliar na triagem de pacientes
- apoiar profissionais de saúde na tomada de decisão
- prever o risco de doenças cardiovasculares
- relacionar variáveis clínicas com padrões de sinais cardíacos

---

## Parte 2 – Dados Textuais (NLP)

Para a etapa de **Processamento de Linguagem Natural (NLP)**, foram selecionados textos científicos relacionados às doenças cardiovasculares, fatores de risco e prevenção em saúde pública. Esses documentos foram armazenados na pasta `document` do repositório e servirão como base para experimentos de análise textual utilizando técnicas de Inteligência Artificial.

### Arquivos principais utilizados

- [Associação Individual e Simultânea entre Fatores de Risco para Doença Cardiovascular e Hábitos Inadequados do Estilo de Vida](https://github.com/vitorguisso/fiap-2ano/blob/main/FASE%201/document/Associa%C3%A7%C3%A3o%20Individual%20e%20Simult%C3%A2nea%20entre%20Fatores%20de%20Risco%20para.pdf)

- [Fatores associados às doenças cardiovasculares na população adulta brasileira](https://github.com/vitorguisso/fiap-2ano/blob/main/FASE%201/document/Fatores%20associados%20%C3%A0s%20doen%C3%A7as%20cardiovasculares.pdf)

- [Nutrição e doenças cardiovasculares: os marcadores de risco em adultos](https://github.com/vitorguisso/fiap-2ano/blob/main/FASE%201/document/Nutri%C3%A7%C3%A3o%20e%20doen%C3%A7as%20cardiovasculares%20os.pdf)

Esses textos abordam temas como:

- fatores de risco cardiovasculares  
- influência do estilo de vida na saúde cardíaca  
- fatores nutricionais associados às doenças cardiovasculares  
- determinantes epidemiológicos da saúde da população brasileira  

### Potencial de aplicação de NLP

Os textos selecionados podem ser explorados por técnicas de NLP como:

- **Extração de entidades médicas**, identificando termos como hipertensão, diabetes, obesidade, colesterol elevado, tabagismo e sedentarismo  
- **Classificação de tópicos**, permitindo separar documentos por temas como prevenção cardiovascular, fatores de risco, nutrição e saúde pública  
- **Mineração de fatores de risco**, identificando relações entre hábitos e doenças, como sedentarismo, dieta inadequada e tabagismo  

### Relevância para o projeto

A utilização desses textos permite demonstrar como sistemas de IA podem:

- analisar conteúdos médicos e epidemiológicos automaticamente  
- identificar padrões de risco em saúde  
- apoiar a tomada de decisão clínica  
- estruturar conhecimento a partir de grandes volumes de informação textual  

Além dos textos principais, o repositório também conta com materiais complementares disponíveis na pasta:

📂 [Materiais complementares](https://github.com/vitorguisso/fiap-2ano/tree/main/FASE%201/document/outros)

Esses materiais poderão ser utilizados em fases futuras do projeto para ampliar a base textual utilizada nas análises de NLP.

---

## Parte 3 – Dados Visuais (Visão Computacional)

Para a etapa de **Visão Computacional**, foram utilizados dois datasets públicos contendo imagens de eletrocardiogramas (ECG). Esses datasets permitem analisar visualmente padrões da atividade elétrica do coração e são amplamente utilizados em pesquisas de Inteligência Artificial aplicada à cardiologia.

As imagens de ECG representam graficamente os sinais elétricos do coração ao longo do tempo, permitindo identificar alterações no ritmo cardíaco, presença de arritmias e outros sinais associados a doenças cardiovasculares.

### Dataset 1 – ECG Images Dataset (MIT-BIH Arrhythmia)

O primeiro conjunto de imagens utilizado foi derivado do **MIT-BIH Arrhythmia Database**, com sinais processados e convertidos em imagens com resolução de **256x256 pixels**.

#### Características do dataset

- Total de imagens: 109.445
- Número de classes: 5
- Resolução: 256x256 pixels
- Origem dos dados: MIT-BIH Arrhythmia Database (PhysioNet)

#### Classes presentes no dataset

| Classe | Descrição | Número de imagens |
|---|---|---:|
| `N` | Batimento normal | 90.589 |
| `S` | Batimento ectópico supraventricular | 2.779 |
| `V` | Batimento ectópico ventricular | 7.236 |
| `F` | Batimento de fusão | 803 |
| `Q` | Batimento desconhecido | 8.038 |

### Dataset 2 – ECG Images Dataset of Cardiac Patients

O segundo dataset utilizado contém imagens reais de eletrocardiogramas de pacientes cardíacos, desenvolvido sob supervisão do **Chaudhry Pervaiz Elahi Institute of Cardiology**, em Multan, Paquistão.

#### Características do dataset

- Total aproximado de imagens: 11.148
- Formato: ECG em formato gráfico
- Licença: CC BY 4.0
- Instituição: University of Management and Technology

#### Categorias presentes

| Categoria | Quantidade de imagens |
|---|---:|
| ECG de pacientes com infarto do miocárdio | 2.880 |
| ECG de pacientes com batimento cardíaco anormal | 2.796 |
| ECG de pacientes com histórico de infarto | 2.064 |
| ECG de indivíduos saudáveis | 3.408 |

### Importância para Visão Computacional

As imagens de ECG podem ser analisadas por algoritmos de Visão Computacional para:

- detecção de bordas e padrões no traçado do ECG
- extração de características do sinal cardíaco
- classificação automática de batimentos cardíacos
- identificação de arritmias e outras anomalias
- reconhecimento de padrões associados a doenças cardiovasculares

Modelos de aprendizado profundo, especialmente **Redes Neurais Convolucionais (CNNs)**, são frequentemente utilizados nesse tipo de aplicação.

### Relevância para Inteligência Artificial na Saúde

A análise automatizada de exames cardiológicos é uma das aplicações mais importantes da IA na saúde. Sistemas baseados em Inteligência Artificial podem auxiliar profissionais médicos na identificação de padrões que indicam doenças cardíacas, contribuindo para diagnósticos mais rápidos e precisos.

---

## 🔗 Links públicos dos dados

- [ECG Images Dataset (MIT-BIH Arrhythmia)](https://drive.google.com/drive/u/1/folders/1G-PjyrZvAJim7DEcohYbYdltkQ8n6B3q)
- [ECG Images Dataset of Cardiac Patients (Chaudhry Pervaiz Elahi Institute of Cardiology)](https://drive.google.com/drive/u/1/folders/1MTJs3u_KbfJBQ__6lsuWFyLr-z-DRuGD) 

### Dados numéricos

- Dataset clínico principal: [Inserir link público]
- Dataset sintético complementar: [Inserir link público]
- Dataset complementar de sinais cardíacos: [Inserir link público]

### Dados textuais

- Pasta com textos científicos: [Inserir link público]

### Dados visuais

- Pasta com imagens de ECG: [Inserir link público]

---

## 🔧 Como executar o código

Nesta fase inicial do projeto, o foco está na **organização e documentação dos dados**, portanto não há, até o momento, uma aplicação executável completa. Ainda assim, o repositório já foi estruturado para permitir a continuidade do desenvolvimento nas próximas fases.

### Pré-requisitos

Para visualizar, manipular e explorar os dados do projeto, recomenda-se o uso das seguintes ferramentas:

- Git para clonar o repositório
- Visual Studio Code, PyCharm ou outra IDE de preferência
- Python 3.10+ para futuras análises e scripts
- Jupyter Notebook ou Google Colab para exploração dos datasets
- bibliotecas como `pandas`, `numpy`, `matplotlib`, `seaborn` e `scikit-learn` para etapas futuras

# 🗃 Histórico de Lançamentos

1.0.0 – 10/03/2026
- Estruturação inicial do repositório
- Organização da documentação da Fase 1
- Inclusão dos datasets numéricos, textuais e visuais
- Definição da base inicial do projeto CardioIA

---

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
