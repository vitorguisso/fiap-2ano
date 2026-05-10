# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/">
<img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width="40%">
</a>
</p>

<br>

# CardioIA – Edge Computing e Resiliência Offline em IoT para Monitoramento Cardíaco

---

## 👨‍🎓 Integrantes

- Vitor Augusto Prado Guisso
- Vinícius Pereira Santana

---

## 👩‍🏫 Professores

### Tutor(a)
- Caique Nonato da Silva Bezerra

### Coordenador(a)
- Andre Godoi Chiovato

---

# 📜 Descrição

O projeto CardioIA foi desenvolvido com o objetivo de simular um sistema inteligente de monitoramento cardíaco utilizando conceitos de Internet das Coisas (IoT), Edge Computing, comunicação em nuvem e resiliência offline.

A solução busca demonstrar, de forma prática, como dispositivos embarcados podem ser utilizados na área da saúde para captura, processamento, armazenamento temporário e transmissão de sinais vitais em tempo real.

O sistema foi desenvolvido utilizando um ESP32 no simulador Wokwi, juntamente com sensores simulados capazes de representar sinais fisiológicos de um paciente cardiológico.

O fluxo completo do sistema funciona da seguinte forma:

```txt
Sensores → ESP32 → Processamento Local → MQTT Broker → Node-RED → Dashboard
```

O ESP32 realiza a leitura dos sensores e executa o processamento local dos dados, caracterizando o conceito de Edge Computing.

Durante a execução, o sistema identifica automaticamente possíveis estados clínicos, como:

- Febre;
- Hipotermia;
- Bradicardia;
- Taquicardia;
- Ausência de batimentos;
- Alertas críticos combinados.

Após o processamento local, os dados são transmitidos via protocolo MQTT utilizando o broker público EMQX.

O Node-RED recebe as informações e atualiza um dashboard interativo em tempo real, permitindo o monitoramento contínuo do paciente.

Além disso, o projeto implementa resiliência offline. Durante falhas simuladas de conectividade, o ESP32 continua coletando os dados normalmente e realiza armazenamento temporário em cache local. Quando a conexão retorna, os dados são sincronizados automaticamente.

Essa abordagem demonstra uma arquitetura moderna de IoT aplicada à saúde digital, permitindo maior confiabilidade em cenários críticos.

---

# 🏗 Arquitetura do sistema

O projeto foi estruturado em seis etapas principais:

```txt
Sensores → ESP32 → Processamento Local → MQTT Broker → Node-RED → Dashboard
```

A figura abaixo apresenta a arquitetura implementada no simulador Wokwi.

![Arquitetura do sistema](assets/arquitetura-wokwi.png)

---

# 📄 Relatório acadêmico

O relatório completo do projeto pode ser acessado pelo link abaixo:

## 🔗 [Clique aqui para abrir o relatório da FASE 3](document/RELATORIO_FASE3_FIAP.pdf)

O documento contém:
- fundamentação teórica;
- arquitetura do sistema;
- Edge Computing;
- MQTT;
- dashboard;
- resiliência offline;
- resultados obtidos;
- testes realizados;
- conclusões do projeto.

---

# 🚀 Tecnologias utilizadas

## Hardware e simulação
- ESP32
- Sensor DHT22
- Botão para simulação cardíaca
- Wokwi Simulator

## Comunicação
- MQTT
- EMQX Broker

## Processamento e dashboard
- Node-RED
- Dashboard Node-RED

## Linguagens
- C++
- JSON

---

# 🧠 Conceitos aplicados

- Internet das Coisas (IoT)
- Edge Computing
- Resiliência Offline
- Comunicação MQTT
- Processamento local
- Monitoramento em tempo real
- Dashboards interativos
- Sistemas embarcados
- Saúde digital

---

# 📊 Funcionalidades implementadas

## ✅ Captura de sinais vitais
- Temperatura corporal;
- Umidade;
- Batimentos cardíacos simulados.

