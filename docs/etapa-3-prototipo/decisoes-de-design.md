# Decisões de design — Etapa 3 (Desenhar)

Este documento fecha o terceiro elo da cadeia de rastreabilidade do projeto:

```
achado (Etapa 1) → persona e cenário (Etapa 2) → requisito → DECISÃO DE DESIGN (aqui)
  → elemento no código → tarefa do teste (Etapa 4) → resultado → melhoria
```

Cada decisão recebe um código **DD**, citado nos esboços, no código e no
protocolo do teste. Quem discordar de uma decisão deve conseguir, lendo a linha
dela, saber exatamente qual evidência derrubar.

## Como ler os rótulos de origem

| Rótulo | Significa |
|---|---|
| `[questionário: item N]` | Dado da Etapa 1, contagem sobre **n = 5**. Não é amostra representativa |
| `[hipótese da equipe]` | Suposição nossa. Continua marcada assim no relatório final |
| `[da literatura]` | Vem de fonte citada no fim deste documento, não dos nossos dados |
| `[decisão Dn]` | Decisão de projeto de 07/11/2026, registrada em `../requisitos/requisitos.md` |
| `[cenário n]` | Cenário de atividade da Etapa 2 |

Critérios WCAG 2.2 aparecem no formato `1.4.10 Realinhar (AA)`.

---

## 1. Estrutura da explicação e do diálogo

| ID | Decisão | Origem | Requisito / persona | Critério |
|---|---|---|---|---|
| **DD01** | A pessoa escolhe **o conceito antes do universo**. O conteúdo técnico é o assunto; o universo é como ele será contado | `[hipótese da equipe]`, apoiada em Glynn: a analogia serve ao conceito-alvo, não o contrário `[da literatura]` | RF02, RF03 · todas as personas | — |
| **DD02** | **Uma parte da explicação por mensagem**, avançando só quando a pessoa pede ("Continuar"). Nada aparece sozinho | `[questionário: item 14]` — 4 de 5 relatam cansaço ao ler textos longos em tela, ninguém respondeu "nunca" · divergência 1 da seção 6 dos Cenários · `[decisão D3]` | RF10 · Ana, Rafael · DP13 | `2.2.2 Pausar, parar, ocultar (A)` |
| **DD03** | A explicação **começa pela analogia**; um botão troca aquele mesmo passo pela versão técnica e volta, mantendo o número do passo | `[questionário: item 11]` — maior média das quatro escalas (4,0); R01 marcou 5 · `[decisão D2]` · `[cenário 3]` | RF04 · Caio · DP05 | `4.1.2 Nome, função, valor (A)` |
| **DD04** | **Trocar de universo sem sair da explicação**, voltando ao mesmo passo com o novo universo | Divergência 3 da seção 6 dos Cenários · `[decisão D4]` · `[questionário: item 7]` — universos variados entre cinco pessoas | RF09 · Rafael | `3.2.5 Mudança a pedido (AAA)` |
| **DD05** | O campo aceita **qualquer texto**, mas a resposta fica **presa ao conceito**. Fora dele, recusa educada nomeando o conceito atual e duas saídas: "Continuar este" e "Escolher outro conceito" | `[decisão D5]` · `[da literatura]` — Nielsen H3 (controle e liberdade) e H9 (ajudar a reconhecer e sair do erro) | RF11 | `3.3.1 Identificação de erro (A)` |
| **DD06** | Pergunta **dentro** do conceito que o texto-base não responde vira **"não consegui verificar isso"**, nunca um palpite | `[questionário: item 12]` — 3 de 5 perderiam a confiança no app diante de um erro · `[decisão D6]` | RNF04 · todas as personas | — |
| **DD07** | O passo **"onde a comparação falha" é obrigatório**, não um extra que se possa pular | `[da literatura]` — Glynn: toda analogia tem limite, e omiti-lo produz concepção equivocada; carga cognitiva: detalhes atraentes e irrelevantes atrapalham | RF03 · T2 do teste · DP01 | — |
| **DD08** | A resposta da pergunta de transferência fica **escondida atrás de um botão** | `[da literatura]` — recuperação ativa (*retrieval practice*): ver a resposta junto da pergunta anula o efeito | RF03 · DP13 | — |

