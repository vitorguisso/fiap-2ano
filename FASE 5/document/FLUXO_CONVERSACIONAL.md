# Projeto do Fluxo Conversacional — CardioIA Fase 5

Documento de projeto do assistente. Escrito **antes** da implementação, para servir de
especificação da skill no IBM Watson Assistant e de base para o relatório acadêmico.

Base didática: Cap10 — *Arquitetura Cognitiva dos LLMs Modernos* (disciplina PLN, Chatbots
& Virtual Agents), seções 1.6.3 (intenções), 1.6.4 (entidades), 1.6.5 (árvore de diálogo)
e 1.6.6 (variáveis de contexto). Limites éticos: Cap01 e Cap07.

---

## 1. Escopo e papel do assistente

O CardioIA Assistente realiza **atendimento inicial (triagem informativa)** em contexto
cardiológico. Ele acolhe o paciente, organiza a informação que ele traz e o direciona ao
canal correto de atendimento.

**O que o assistente faz:**

- reconhece a intenção do paciente em linguagem natural;
- extrai informação clínica estruturada (sintoma, intensidade, duração, pressão, exame);
- identifica sinais de urgência e orienta procura imediata de atendimento;
- explica exames e hábitos de prevenção em linguagem acessível;
- organiza o encaminhamento (consulta, retorno, orientação ao médico responsável).