## ✅ Processamento local

O ESP32 realiza:
- Leitura dos sensores;
- Processamento dos dados;
- Identificação de alertas clínicos;
- Controle de sincronização offline.

## ✅ Alertas clínicos automáticos

O sistema detecta:
- Paciente normal;
- Febre;
- Hipotermia;
- Bradicardia;
- Taquicardia;
- Sem batimentos;
- Combinações críticas.

## ✅ Dashboard em tempo real

O dashboard exibe:
- BPM em gráfico temporal;
- Temperatura corporal;
- Alertas visuais;
- Status do paciente.

## ✅ Resiliência offline

Quando ocorre perda de conectividade:
- Os dados continuam sendo coletados;
- Os dados são armazenados localmente;
- Nenhuma informação é perdida;
- O sistema sincroniza automaticamente após reconexão.

---

# ▶️ Projeto no Wokwi

O projeto completo pode ser acessado pelo link abaixo:

https://wokwi.com/projects/462873493787646977

Para executar a simulação:

1. Abrir o projeto;
2. Clicar em `Start Simulation`;
3. Acompanhar os dados no Serial Monitor;
4. Executar o Node-RED localmente para visualizar o dashboard.

---

# 📊 Dashboard em funcionamento

## ✅ Paciente normal

![Dashboard normal](assets/dashboard-normal.png)

---

## 🚨 Febre + Taquicardia

![Dashboard febre e taquicardia](assets/dashboard-febre-taquicardia.png)

---

## 🚨 Hipotermia + Bradicardia

![Dashboard hipotermia e bradicardia](assets/dashboard-hipotermia-bradicardia.png)

---

# 🧪 Resiliência offline

O projeto implementa resiliência offline utilizando armazenamento temporário em cache local no ESP32.

Durante falhas de conectividade:
- os dados continuam sendo coletados;
- o sistema continua funcionando;
- os dados são armazenados localmente;
- nenhuma leitura é perdida.

Após o retorno da conexão:
- o ESP32 sincroniza automaticamente os dados armazenados.

A figura abaixo demonstra o funcionamento da sincronização offline.

![Resiliência offline](assets/resiliencia-offline.png)

---

# 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

## 📂 .github
Arquivos de configuração específicos do GitHub.

## 📂 assets
Imagens utilizadas no projeto:
- arquitetura do sistema;
- dashboard;
- evidências dos testes;
- resiliência offline;
- logo FIAP.

## 📂 config
Arquivos auxiliares de configuração do projeto:
- flows.json do Node-RED.

## 📂 document
Documentação acadêmica:
- relatório da fase;
- documentação complementar.

## 📂 scripts
Scripts auxiliares do projeto.

## 📂 src
Código-fonte do projeto.

### 📂 src/esp32
Arquivos do simulador Wokwi:
- sketch.ino
- diagram.json
- libraries.txt

## 📄 README.md
Arquivo principal de documentação do projeto.

---

# 🔧 Como executar o projeto

## 📌 Pré-requisitos

Instalar:
- Node.js;
- Node-RED;
- Navegador web;
- Conta no Wokwi.

---

# ▶️ Executando o ESP32 no Wokwi

## 1. Abrir o simulador

Acesse:

```txt
https://wokwi.com/projects/462873493787646977
```

---

## 2. Executar a simulação

Clique em:

```txt
Start Simulation
```

O ESP32 iniciará:
- conexão Wi-Fi;
- conexão MQTT;
- envio dos dados.

---

# ▶️ Executando o Node-RED

## 1. Instalar o Node-RED

No terminal:

```bash
npm install -g --unsafe-perm node-red
```

---

## 2. Iniciar o Node-RED

No terminal:

```bash
node-red
```

O terminal exibirá:

```txt
Server now running at http://127.0.0.1:1880/
```

---

## 3. Abrir o Node-RED

No navegador:

```txt
http://localhost:1880
```