### Por que o chat, e o que ele não promete

A aparência de chat foi escolhida porque é a interface que o público-alvo já
usa para estudar: **5 de 5 respondentes usam IA para estudar e 3 deles quase
todos os dias** `[questionário: itens 4 e 5]`. Não é uma escolha estética — é
reconhecimento de que o concorrente real do app é o ChatGPT, e que exigir um
modelo de interação diferente custaria aprendizado sem ganho.

O risco dessa escolha é o oposto: **parecer um chat promete conversa livre**, e
este app não entrega isso (DD05). A mitigação é dizer o limite **antes** do
primeiro erro — no aviso fixo abaixo do campo de digitação, em toda tela
—, não só depois que a pessoa já perguntou `[da literatura]`, Nielsen H2
(correspondência com o mundo real) e H1 (visibilidade do estado do sistema).

---

## 2. Acessibilidade da interface de chat

Um chat é uma lista que cresce sozinha. Para quem usa leitor de tela ou
ampliação, é exatamente o padrão que mais costuma quebrar. As decisões abaixo
existem para que ele não quebre, e cada uma vira um item verificável na
auditoria da Etapa 4.

| ID | Decisão | Origem | Critério |
|---|---|---|---|
| **DD09** | O histórico é uma região `role="log"` com `aria-live="polite"`. Anuncia-se a **mensagem pronta**, nunca o texto sendo montado | `[da literatura]` · `[decisão D3]` | `4.1.3 Mensagens de status (AA)` |
| **DD10** | **Nada rola nem recebe foco sozinho** quando chega mensagem nova. Quem quiser descer usa o botão "Ir para a última mensagem" | `[da literatura]` — movimento automático desorienta quem usa ampliação: a pessoa lê uma janela de poucos caracteres e perde o ponto | `2.2.2 (A)`, `3.2.5 (AAA)` |
| **DD11** | Todos os alvos têm **no mínimo 24 × 24 px**, com 44 × 44 px como meta nos botões de ação da mensagem | `[questionário: item 3]` — 5 de 5 estudam pelo celular · Ana | `2.5.8 Tamanho do alvo mínimo (AA)` |
| **DD12** | O campo de pergunta tem **rótulo visível acima**, não placeholder | `[da literatura]` — placeholder some ao digitar e costuma falhar no contraste | `3.3.2 Instruções ou rótulos (A)` |
| **DD13** | Todo estado é dito **por texto**, além da cor ou da forma: universo atual marcado com "atual", passo em versão técnica marcado com "téc" | Ana `[da literatura]` | `1.4.1 Uso de cor (A)` |
| **DD14** | A **largura da linha de texto não passa de ~80 caracteres**, mesmo em tela larga | `[da literatura]` — linha longa dificulta o retorno visual, sobretudo com ampliação | `1.4.8 Apresentação visual (AAA)` |
| **DD15** | A 320 px, os botões de ação da mensagem **empilham**; nada é escondido e nada rola para o lado | `[questionário: item 3]` · RNF01, RNF07 | `1.4.10 Realinhar (AA)` |
| **DD16** | A folha de troca de universo **prende o foco**, fecha com `Esc` e **devolve o foco ao botão que a abriu** | `[da literatura]` | `2.1.2 Sem armadilha de teclado (A)`, `2.4.3 Ordem de foco (A)` |
| **DD17** | Os **três temas e a escala de fonte continuam valendo no chat**, inclusive em "Enorme" (2×) | `[questionário: item 13]` — 4 de 5 usam algum ajuste de leitura | `1.4.4 Redimensionar texto (AA)`, `1.4.6 Contraste melhorado (AAA)` |

### Um conflito que ficou em aberto

`role="log"` com `aria-live="polite"` faz o leitor de tela ler **a mensagem
inteira** quando ela chega. Numa explicação técnica de vários parágrafos, isso
é muito texto de uma vez, e a pessoa não consegue interromper com facilidade.

