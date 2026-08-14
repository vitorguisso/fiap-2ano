# Roteiro do Vídeo de Demonstração — CardioIA Fase 5

**Limite do enunciado: até 3 minutos.** O roteiro abaixo está dimensionado para
2min40s, deixando margem.

O enunciado pede um vídeo "demonstrando o funcionamento da interação". O foco,
portanto, é a **conversa acontecendo** — não é uma apresentação de slides sobre o
projeto. Mostre a tela, digite de verdade, deixe as respostas aparecerem.

---

## Preparação antes de gravar

- [ ] Backend rodando: `python src/backend/app.py`
- [ ] Confirmar o modo no selo do canto superior direito da interface
      (o ideal é gravar em modo `WATSON`, com o `.env` configurado)
- [ ] Navegador em tela cheia, zoom em 100% ou 110% (o texto precisa ser legível
      no vídeo)
- [ ] Fechar abas e notificações que possam aparecer na gravação
- [ ] Conversa zerada (botão "Reiniciar conversa")
- [ ] Testar o áudio antes de gravar a tomada final

Sugestão de ferramenta: a gravação nativa do Windows (`Win + G`) ou OBS Studio.

---

## Bloco 1 — Abertura (0:00 – 0:20)

**Tela:** interface do CardioIA já aberta, com a mensagem de boas-vindas visível.

**Fala:**

> "Este é o CardioIA Assistente, o módulo conversacional do projeto CardioIA,
> desenvolvido na Fase 5. É um assistente de atendimento inicial em saúde
> cardiovascular, construído no IBM Watson Assistant e integrado a um backend em
> Flask."

**Ação:** aponte o cursor para o aviso amarelo no topo.

> "Antes de qualquer coisa: ele não faz diagnóstico e não substitui avaliação
> médica. Esse limite é parte do projeto, e vou mostrar como ele aparece no
> comportamento do assistente."

---

## Bloco 2 — Triagem de sintoma em múltiplos turnos (0:20 – 1:10)

Este é o bloco mais importante. Ele demonstra intenção, entidade, variáveis de
contexto e diálogo de múltiplas etapas de uma só vez.

**Digite:** `minhas pernas estão inchando no fim do dia`

**Fala enquanto a resposta aparece:**

> "O assistente reconheceu a intenção de relato de sintoma e extraiu a entidade
> de sintoma — repare no rodapé, que mostra o resultado do processamento de
> linguagem natural. Ele identificou 'inchaço' mesmo eu tendo escrito 'inchando',
> numa forma verbal diferente da cadastrada."

**Digite:** `uns três dias`

> "Aqui está o ponto central: ele lembra qual era o sintoma e continua a coleta,
> perguntando agora a duração e depois a intensidade. Isso é sustentado pelas
> variáveis de contexto da árvore de diálogo."

**Digite:** `leve`

> "E fecha com um resumo estruturado do relato — sintoma, duração e intensidade —
> que o paciente pode levar para a consulta. Foi exatamente isso que
> organizamos: transformar um relato solto em informação estruturada."

---

## Bloco 3 — Entidade de regex e regra de domínio (1:10 – 1:45)

**Digite:** `minha pressão deu 190 por 120`

**Fala:**

> "Pressão arterial é capturada por uma entidade de expressão regular, porque o
> paciente escreve de formas imprevisíveis: com barra, com 'x' ou com 'por'.
> Escrevi 'por' aqui e ele entendeu."

**Ação:** aponte para o rodapé, que mostra a classificação.

> "E há uma divisão de responsabilidade: o Watson reconhece o formato da medida,
> mas quem avalia se o valor é plausível e em que faixa clínica ele cai é o
> backend. Esse valor entrou como muito elevado, e por isso a resposta recebeu o
> destaque de urgência."

---

## Bloco 4 — Emergência e limite ético (1:45 – 2:20)

**Ação:** clique em "Reiniciar conversa".

**Digite:** `acho que estou tendo um infarto`

**Fala:**

> "Emergência é uma intenção separada, e o nó dela é o primeiro da árvore de
> diálogo. Isso é uma decisão de segurança: se o nó de sintoma viesse antes, um
> paciente em quadro agudo entraria num questionário de coleta de dados antes de
> receber qualquer orientação."

**Digite:** `posso parar de tomar losartana`

> "E aqui o oposto: um nó projetado para não responder. Ele reconhece a intenção,
> explica por que não pode orientar sobre medicamento e indica o canal correto.
> Reconhecer e recusar é melhor do que deixar a pergunta cair no 'não entendi'."

---

## Bloco 5 — Reconhecendo o próprio limite (2:20 – 2:45)

Este bloco costuma impressionar mais do que os anteriores, porque mostra maturidade
de projeto: o assistente sabe o que **não** sabe.

**Digite:** `meu cachorro está passando mal`

> "Aqui está algo que descobrimos testando: na primeira versão, essa frase era
> classificada como emergência cardíaca — o classificador sempre escolhe a intenção
> mais provável, e sem exemplos do que está fora do domínio, tudo é atraído para
> dentro dele. Corrigimos com 24 counterexamples, que ensinam o Watson a marcar
> entradas como irrelevantes."

**Digite:** `quanto custa um carro`

> "Na segunda falha seguida, ele escalona: reconhece o próprio limite e oferece
> encaminhamento humano, em vez de repetir a mesma resposta indefinidamente."

**Encerramento:**

> "O código, a skill exportada do Watson e a documentação completa estão no
> repositório. Obrigado."

---

## Erros a evitar

| Erro | Por quê |
|------|---------|
| Gravar em modo `LOCAL` sem explicar | O requisito da atividade é a integração com o Watson. Se por algum motivo gravar em modo local, **diga isso no vídeo** e explique que é o modo de demonstração — omitir seria pior |
| Ler o roteiro palavra por palavra | Soa artificial. Use como guia dos pontos a cobrir |
| Passar de 3 minutos | É limite explícito do enunciado |
| Mostrar o `.env` na tela | Expõe credenciais na gravação |
| Digitar rápido demais | O avaliador precisa conseguir ler a resposta antes de você seguir |
| Explicar tudo o que existe no projeto | O vídeo é sobre a **interação**. Arquitetura e decisões estão no relatório |

---

## Checklist pós-gravação

- [ ] Duração menor ou igual a 3 minutos
- [ ] Áudio audível, sem ruído dominante
- [ ] Texto da conversa legível na resolução final
- [ ] Nenhuma credencial visível em nenhum momento
- [ ] Vídeo publicado (YouTube não listado, Drive ou similar) com **link de acesso liberado**
- [ ] Link inserido no README, na seção "Vídeo de Demonstração"
- [ ] Link testado em uma janela anônima, para confirmar que o avaliador conseguirá abrir