---

# 🔄 Importando o fluxo do Node-RED

## 1. Abrir o menu

No canto superior direito:

```txt
Menu → Import
```

---

## 2. Selecionar o arquivo

Importar:

```txt
config/flows.json
```

---

## 3. Implantar o fluxo

Clique em:

```txt
Deploy
```

---

# 📈 Acessando o dashboard

Após executar o fluxo, abrir no navegador:

```txt
http://localhost:1880/ui
```

---

# ⚠️ IMPORTANTE SOBRE O DASHBOARD

O dashboard do projeto funciona localmente utilizando Node-RED.

Por esse motivo, o avaliador precisa:

1. Executar o Node-RED localmente;
2. Importar o fluxo do projeto;
3. Executar a simulação do Wokwi;
4. Acessar o dashboard pelo navegador.

O endereço:

```txt
http://localhost:1880/ui
```

funciona apenas no computador onde o Node-RED está sendo executado.

---

# 📂 Arquivos importantes do projeto

## 🔧 Código ESP32

Localização:

```txt
src/esp32/
```

Arquivos:
- sketch.ino
- diagram.json
- libraries.txt

---

## 🔄 Fluxo do Node-RED

Localização:

```txt
config/flows.json
```

O arquivo contém:
- dashboard;
- MQTT;
- gráficos;
- gauge;
- alertas clínicos;
- integração em tempo real.

---

## 📄 Relatório acadêmico

Localização:

```txt
document/RELATORIO_FASE3_FIAP.pdf
```

O relatório contém:
- fundamentação teórica;
- arquitetura do sistema;
- Edge Computing;
- MQTT;
- resultados;
- testes;
- resiliência offline.

---

# 📈 Resultados obtidos

O sistema apresentou:
- funcionamento estável;
- comunicação MQTT em tempo real;
- dashboard funcional;
- detecção automática de alertas clínicos;
- sincronização automática;
- resiliência offline.

Durante os testes, foram simulados cenários como:
- febre;
- hipotermia;
- taquicardia;
- bradicardia;
- ausência de batimentos;
- perda de conectividade.

O sistema continuou funcionando normalmente mesmo durante desconexões simuladas.

---

# 🔮 Trabalhos futuros

Como evolução futura, pretende-se:
- integrar sensores biomédicos reais;
- utilizar SPIFFS;
- hospedar o dashboard em nuvem;
- implementar banco de dados;
- integrar Inteligência Artificial preditiva;
- gerar alertas automáticos para profissionais da saúde.

---

# 🗃 Histórico de lançamentos

## 0.3.0 - Maio/2026
- Implementação da resiliência offline;
- Cache local no ESP32;
- Sincronização automática;
- Dashboard Node-RED.

## 0.2.0 - Maio/2026
- Implementação MQTT;
- Dashboard em tempo real;
- Processamento local.

## 0.1.0 - Maio/2026
- Estrutura inicial do projeto;
- Simulação ESP32;
- Captura de sinais vitais.

---

# 📚 Referências

WOKWI. Wokwi Simulator. Disponível em: <https://wokwi.com>. Acesso em: 12 maio 2026.

NODE-RED. Flow-based programming for the Internet of Things. Disponível em: <https://nodered.org>. Acesso em: 12 maio 2026.

EMQX. EMQX MQTT Broker Platform. Disponível em: <https://www.emqx.com>. Acesso em: 12 maio 2026.

IBM. MQTT Protocol Overview. Disponível em: <https://www.ibm.com/docs/en/ibm-mq/9.3?topic=overview-mqtt>. Acesso em: 12 maio 2026.

ESPRESSIF SYSTEMS. ESP32 Documentation. Disponível em: <https://docs.espressif.com/projects/esp-idf/en/latest/esp32/>. Acesso em: 12 maio 2026.

---

# 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1">
<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1">

Este projeto está licenciado sob Creative Commons Attribution 4.0 International.