A alternativa seria deixar o histórico mudo e anunciar só um aviso curto
("Passo 3 pronto") numa região `role="status"`, deixando a leitura do conteúdo
para a navegação normal. **Mantivemos `role="log"` porque é o que a decisão D3
registrou** — mas a troca não é obviamente pior, e este é um dos pontos que
pedem teste com uma pessoa que use leitor de tela no dia a dia, não opinião
nossa. Está registrado como item aberto na auditoria da Etapa 4.

---

## 3. Responsividade (decisão D1)

| ID | Decisão | Origem | Critério |
|---|---|---|---|
| **DD18** | **Uma interface só, em coluna única**, que apenas se estreita. O conceito, o universo e o progresso ficam num cartão no topo da conversa, igual em qualquer largura | `[decisão D1]` · RNF07 · `[questionário: item 3]` — 5 de 5 estudam pelo celular | `1.4.10 (AA)` |
| **DD19** | A posição na explicação é dita **duas vezes, por meios diferentes**: uma barra de progresso com "parte 3 de 6" para quem vê, e um complemento oculto no título de cada mensagem para quem ouve | `[hipótese da equipe]` · a barra é decorativa (`aria-hidden`), então a posição precisa existir em texto | `1.3.1 Informações e relações (A)`, `1.4.1 Uso de cor (A)` |

**DD18 mudou entre o esboço e o código, e o esboço fica como está.** A tela 2
dos esboços propõe uma coluna lateral fixa no desktop, com a trilha das seis
partes. Na implementação virou coluna única nas duas larguras, por três razões:
a mesma interface em qualquer tela é o que a decisão D1 pede e o que reduz o
risco de um comportamento só aparecer num tamanho; a linha de leitura fica curta
nos dois casos (DD14); e a barra de progresso entrega a mesma informação da
trilha ocupando uma fração do espaço.

Os esboços **não foram redesenhados para esconder essa mudança**: o esboço é o
que se projetou, e o código é o que se construiu. A diferença entre os dois é o
registro de que houve iteração, que é o princípio (4) da ISO 9241-210.

---

## 4. Confiança no conteúdo (decisão D6)

| ID | Decisão | Origem | Requisito |
|---|---|---|---|
| **DD20** | Explicação gerada por IA traz **aviso em mensagem própria**, não em letra miúda no rodapé | `[questionário: item 12]` · `[da literatura]` — Nielsen H1 | RNF04 |
| **DD21** | **"Está errada" fica em toda mensagem de explicação**, não só no fim da conversa | `[questionário: item 12]` — 3 de 5 · `[cenário 2]`, passo 7 | RF05 · T5 |
| **DD22** | A espera da autoverificação aparece como **mensagem própria** ("Conferindo a explicação…"), que depois é substituída. A leitura do que já chegou não trava | `[hipótese da equipe]` — a autoverificação são 3 a 5 chamadas ao modelo (ADR 0003), e a latência será visível | RNF04 |
| **DD23** | Reprovada duas vezes, aparece **a explicação padrão com o motivo**, nunca o rascunho reprovado | ADR 0003 · `[decisão D6]` | RNF03, RNF04 |

---

## 3-A. A engrenagem não aparece

| ID | Decisão | Origem | Critério |
|---|---|---|---|
| **DD27** | O título de cada mensagem traz **só o nome da parte** — "A cena", "Quem é quem" —, sem "Passo 3 de 6". A numeração vai para a barra de progresso e para um trecho oculto no título | `[hipótese da equipe]` · `[da literatura]` — Nielsen H2 (falar a língua de quem usa) | `4.1.2 Nome, função, valor (A)` |

As seis partes continuam existindo: vêm do modelo *Teaching-With-Analogies*
(Glynn, 1991), estão nos critérios de aceite de RF03 e a tarefa T2 do teste de
usabilidade depende da parte "onde a comparação não vale". O que saiu da tela
foi o **vocabulário interno** delas.

Ninguém diz "estou no passo 3 de 6" ao explicar algo a um colega. Um aplicativo
que fala assim expõe a própria engrenagem e parece protótipo, não produto — e,
pior, convida quem lê a contar passos em vez de acompanhar o raciocínio.

