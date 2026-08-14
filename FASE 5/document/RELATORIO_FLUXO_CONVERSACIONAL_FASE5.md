# Relatório do Fluxo Conversacional — CardioIA Fase 5

**FIAP — Graduação em Inteligência Artificial — 2º ano**
**Projeto:** CardioIA Assistente — Assistente Cardiológico Inteligente e Conversacional
**Disciplina:** Processamento de Linguagem Natural, Chatbots & Virtual Agents

**Integrantes:** Vitor Augusto Prado Guisso (RM562317) · Vinícius Pereira Santana (RM564940) · Isaac Maciel (RM98222)

---

## 1. Objetivo e escopo

O assistente realiza **triagem informativa** em contexto cardiológico: reconhece a intenção do paciente em linguagem natural, extrai informação clínica estruturada, identifica sinais de urgência e o direciona ao canal correto de atendimento.

O escopo exclui deliberadamente diagnóstico, interpretação de laudo e orientação de medicamento. Essa fronteira não é apenas um aviso na interface — ela está implementada na árvore de diálogo, conforme detalhado na seção 5.

## 2. Estrutura do fluxo

A modelagem foi feita no **IBM Watson Assistant** (experiência clássica, pt-BR) e é composta por 10 intenções com 111 exemplos de treino, 6 entidades e 29 nós de diálogo.

**Intenções:** `saudacao`, `despedida`, `capacidades_assistente`, `emergencia_cardiaca`, `informar_sintoma`, `duvida_pressao`, `duvida_medicamento`, `duvida_exame`, `agendar_consulta` e `habitos_saudaveis`.

**Entidades:** `@sintoma` (8 valores), `@intensidade`, `@duracao`, `@exame` (6 valores), `@fator_risco` (7 valores) e `@pressao_arterial`. Esta última é uma entidade **de expressão regular**, e não de sinônimos: o paciente escreve a medida de formas imprevisíveis — `150/100`, `150 por 100`, `15x10` — e nenhuma lista de sinônimos cobriria essa variação. A alternativa de capturar dois `@sys-number` foi descartada porque perde a associação entre os valores, impossibilitando saber qual deles é a pressão sistólica.

## 3. Funcionamento do diálogo

O Watson Assistant avalia as condições dos nós de cima para baixo e responde pelo primeiro cuja condição é satisfeita. A **ordem dos nós é, portanto, parte da lógica** — e não uma questão de organização visual.

A sequência adotada é: boas-vindas, emergência, sintoma de forte intensidade, sintoma identificado, sintoma não especificado, pressão arterial, medicamento, exames, agendamento, hábitos, capacidades, saudação, despedida e, por último, o tratamento de exceção.

**Diálogo de múltiplas etapas.** O relato de sintoma não se resolve em um único turno. Ao identificar `@sintoma`, o assistente armazena o valor na variável de contexto `$sintoma_relatado` e pergunta a duração; o nó filho registra `$duracao` e pergunta a intensidade; o nó seguinte registra `$intensidade` e devolve um **resumo estruturado do relato**, que o paciente pode apresentar ao profissional que o atender.

Quando o paciente informa a intenção sem o dado — *"queria relatar um sintoma"* ou *"minha pressão está alta?"* —, o assistente pergunta o que falta e, ao receber a informação, executa um salto (`jump_to` com `selector: body`) para o nó principal correspondente. Isso evita duplicar o mesmo texto de resposta em dois pontos da skill.

**Variáveis de contexto utilizadas:** `$sintoma_relatado`, `$duracao`, `$intensidade`, `$urgencia` e `$falhas`. São elas que dão memória à conversa entre turnos.

## 4. Tratamento de exceções

Foram implementadas três camadas:

1. **Não compreensão com escalonamento.** O contador `$falhas` evita que o assistente repita indefinidamente a mesma resposta. Na primeira falha ele pede reformulação e exemplifica o que entende; na segunda, reconhece o próprio limite e oferece encaminhamento a atendimento humano.
2. **Repergunta nos fluxos de coleta**, quando o dado solicitado não é fornecido.
3. **Falha de infraestrutura**, tratada no backend: indisponibilidade do serviço ou credencial inválida retornam mensagem compreensível ao paciente, sem exposição de erro técnico na interface.

## 5. Decisões técnicas relevantes

**Emergência como intenção separada, avaliada primeiro.** As frases *"estou com dor no peito"* e *"estou com dor no peito forte agora e não consigo respirar"* são linguisticamente próximas e clinicamente opostas. Uma alternativa seria manter uma única intenção e decidir a urgência pela entidade `@intensidade` — mas assim a identificação do quadro grave passaria a depender de o paciente empregar uma palavra específica da lista de sinônimos. Optou-se por duas intenções distintas, com a de emergência posicionada no topo da árvore. O custo é o risco de falso positivo, no qual o assistente orienta procurar emergência sem necessidade. Em triagem em saúde, esse é o erro preferível: um falso positivo gera deslocamento desnecessário, enquanto um falso negativo pode atrasar o atendimento de um infarto.