**O que o assistente NÃO faz** (restrição do enunciado — "respeitando limites técnicos,
éticos e conceituais" — e do Cap01/Cap07):

- não emite diagnóstico;
- não prescreve, ajusta ou suspende medicamento;
- não interpreta laudo de exame;
- não substitui avaliação médica.

Essa fronteira não é apenas um aviso no rodapé: ela é **implementada na árvore de diálogo**.
Os nós de medicamento e de exame são deliberadamente construídos para *não* responder à
pergunta clínica, e sim para redirecionar. Ver seção 6.

---

## 2. Persona e tom

- Nome: **CardioIA**
- Tratamento: "você", segunda pessoa, pt-BR
- Tom: acolhedor, direto, sem jargão. Frases curtas.
- Nunca alarmista, nunca minimizador. Em dúvida sobre gravidade, orienta procurar avaliação.
- Toda resposta de conteúdo clínico termina com encaminhamento ou disclaimer.

---

## 3. Intenções (intents)

Dez intenções, cada uma com no mínimo 10 exemplos de treino em pt-BR (o Watson recomenda
5+; usamos 10+ para reduzir confusão entre intenções vizinhas).

| # | Intent | O que captura | Risco de confusão com |
|---|--------|---------------|-----------------------|
| 1 | `saudacao` | abertura da conversa | — |
| 2 | `despedida` | encerramento, agradecimento | — |
| 3 | `capacidades_assistente` | "o que você faz?", "como funciona?" | `saudacao` |
| 4 | `emergencia_cardiaca` | quadro agudo em curso | `informar_sintoma` |
| 5 | `informar_sintoma` | relato de sintoma sem urgência aguda | `emergencia_cardiaca` |
| 6 | `duvida_pressao` | valores de pressão arterial | `informar_sintoma` |
| 7 | `duvida_medicamento` | dose, esquecimento, efeito colateral | `informar_sintoma` |
| 8 | `duvida_exame` | preparo e significado de exames | `agendar_consulta` |
| 9 | `agendar_consulta` | marcar, remarcar, cancelar | `duvida_exame` |
| 10 | `habitos_saudaveis` | prevenção, dieta, exercício | `duvida_medicamento` |

### 3.1 Decisão técnica: separar `emergencia_cardiaca` de `informar_sintoma`

Este é o par mais delicado do projeto. "Estou com dor no peito" e "estou com dor no peito
forte agora e não consigo respirar" são linguisticamente próximos, mas clinicamente
opostos em urgência.

Duas alternativas foram consideradas:

- **(A) Uma única intenção `informar_sintoma`**, com a urgência decidida depois pela
  entidade `@intensidade`. Mais simples, porém a urgência passa a depender de o paciente
  usar uma palavra da lista de sinônimos — se ele não disser "forte", o caso agudo cai no
  fluxo lento de coleta de dados.
- **(B) Duas intenções distintas**, com `emergencia_cardiaca` treinada especificamente em
  frases de quadro agudo e avaliada **antes** na árvore de diálogo.

Adotamos **(B)**. O custo é maior esforço de curadoria dos exemplos de treino e risco de
falso positivo (o assistente orienta procurar emergência quando não era necessário). Em
triagem em saúde esse é o erro preferível: falso positivo gera deslocamento desnecessário,
falso negativo pode atrasar atendimento de um infarto. A assimetria justifica a escolha.

Limitação honesta: o classificador do Watson é estatístico, treinado com poucos exemplos.
Ele **vai** errar em frases ambíguas. Por isso a orientação de emergência também aparece
como reforço no nó de sintoma com `@intensidade:forte`, criando redundância proposital.

### 3.2 Exemplos de treino (resumo)

Listagem completa no arquivo da skill (`config/watson/`). Amostra do desenho:

- `emergencia_cardiaca`: "estou com uma dor muito forte no peito agora", "sinto o peito
  apertado e o braço esquerdo formigando", "não consigo respirar e estou suando frio",
  "acho que estou tendo um infarto", "meu peito está pesado e estou com tontura forte".
- `informar_sintoma`: "ando cansado ao subir escada", "sinto o coração acelerado às vezes",
  "minhas pernas estão inchando no fim do dia", "tenho sentido palpitações", "senti uma
  tontura rápida hoje de manhã".
- `duvida_pressao`: "minha pressão deu 150 por 100", "medi 12 por 8, está bom?",
  "a pressão está alta?", "o que é pressão sistólica".
- `duvida_medicamento`: "esqueci de tomar o remédio da pressão", "posso parar a losartana",
  "esse medicamento dá tosse?", "posso dobrar a dose hoje".

---

## 4. Entidades (entities)

| Entidade | Tipo | Valores / padrão | Uso no diálogo |
|----------|------|------------------|----------------|
| `@sintoma` | sinônimos | dor_no_peito, falta_de_ar, palpitacao, tontura, inchaco, cansaco, desmaio, sudorese | identifica o que o paciente relata |
| `@intensidade` | sinônimos | leve, moderada, forte | modula a resposta e reforça urgência |
| `@duracao` | sinônimos | agora, hoje, dias, semanas, meses | contextualiza o relato |
| `@pressao_arterial` | **regex** | `\d{2,3}\s?(x\|/\|por\|por\s)\s?\d{1,3}` | captura "150/100", "12 por 8" |
| `@exame` | sinônimos | eletrocardiograma, ecocardiograma, holter, teste_ergometrico, cateterismo, exame_de_sangue | seleciona a explicação do exame |
| `@fator_risco` | sinônimos | hipertensao, diabetes, colesterol, tabagismo, sedentarismo, obesidade, historico_familiar | personaliza orientação de prevenção |
| `@sys-number` | sistema | — | idade, valores numéricos soltos |
| `@sys-date` / `@sys-time` | sistema | — | agendamento |

### 4.1 Decisão técnica: `@pressao_arterial` como entidade regex

O Cap10 (seção 1.6.4) demonstra entidades de sistema, de sinônimos e **de regex** (exemplo
`@cep`). Pressão arterial é o caso perfeito para regex: o paciente escreve de formas
imprevisíveis — "150/100", "150 por 100", "15 x 10", "12x8" — e nenhuma lista de sinônimos
cobriria isso.

Alternativa tecnicamente possível: capturar dois `@sys-number` e reconstruir o par no
backend. Rejeitada porque perde a associação entre os números (qual é a sistólica?) e joga
lógica de domínio para fora do assistente, que é justamente onde a rubrica avalia.

Limitação: a regex aceita valores clinicamente impossíveis (ex.: "999/999"). A validação
de faixa fica no backend, não na entidade.

---

## 5. Variáveis de contexto

| Variável | Origem | Função |
|----------|--------|--------|
| `$nome` | informado pelo paciente | personaliza o atendimento |
| `$sintoma_relatado` | `@sintoma` | mantém o sintoma entre turnos |
| `$intensidade` | `@intensidade` | usada na composição da orientação |
| `$falhas` | contador | dispara escalonamento após 2 falhas seguidas |
| `$urgencia` | booleano | marca a conversa como caso de urgência |

Cap10, seção 1.6.6. As variáveis são o que permite a conversa ter **memória entre turnos** —
sem elas, cada mensagem seria um atendimento novo.

⚠️ **Ponto crítico de implementação:** o exemplo de backend do Cap10 (Código-fonte 10)
chama `create_session()` a cada mensagem. Isso zera as variáveis de contexto em todo turno
e inutiliza tudo o que está nesta seção. Nossa implementação vai **reusar a sessão**,
guardando o `session_id` por usuário. Essa divergência em relação ao material é uma decisão
técnica deliberada e será documentada no relatório.

---

## 6. Árvore de diálogo

Ordem dos nós **é** a lógica: o Watson avalia de cima para baixo e para no primeiro nó cuja
condição é verdadeira. A ordenação abaixo é intencional.

```text
[1] Welcome                    conditions: welcome
      └─ apresentação + disclaimer clínico + menu de possibilidades

[2] Emergência                 conditions: #emergencia_cardiaca
      └─ orientação imediata SAMU 192 / pronto-socorro
         set $urgencia = true
         (nó de saída — não continua a coleta de dados)

[3] Sintoma forte              conditions: #informar_sintoma AND @intensidade:forte
      └─ mesma orientação de urgência (redundância proposital, ver 3.1)

[4] Sintoma identificado       conditions: #informar_sintoma && @sintoma
      ├─ set $sintoma_relatado = @sintoma
      ├─ pergunta: "há quanto tempo isso acontece?"
      └─ [4.1] Coleta - duração        conditions: true
             ├─ set $duracao
             ├─ pergunta: "leve, moderada ou forte?"
             ├─ [4.1.1] intensidade forte   conditions: @intensidade:forte
             │      └─ resumo + orientação de urgência
             └─ [4.1.2] intensidade         conditions: true
                    └─ resumo estruturado + orientação de encaminhamento

[5] Sintoma não especificado   conditions: #informar_sintoma
      ├─ pergunta: "qual sintoma você está sentindo?"
      └─ [5.1] Captura            conditions: @sintoma
             └─ next_step: jump_to [4] (selector: body)

[6] Pressão com valor          conditions: #duvida_pressao && @pressao_arterial
      └─ faixas de referência + disclaimer

[7] Pressão sem valor          conditions: #duvida_pressao
      ├─ pergunta: "qual foi o valor medido?"
      └─ [7.1] Captura            conditions: @pressao_arterial
             └─ next_step: jump_to [6] (selector: body)

[8] Dúvida de medicamento      conditions: #duvida_medicamento
      └─ NÃO responde dose. Redireciona ao médico/farmacêutico.
         Trata o caso "esqueci de tomar" com orientação genérica segura.

[9..14] Exame por tipo         conditions: #duvida_exame && @exame:<valor>
      └─ um nó por exame: ECG, ecocardiograma, Holter, teste ergométrico,
         cateterismo, exames de sangue

[15] Exame não especificado    conditions: #duvida_exame
      └─ "sobre qual exame?"

[16] Agendar consulta          conditions: #agendar_consulta
      └─ [16.1] Confirmação      conditions: true → registra preferência (simulado)

[17] Hábitos com fator         conditions: #habitos_saudaveis && @fator_risco
[18] Hábitos geral             conditions: #habitos_saudaveis
[19] Capacidades               conditions: #capacidades_assistente
[20] Saudação                  conditions: #saudacao
[21] Despedida                 conditions: #despedida
[22] Escalonamento             conditions: anything_else && $falhas > 0
      └─ reconhece o limite e oferece encaminhamento humano; zera $falhas
[23] Não entendi               conditions: anything_else
      └─ "não entendi, pode reformular?" + exemplos do que ele entende; $falhas = 1
```

### 6.0 Decisão técnica: nós filhos em vez de slots

O Watson clássico oferece **slots** (`type: "frame"` + `type: "slot"`) para coleta de
múltiplas informações. Optamos por **nós filhos com condição `true`** e variáveis de
contexto.

Razões: (a) o JSON de slots exige `event_handler` de `focus` e de `input` por slot, o que
tornaria o arquivo da skill muito mais difícil de auditar manualmente; (b) o comportamento
padrão de um nó com filhos — aguardar a entrada do usuário e avaliar os filhos antes de
voltar à raiz — já entrega a coleta em etapas; (c) a estrutura resultante é legível na
árvore do Watson por quem for corrigir o trabalho.

Limitação aceita: slots reprovam automaticamente valores inválidos e permitem preenchimento
em qualquer ordem. Com nós filhos, a ordem é fixa (sintoma → duração → intensidade). Para
uma triagem inicial guiada, ordem fixa é adequada — e até desejável.

### 6.4 Decisão de segurança: emergência interrompe a coleta

Nós filhos com condição `true` capturam qualquer entrada. Isso cria um risco concreto: se o
paciente piorar durante a coleta ("a dor no peito está insuportável agora"), a mensagem
seria consumida como se fosse a resposta à pergunta anterior, e ele receberia a próxima
pergunta do questionário em vez da orientação de urgência.

Por isso a intenção `emergencia_cardiaca` tem precedência sobre o fluxo em andamento:
detectada, ela sai da coleta e vai direto ao nó de emergência. Validado no teste D03.

### 6.1 Decisão técnica: o nó de emergência vem antes de tudo

Se `#informar_sintoma` fosse avaliado primeiro, um paciente em quadro agudo entraria na
coleta de dados ("há quanto tempo?", "é leve ou forte?") antes de qualquer orientação. Em
triagem isso é inaceitável. A posição do nó na árvore é, portanto, uma **decisão de
segurança**, não de estilo.

### 6.2 Decisão técnica: o nó de medicamento responde "não"

É contraintuitivo projetar um nó cuja função é não responder. Mas orientar dose de
anti-hipertensivo é exercício ilegal da medicina e o enunciado exige respeito aos limites
éticos. O nó reconhece a intenção (o paciente é atendido, não ignorado), explica por que
não pode responder e indica o canal correto. Reconhecer e recusar é melhor experiência do
que cair no `anything_else`.

### 6.3 Tratamento básico de exceções (requisito explícito)

O enunciado pede "tratamento básico de exceções". Implementamos em três camadas:

1. **`anything_else`** com escalonamento por contador `$falhas` — não repete a mesma
   resposta indefinidamente. O contador acumula ao longo da sessão e é zerado tanto após o
   escalonamento quanto a cada intenção reconhecida com sucesso.
2. **Slots com reprompt** — quando o paciente não fornece a informação pedida.
3. **Falha de infraestrutura no backend** — timeout ou erro da API do Watson retorna
   mensagem de indisponibilidade, sem stack trace na tela do usuário.

A camada 3 não é do Watson, é do Flask. Vale ponto no critério de integração e é o tipo de
detalhe que separa protótipo de demonstração frágil.

---

## 7. Fluxo de exemplo (caminho feliz e caminho crítico)

**Caminho de triagem normal**

```text
Paciente: oi
CardioIA: apresentação + disclaimer + o que sei fazer
Paciente: tenho sentido o coração acelerado
CardioIA: [@sintoma=palpitacao] há quanto tempo isso acontece?
Paciente: uns três dias
CardioIA: [@duracao=dias] a intensidade é leve, moderada ou forte?
Paciente: leve
CardioIA: resumo do relato + orientação de agendar avaliação + disclaimer
```

**Caminho crítico**

```text
Paciente: estou com dor forte no peito e falta de ar agora
CardioIA: [#emergencia_cardiaca] orientação imediata: SAMU 192 / pronto-socorro
          não aguarde, não dirija por conta própria
```

---

## 8. Validação

### 8.1 Executado — motor de NLU local

`python scripts/testar_nlu_local.py` — **17/17 casos conforme o esperado**.

| # | Cenário | Entrada | Resultado obtido | Status |
|---|---------|---------|------------------|--------|
| T01 | Saudação | "oi" | `#saudacao`, nó Saudação | ✅ |
| T02 | Emergência explícita | "acho que estou tendo um infarto" | `#emergencia_cardiaca`, urgência | ✅ |
| T03 | Emergência implícita | "meu peito está apertado e o braço esquerdo formigando" | `#emergencia_cardiaca`, urgência | ✅ |
| T04 | Sintoma leve | "sinto o coração acelerado às vezes" | `#informar_sintoma`, `@sintoma:palpitacao` | ✅ |
| T05 | Dor torácica intensa | "estou com dor no peito muito forte" | `#emergencia_cardiaca`, urgência | ✅ |
| T05b | Sintoma não torácico forte | "meu cansaço está forte" | nó Sintoma de forte intensidade, urgência | ✅ |
| T05c | Ambiguidade tontura forte | "minha tontura está muito forte" | `#emergencia_cardiaca` (direção segura) | ✅ |
| T06 | Pressão com barra | "minha pressão deu 150/100" | `@pressao_arterial` capturada | ✅ |
| T07 | Pressão em texto | "medi 12 por 8" | `@pressao_arterial` capturada | ✅ |
| T08 | Medicamento | "posso parar de tomar losartana" | recusa + encaminhamento | ✅ |
| T09 | Exame | "o que é holter" | nó Exame - holter | ✅ |
| T10 | Fora de escopo | "qual a previsão do tempo" | `anything_else`, 1ª falha | ✅ |
| T11 | Fora de escopo repetido | duas mensagens fora do escopo | escalonamento | ✅ |
| T14–T17 | Agendamento, hábitos, capacidades, despedida | — | nó correspondente | ✅ |

Diálogos de múltiplos turnos verificados no navegador:

| # | Diálogo | Resultado obtido | Status |
|---|---------|------------------|--------|
| D01 | sintoma → duração → intensidade | contexto preservado, resumo final correto | ✅ |
| D02 | sintoma informado só no 2º turno (jump_to body) | saltou para o nó principal | ✅ |
| D03 | emergência no meio da coleta | interrompeu a coleta, orientou urgência | ✅ |
| D04 | pressão informada só no 2º turno | saltou para o nó de faixas | ✅ |
| D05 | agendamento → preferência de período | preferência registrada | ✅ |

Regra de faixa de pressão (`triagem.py`), executada:

| Entrada | Normalizado | Classificação | Urgência |
|---------|-------------|---------------|----------|
| 110/70 | 110/70 mmHg | ótima | não |
| 128/84 | 128/84 mmHg | normal | não |
| 135/88 | 135/88 mmHg | pré-hipertensão | não |
| 150/100 | 150/100 mmHg | hipertensão (a confirmar) | não |
| 190/120 | 190/120 mmHg | muito elevada | **sim** |
| "12 por 8" | 120/80 mmHg | normal | não |
| "15x10" | 150/100 mmHg | hipertensão (a confirmar) | não |
| 999/999 | — | valor implausível | não |
| "não medi a pressão" | — | nenhuma medida reconhecida | — |

### 8.2 Executado — IBM Watson Assistant

Instância criada em 13/08/2026: watsonx Assistant, plano Lite, Dallas (us-south),
experiência clássica. Skill importada e vinculada ao assistente `CardioIA Assistente`.

A plataforma confirma o conteúdo importado: **10 Intents · 6 Entities · 29 Dialog nodes**,
idioma Brazilian Portuguese.

#### Executado na aba *Try it out* do Watson

| # | Entrada | Resultado obtido | Status |
|---|---------|------------------|--------|
| T02 | "acho que estou tendo um infarto" | `#emergencia_cardiaca`, orientação de urgência | ✅ |
| D01 | sintoma → duração → intensidade | "Registrado: inchaço, duração informada "uns três dias", intensidade "leve"" | ✅ |
| T07 | "medi 12 por 8, está bom?" | `@pressao_arterial` capturada; resposta exibe "a medida 12 por 8" | ✅ |
| T08 | "posso parar de tomar losartana" | recusa e encaminhamento | ✅ |
| T10 | "qual a previsão do tempo" | classificado como *Irrelevant*, 1ª falha | ✅ |
| T11 | segunda mensagem fora de escopo | nó de escalonamento | ✅ |

#### Executado pela API, com o backend Flask em modo `watson`

| # | Entrada | Intenção (confiança) | Entidades | Urgência |
|---|---------|----------------------|-----------|----------|
| T02 | "acho que estou tendo um infarto" | `emergencia_cardiaca` (1,00) | — | **sim** |
| D01a | "minhas pernas estão inchando no fim do dia" | `informar_sintoma` (1,00) | `@sintoma:inchaço` | não |
| D01b | "uns três dias" | — | `@duracao:dias` | não |
| D01c | "leve" | `despedida` (0,48) | `@intensidade:leve` | não |
| T07 | "medi 190 por 120" | `duvida_pressao` (0,81) | `@pressao_arterial` | **sim** |
| T08 | "posso parar de tomar losartana" | `duvida_medicamento` (1,00) | — | não |
| T09 | "o que é holter" | `duvida_exame` (1,00) | `@exame:holter` | não |
| T10 | "qual a previsão do tempo" | — | — | não |

Observação sobre D01c: o classificador atribuiu `#despedida` a "leve", com confiança baixa
(0,48). O nó filho de coleta foi avaliado antes e tratou a mensagem corretamente — o
comportamento projetado na seção 6.4. É um exemplo de por que a estrutura da árvore não
deve depender apenas da classificação de intenção.

#### Tratamento de exceções do backend — executado

| # | Cenário | Resultado obtido | Status |
|---|---------|------------------|--------|
| T18 | Mensagem vazia | HTTP 400, orientação ao usuário | ✅ |
| T19 | Mensagem acima de 500 caracteres | HTTP 400, pedido de resumo | ✅ |
| T20 | Requisição sem o campo `message` | HTTP 400 tratado | ✅ |
| T21 | Credencial inválida | `WatsonIndisponivel` capturada; detalhe técnico só no log | ✅ |
| T22 | Servidor indisponível | Interface avisa e não trava | ✅ |

Com isso, as três camadas de tratamento de exceção descritas na seção 6.3 estão validadas.

---

## 8A. Dificuldades encontradas durante a implementação

Registro das dificuldades **reais**, na ordem em que apareceram.

### D-1: saudação curta não era reconhecida

*Problema:* "oi" caía no tratamento de exceção.
*Causa:* o tokenizador descartava palavras com menos de 3 caracteres, e "oi" ficava sem
nenhum token para comparar.
*Solução:* limite mínimo reduzido para 2 caracteres, com remoção de palavras funcionais
(artigos, preposições) para compensar o ruído. "não" foi deliberadamente mantido, porque em
relato clínico ele inverte o sentido da frase.
*Resultado:* T01 passou.

### D-2: sobreposição de sinônimo entre duas entidades

*Problema:* "como reduzir o colesterol" ativava `@exame` e `@fator_risco` ao mesmo tempo.
*Causa:* "colesterol" estava cadastrado como sinônimo de `@exame:exame_de_sangue` e de
`@fator_risco:colesterol`.
*Solução:* removido de `@exame`, mantido "perfil lipídico" no lugar.
*Resultado:* apenas `@fator_risco` é ativado.

### D-3: palavras genéricas dominavam a classificação

*Problema:* "sinto palpitação forte" era classificada como emergência.
*Causa:* todas as palavras pesavam igual na comparação. A frase compartilhava "sinto" e
"forte" com um exemplo de emergência, enquanto o termo decisivo ("palpitação") tinha o mesmo
peso dos genéricos.
*Solução:* ponderação **IDF** — termos frequentes no corpus de treino pesam menos, termos
raros pesam mais. Mesmo princípio do TF-IDF.
*Resultado:* a palavra discriminante passou a dominar o cálculo.

### D-4: limiar de aceitação arbitrado

*Problema:* qual similaridade mínima aceitar como intenção reconhecida?
*Solução:* varredura sobre 35 frases rotuladas (29 no escopo, 6 fora), testando 0.34, 0.38,
0.42, 0.46 e 0.50. Em 0.34 entrava falso positivo ("qual a previsão do tempo" casava com
`#duvida_exame`, score 0.375); em 0.50 começava a rejeitar frase válida ("minha pressão deu
150/100", score 0.50).
*Resultado:* limiar 0.42, ponto mais distante das duas bordas de erro. 35/35.

### D-5: flexão verbal não reconhecida (encontrado no navegador)

*Problema:* "minhas pernas estão **inchando**" não ativava `@sintoma`.
*Causa:* o sinônimo cadastrado era "pernas inchadas". A skill declara `fuzzy_match: true`,
recurso que o Watson resolve internamente — mas o motor local fazia comparação literal.
*Solução:* comparação por radical (5 primeiras letras + sufixo livre) para palavras de 5+
caracteres, mantendo correspondência exata para palavras curtas. O limite de 5 evita falso
positivo: sem ele, "leve" casaria com "levei" e "levar". Sinônimos com a forma verbal também
foram adicionados à skill, beneficiando os dois motores.
*Resultado:* "inchando", "inchado" e "inchadas" passaram a ser reconhecidos; "levei o
resultado do exame" continua **não** ativando `@intensidade:leve`.

### D-6: dor torácica leve recebia resposta de emergência

*Problema:* "sinto uma dor leve no peito" disparava a orientação de emergência.
*Causa:* `informar_sintoma` não tinha nenhum exemplo de treino com dor torácica — por
construção, já que dor no peito foi direcionada à emergência. Consequência: qualquer menção
a peito era atraída para a intenção de emergência.
*Solução:* dois exemplos de dor torácica **explicitamente leve** adicionados a
`informar_sintoma`. A correção foi no dado de treino, não no limiar nem na árvore, porque o
problema estava na fronteira entre as duas intenções.
*Resultado:* dor leve → `#informar_sintoma`; dor forte/aguda continua em emergência.

### D-7: diálogo de múltiplos turnos quebrado no modo local (encontrado no navegador)

*Problema:* o assistente perguntava "há quanto tempo isso acontece?" e não entendia "uns três
dias" — caía no tratamento de exceção.
*Causa:* o motor local avaliava apenas nós de primeiro nível. Os nós filhos, que sustentam a
coleta em etapas, nunca eram alcançados.
*Solução:* travessia de filhos com o nó atual guardado no contexto, mais suporte a
`next_step: jump_to` com `selector: body`. Junto veio a regra de segurança da seção 6.4.
*Resultado:* D01–D05 passaram.

### D-8: SDK do Watson incompatível com a experiência clássica

*Problema:* a primeira chamada ao Watson falhou com
`TypeError: AssistantV2.create_session() missing 1 required positional argument: 'environment_id'`.

*Causa:* `pip install ibm-watson` instala a versão mais recente (11.2.0). A partir da
versão 7, o SDK passou a exigir `environment_id` e a montar a rota
`/v2/assistants/{id}/environments/{env}/sessions`, que existe apenas para assistentes da
experiência nova. Investigando na instância real:
`list_environments` responde **404** e `list_assistants` responde
**400 — "API is not supported on lite plan"**.

*Solução:* fixar `ibm-watson==6.1.0` no `requirements.txt`, versão que usa a rota
`/v2/assistants/{id}/sessions` — compatível com a experiência clássica e igual à do
material didático. A justificativa ficou registrada como comentário no próprio arquivo de
dependências, para que ninguém "atualize" a biblioteca sem entender o motivo.

*Resultado:* integração funcionando, com `origem: watson` em todas as respostas.

### D-9: variáveis de contexto invisíveis para o backend

*Problema:* uma mensagem de emergência retornava `urgencia: False`, e a interface não
exibia o destaque vermelho — apesar de a árvore de diálogo definir `$urgencia = true`.

*Causa:* a resposta do Watson Assistant v2 traz apenas `output` e `user_id`. O campo
`context` volta **vazio** por padrão. O diálogo continuava correto, porque o Watson mantém
o estado na sessão, mas o backend não enxergava nenhuma variável.

*Solução:* enviar `options.return_context = true` no corpo da mensagem.

*Resultado:* as variáveis de contexto passaram a chegar ao backend e à interface.

### D-10: `$urgencia` ficava ligada pelo resto da conversa

*Problema:* depois de corrigir D-9, **todas** as respostas passaram a vir com
`urgencia: True`, inclusive "o que é holter".

*Causa:* defeito de projeto na skill. Três nós ligavam `$urgencia = true`, mas apenas o nó
de boas-vindas a desligava. Como a variável vive na sessão, uma única mensagem de
emergência marcava a conversa inteira como urgente.

*Solução:* `urgencia = false` explicitamente nos 26 nós que não são de urgência, mantendo
`true` apenas em `node_emergencia`, `node_sintoma_forte` e `node_sintoma_int_forte`.

*Resultado:* emergência destaca; mensagens seguintes voltam ao normal. Verificado na
interface, em modo `watson`.

### D-11: entradas fora do domínio eram forçadas para dentro dele

*Problema:* investigando a pergunta "o que acontece se o usuário perguntar algo que não
prevemos?", foi executado um teste com seis frases fora do escopo. Três falharam:

| Entrada | Comportamento incorreto |
|---------|-------------------------|
| "estou com muita ansiedade e insônia" | classificada como `#emergencia_cardiaca` (0,45), com **balão vazio** |
| "meu cachorro está passando mal" | classificada como `#emergencia_cardiaca` (0,65), com **balão vazio** |
| "quebrei o braço, o que faço" | consumida como *preferência de período* do agendamento em andamento |

*Causas — três, distintas:*

1. **Balão vazio.** A desambiguação estava habilitada em `system_settings`. Com confiança
   baixa, o Watson responde com `response_type: "suggestion"` em vez de `"text"`, e o
   normalizador do backend só lia respostas de texto.
2. **Falso positivo.** O classificador sempre escolhe a intenção mais provável. Sem
   exemplos do que está **fora** do domínio, qualquer frase acaba atraída para alguma
   intenção — inclusive a de emergência, que é a mais grave possível.
3. **Mensagem consumida pelo fluxo.** Nó filho com condição `true` captura qualquer
   entrada, inclusive uma mudança de assunto.

*Soluções:*

1. `counterexamples` — 24 frases fora do domínio adicionadas à skill, agrupadas em quatro
   famílias: emergências não relacionadas à saúde, saúde fora da cardiologia, assuntos
   administrativos e temas totalmente alheios. É o mecanismo próprio do Watson para
   aprender a marcar entradas como irrelevantes.
2. Desambiguação desligada: as sugestões exigiriam uma interface de opções clicáveis, fora
   do escopo desta entrega. O tratamento de exceção já cobre o caso com mais clareza.
3. Suporte a `response_type: "suggestion"` no normalizador, mais uma **rede de segurança no
   backend**: se a resposta chegar sem texto por qualquer motivo, o paciente recebe o
   tratamento de exceção em vez de um balão em branco.

*Resultado:* as seis entradas fora do domínio passaram a cair corretamente no tratamento de
exceção, sem falso positivo e sem balão vazio. Os casos dentro do domínio permaneceram
inalterados.

*Limitação que permanece:* durante um fluxo de coleta, uma mudança brusca de assunto ainda
pode ser interpretada como resposta à pergunta anterior — com exceção de emergência, que
tem precedência (seção 6.4). É o custo da escolha por nós filhos com condição `true`.

Observação sobre D-5, D-6, D-7: as três só apareceram no teste manual no navegador, depois
de o conjunto automatizado estar passando. E D-8, D-9 e D-10 só apareceram com credencial
real — nenhuma delas seria detectável no modo de demonstração local. D-10 em especial é
instrutiva: era um defeito que existia desde o início na modelagem, mas que permanecia
invisível porque nenhum teste encadeava uma emergência com uma pergunta comum na mesma
conversa.

---

## 9. Limitações conhecidas deste projeto de fluxo

1. **Cobertura linguística limitada** — cerca de 10 exemplos por intenção capturam as
   formulações mais comuns, não a diversidade real de expressão dos pacientes.
2. **Sem histórico entre sessões** — o contexto vive na sessão do Watson (ou em memória, no
   modo local); reiniciar o servidor zera os atendimentos em andamento. Persistência
   (Cap02) não está no escopo da rubrica desta fase.
3. **Faixas de pressão são informativas** — classificação por faixa não considera idade,
   comorbidade, medicação em uso nem condições da medição.
4. **Triagem por palavra-chave não é triagem clínica** — o assistente não tem sinais
   vitais, exame físico ou histórico. Ele organiza relato, não avalia risco.
5. **`@sintoma` cobre 8 sintomas** cardiológicos frequentes, não o espectro completo.
6. **Português apenas** — a skill é criada em pt-BR.
7. **Ordem de coleta fixa** — consequência da escolha de nós filhos em vez de slots
   (seção 6.0): sintoma → duração → intensidade, sempre nessa ordem.
8. **O motor local generaliza menos que o Watson** — ele é uma rede de segurança de
   demonstração, não um substituto. Casos limítrofes como o T05c são resolvidos por
   similaridade de tokens, não por classificador treinado.

Cada limitação acima tem evolução correspondente proposta no README (seção "Trabalhos
futuros"), conforme seção 18 do `CLAUDE.md`.