O cuidado aqui é não jogar fora a informação junto com o rótulo. Saber quanto
falta reduz a ansiedade de quem estuda (Nielsen H1), e para quem usa leitor de
tela a posição é o que impede a sensação de estar perdido numa lista que cresce.
Por isso a posição aparece **duas vezes, por meios diferentes**, como diz DD19.

---

## 4-A. Cor

| ID | Decisão | Origem | Critério |
|---|---|---|---|
| **DD24** | A identidade visual é uma **paleta em tons de azul**: fundos, superfícies, texto e ação. O **vermelho de erro fica fora dela** — cor de alerta é convenção, não estética, e pintar de azul um botão "apagar tudo" o faria parecer inofensivo | `[hipótese da equipe]` · `[da literatura]` — Nielsen H4 (consistência e padrões) | `1.4.1 Uso de cor (A)`: o vermelho nunca é o único sinal, sempre vem com texto |
| **DD25** | O **tema de alto contraste continua amarelo sobre preto**, fora da paleta azul. É a combinação dos teclados ampliados e das lupas eletrônicas, e Ana é a razão de o tema existir | Ana `[da literatura]` · `[questionário: item 13]` — 4 de 5 usam algum ajuste de leitura | `1.4.6 Contraste melhorado (AAA)` |
| **DD26** | A separação entre blocos vem de **preenchimento**, não de linha clara. Uma borda discreta o bastante para parecer elegante mediu 1,38:1 e não alcança os 3:1 exigidos | Medição com `contrast_check.py`, 07/11/2026 | `1.4.11 Contraste de elementos não textuais (AA)` |

Os 34 pares da paleta estão em `apps/web/src/styles/paleta-contraste.json` e são
medidos por script. **Ao mudar uma cor, meça de novo** — o número que vai para o
relatório é resultado medido, não promessa:

```bash
python .claude/skills/lumen-ihc-acessibilidade/scripts/contrast_check.py --palette apps/web/src/styles/paleta-contraste.json
```

---

## 5. O que foi deliberadamente deixado de fora

Registrar o que não entrou vale tanto quanto registrar o que entrou: evita que
a ausência pareça esquecimento.

| Fora do escopo | Por quê |
|---|---|
| **RF08** — começar pela versão técnica por padrão | Adiado pela decisão D2. Caio é atendido pelo botão de alternar (DD03). **O teste de usabilidade vai dizer se isso bastou**: se o participante de perfil cético reclamar do clique extra em T3, RF08 volta para a lista |
| Streaming da resposta, palavra por palavra | Conflita com DD09: anunciar texto em construção numa região viva é ruído para leitor de tela |
| Histórico de conversas entre sessões | Não há conta de usuário (RF01). A conversa vive na sessão anônima |
| Voz (ditar a pergunta, ouvir a resposta) | Seria útil para Ana `[da literatura]`, mas não cabe no prazo. Fica como trabalho futuro no relatório |

---

## 6. Ordem real do processo, sem maquiagem

A tela inicial e os seis passos **já existiam em código** antes desta etapa;
seu esboço documenta o que havia. As quatro telas novas — chat, troca de
universo, versão técnica e recusa — **foram desenhadas antes de existir
código**, a partir das divergências da seção 6 dos Cenários.

Dito de outro modo: a Etapa 2 encontrou três divergências entre o que os
cenários pediam e o que o protótipo fazia, e a Etapa 3 as resolveu com decisões
registradas (D1 a D6) e com estes esboços. É iteração de verdade, e é o que a
ISO 9241-210:2019 chama de princípio (4).

## 7. Segunda iteração: o primeiro protótipo não parecia um chat (07/11/2026)

A equipe usou o protótipo de alta fidelidade e o reprovou em quatro pontos:
não parecia um chat de IA; o visual de cartões empilhados; o fluxo em telas
separadas (interesses → lista de conteúdos → explicação); e a tabela "Quem é
quem". A revisão abaixo substitui DD01 e as partes de DD04 e DD16 que falavam
da folha de troca de universo. É a avaliação formativa da ISO 9241-210 agindo
antes do teste com participantes.