**Emergência interrompe a coleta em andamento.** Os nós de coleta respondem a qualquer entrada, o que cria um risco concreto: se o paciente piorar no meio do questionário — *"a dor está insuportável agora"* —, a mensagem seria consumida como resposta à pergunta anterior. A intenção de emergência tem, por isso, precedência sobre qualquer fluxo em curso.

**O nó de medicamento reconhece e recusa.** É contraintuitivo projetar um nó cuja função é não responder à pergunta feita, porém orientar dose de medicamento cardiovascular extrapola o papel de um assistente virtual. O nó identifica a intenção — o paciente é atendido, e não ignorado —, explica por que não pode responder e indica o canal correto. Isso é preferível a deixar a mensagem cair no tratamento de exceção.

**Nós filhos em lugar de slots.** O recurso de slots do Watson permitiria coleta em qualquer ordem e validação automática. Optou-se por nós filhos com variáveis de contexto, cuja estrutura é mais legível na árvore de diálogo. A limitação aceita é a ordem fixa de coleta: sintoma, duração e intensidade — adequada a uma triagem inicial guiada.

**Reaproveitamento da sessão na integração.** O exemplo de integração do material didático cria uma nova sessão a cada mensagem. Como as variáveis de contexto pertencem à sessão, essa abordagem as descartaria a cada turno e inviabilizaria todo o fluxo descrito na seção 3 — o assistente perguntaria a duração e, na mensagem seguinte, já teria esquecido o sintoma. Nesta implementação a sessão é criada uma vez e reaproveitada; quando expira por inatividade, o cliente a recria de forma transparente.

**Regra de faixa de pressão fora da árvore.** A entidade de regex reconhece o formato da medida, mas não avalia plausibilidade nem faixa clínica. Essa regra foi implementada no backend, onde permanece isolada e testável, evitando criar um nó de diálogo por faixa de valor.

## 6. Validação

O plano de testes cobre 17 casos, executados sobre o fluxo: saudação, emergência explícita e implícita, sintoma leve, sintoma intenso, ambiguidade de intensidade, pressão em dois formatos, medicamento, exame, mensagem fora de escopo, escalonamento de falha, agendamento, hábitos, capacidades e despedida. **Resultado: 17 de 17 conformes.**

Foram verificados também cinco diálogos de múltiplos turnos, entre eles a coleta completa de sintoma, os dois saltos entre nós e a interrupção da coleta por emergência. A regra de faixa de pressão foi validada em nove formatos de entrada, incluindo a escala coloquial (*"12 por 8"* → 120/80 mmHg) e valor implausível.

A skill foi importada em uma instância real do watsonx Assistant (plano Lite, Dallas, experiência clássica), que confirma o conteúdo: **10 intenções, 6 entidades e 29 nós de diálogo**. Os casos foram reexecutados contra a nuvem, com o backend integrado: emergência reconhecida com confiança 1,00; coleta de sintoma preservando contexto entre três turnos; medida de pressão capturada nos formatos com barra e por extenso; recusa correta na dúvida sobre medicamento.

Foram testadas também seis entradas **fora do domínio** — de "minha casa tá pegando fogo" a "meu cachorro está passando mal". Na primeira execução, três foram indevidamente classificadas dentro do domínio, uma delas como emergência cardíaca. A correção exigiu adicionar 24 *counterexamples* à skill, desligar a desambiguação e criar uma rede de segurança no backend contra respostas vazias. Após a correção, as seis passaram a cair corretamente no tratamento de exceção.

Ao todo, onze dificuldades técnicas reais foram registradas durante o desenvolvimento, com causa, solução e resultado. Seis delas só se tornaram visíveis no uso real da aplicação ou após a integração com a nuvem — nenhuma seria detectável apenas pelos testes automatizados.

## 7. Limitações

Um assistente que interpreta apenas linguagem **não realiza triagem clínica**: ele não dispõe de sinais vitais, exame físico ou histórico do paciente, e organiza o relato sem avaliar risco. As faixas de pressão são informativas e não consideram idade, comorbidades ou medicação em uso. A cobertura linguística está limitada a cerca de dez exemplos por intenção, o que não representa a diversidade real de expressão dos pacientes. A ordem de coleta é fixa, e o contexto da conversa não sobrevive ao reinício do servidor.

Reconhecer explicitamente essas fronteiras é parte da responsabilidade de projeto de um sistema aplicado à saúde.

---

*Documento técnico completo, com a árvore de diálogo integral, o registro das dificuldades encontradas e as tabelas de resultado: `document/FLUXO_CONVERSACIONAL.md`.*