| ID | Decisão | Origem | Requisito / persona | Critério |
|---|---|---|---|---|
| **DD28** | **Tudo dentro do chat.** O app pergunta o assunto e o aluno escreve com as próprias palavras; depois pergunta o universo, e o aluno escreve. Some a tela de interesses e a lista de conteúdos (substitui DD01) | `[decisão D7]` · `[questionário: itens 4 e 5]` — o público já estuda conversando com IA | RF02, RF03, RF10 · todas as personas | `3.3.2 Rótulos ou instruções (A)`: a pergunta do app é a instrução, e o campo tem rótulo acessível que muda com o papel dele |
| **DD29** | O assunto digitado é **reconhecido na biblioteca** de conteúdos, sem IA. Assunto fora dela recebe resposta honesta ("ainda não tenho material de referência") e sugestões; o app não improvisa uma explicação sem fonte | `[decisão D6]` · `[da literatura]` — sem referência externa, a autocorreção da IA falha (Huang et al., 2024) | RNF04 · DD06 | — |
| **DD30** | **Visual de chat de IA**: mensagens do app em texto corrido, sem balão; mensagens do aluno em balão à direita; campo arredondado fixo embaixo, Enter envia e Shift+Enter quebra a linha | `[hipótese da equipe]` — reconhecimento em vez de memorização (Nielsen H6): o modelo já é conhecido | RF10 · RNF07 | `1.4.11 Contraste não textual (AA)` na borda do campo |
| **DD31** | **Ações numa barra fixa acima do campo** (Continuar, Ver versão técnica, Trocar universo, Está errada), e não dentro da mensagem. O botão "Continuar" fica sempre no mesmo lugar e não some debaixo do foco a cada parte | `[hipótese da equipe]` · consistência (Nielsen H4) | RF04, RF05, RF09 | `2.4.3 Ordem do foco (A)`, `3.2.3 Navegação consistente (AA)` |
| **DD32** | "Trocar universo" é uma **pergunta do app na conversa**, não uma janela sobreposta (substitui a folha de DD16) | `[decisão D3]` — uma só forma de interação | RF09 | `3.2.5 Mudança a pedido (AAA)` |
| **DD33** | "Quem é quem" vira **frases curtas** ("bolas numeradas → segmentos com número de sequência"), sem tabela | Avaliação da equipe · a 320 px a tabela virava uma pilha de células difícil de seguir | RF03 · Ana | `1.3.1 Informações e relações (A)`: a seta é decorativa e o leitor de tela ouve "no conceito" |
| **DD34** | A tela só se move por gesto do aluno: ao enviar, a fala dele sobe para o alto e a resposta aparece logo abaixo. Mensagem do app chegando continua sem rolar a tela (mantém DD10) | `[da literatura]` — movimento automático desorienta quem usa ampliação | RF10 · Ana | `2.4.11 Foco não encoberto (AA)`: `scroll-padding` mantém o foco acima do rodapé fixo |
| **DD35** | Com texto "Muito grande" ou "Enorme", ou tela baixa, o rodapé **deixa de ser fixo** e rola com a página | Persona Ana · a 400% de zoom um rodapé fixo ocuparia quase a tela toda | RA04, RA05 · Ana | `1.4.10 Realinhar (AA)` |

## Fontes

- **GLYNN, S. M.** Explaining science concepts: a Teaching-with-Analogies
  model. In: *The Psychology of Learning Science*. Erlbaum, 1991.
- **ISO 9241-210:2019** — design centrado no ser humano, princípio (4).
- **NIELSEN, J.** *10 Usability Heuristics for User Interface Design.* Nielsen
  Norman Group, 1994 (rev. 2024).
- **ROSSON, M. B.; CARROLL, J. M.** *Usability Engineering.* Morgan Kaufmann, 2002.
- **SWELLER, J.; AYRES, P.; KALYUGA, S.** *Cognitive Load Theory.* Springer, 2011.
- **W3C.** *WCAG 2.2*, 2023 — critérios citados por número e nível.
- **W3C.** *Making Content Usable for People with Cognitive and Learning
  Disabilities (COGA)*, 2021.
- Biblioteca do Lumen: `references/acessibilidade.md` (RA01–RA24) e
  `references/carga-cognitiva-e-personalizacao.md` (DP01–DP18).
- ADR [0003](../adr/0003-autoverificacao-da-ia.md) deste repositório.
