# ADR 0003 — Autoverificação da IA no lugar da revisão humana

- **Status:** aceita
- **Data:** 2026-11-07
- **Decisores:** equipe do projeto (decisão D6, registrada em `docs/requisitos/requisitos.md`)
- **Relação com outras decisões:** **substitui em parte o ADR 0002** — o item 4
  daquele ADR (explicação nasce como rascunho e só aparece depois de aprovada
  por pessoa) deixa de valer. Os itens 1 a 3 do ADR 0002 continuam em vigor.

## Contexto

O ADR 0002 criou um portão humano: a IA gera a explicação como rascunho e um
integrante da equipe aprova antes de o aluno ver (`python -m app.review`,
`SERVE_ONLY_APPROVED=true`). Esse portão resolvia o risco certo — analogia que
soa correta e está errada, como a que descrevia o protocolo pare-e-espere em vez
do TCP — mas tem dois problemas que só apareceram com o projeto andando:

1. **Não escala com a personalização.** O número de revisões cresce com
   conceitos × interesses. A pesquisa da Etapa 1 mostrou interesses variados
   entre apenas cinco respondentes [questionário: item 7]. Um aluno que informa
   um universo novo cairia sempre na explicação padrão, ou seja, exatamente a
   pessoa que o app existe para atender ficaria sem personalização.
2. **Quebra a promessa de RF09.** A decisão D4 permite trocar de universo de
   dentro da explicação. Com revisão humana, a troca devolveria "em revisão" na
   maioria das tentativas, e a tarefa do teste de usabilidade não poderia ser
   executada.

Há ainda um limite de prazo: a entrega é 09/11/2026 e não há pessoa disponível
para revisar conteúdo durante as sessões de teste.

## Decisão

A revisão humana prévia sai. Antes de exibir qualquer resposta, **o próprio
modelo verifica o rascunho**, por autoverificação no estilo *Chain-of-Verification*
(Dhuliawala et al., 2024), e só então os validadores determinísticos decidem.

Fluxo, implementado em `apps/api/app/services/verification.py`:

| # | Etapa | O que acontece |
|---|---|---|
| 1 | **Rascunho** | O gerador produz a explicação nos seis passos, ou a resposta de uma pergunta do aluno |
| 2 | **Perguntas de checagem** | O modelo lista as afirmações técnicas do rascunho e escreve uma pergunta de verificação para cada uma |
| 3 | **Respostas independentes** | Cada pergunta é respondida em **chamada separada, sem o rascunho no contexto**, para que o modelo não repita o próprio erro |
| 4 | **Veredito** | O modelo compara respostas e rascunho, confere se a analogia não contradiz a versão técnica e se os fatos do universo estão corretos. Saída estruturada: `aprovada` ou `reprovada` + motivos |
| 5 | **Validadores** | `validators/grounding.py` continua valendo, depois da autoverificação |
| 6 | **Reprovada** | Uma nova tentativa com os motivos. Reprovada de novo → explicação padrão com aviso visível |

Regra que não admite exceção: **nenhuma resposta reprovada é exibida.** O
caminho de falha é sempre o texto-base revisado, nunca o rascunho duvidoso.

O passo 3 é o que dá valor ao método. Perguntar ao modelo "isto está certo?"
com o rascunho à vista produz concordância; perguntar a mesma coisa sem o
rascunho produz uma resposta independente, que pode discordar.

A referência da checagem é **fixa por conceito**: o texto-base de
`content/concepts/<slug>.md`, revisado e versionado no Git. A autoverificação
compara o rascunho com esse texto, não com a memória do modelo.

## Alternativas consideradas

| Alternativa | Por que não |
|---|---|
| **Manter a revisão humana** (ADR 0002) | É mais segura, e seria a escolha para uso real com muitos alunos. Não cabe no prazo nem na troca de universo em tempo de uso |
| **Só os validadores determinísticos** | Pegam citação fora do texto-base, vazamento de termos do universo e armadilhas conhecidas, mas não pegam erro técnico novo: são regras, não compreensão |
| **Busca em fonte externa (RAG) na checagem** | Mitiga melhor o limite do Huang et al. (2024), mas acrescenta índice, recuperação e custo de infraestrutura a um projeto de disciplina. O texto-base fixo por conceito cumpre o papel de fonte externa com muito menos peça móvel |
| **Dois modelos diferentes** (um gera, outro verifica) | Reduz o erro correlacionado de verdade. Exige segunda chave e segundo provedor; fica registrado como trabalho futuro |

## Consequências

**(+)** A personalização funciona para universo que ninguém revisou antes, que
é o caso de uso principal do app.

**(+)** RF09 e RF11 tornam-se executáveis no teste de usabilidade.

**(+)** O caminho de falha é testável sem IA: os testes injetam um gerador e um
verificador falsos e cobrem os três casos — aprovada, reprovada uma vez e
reprovada duas vezes.

**(−)** **A garantia é mais fraca que a revisão humana, e isso precisa aparecer
no relatório.** Um modelo verificando a si mesmo reduz erros, mas não os
elimina; sem informação externa, a autocorreção pode piorar o resultado (Huang
et al., 2024). Não afirmamos que o conteúdo está correto — afirmamos que passou
por autoverificação e pelos validadores.

**(−)** Custo por explicação sobe: são 3 a 5 chamadas ao modelo em vez de 1.
Mitigado pelo cache (explicação aprovada fica no banco) e por `max_tokens`.

**(−)** Latência maior. No chat isso é visível, e por isso a interface mostra
estado de espera em mensagem própria, sem travar a leitura do que já chegou.

### Mitigações mantidas

- Botão "Está errada" (RF05) continua, e o caso vai para `under_review`.
- **Medir no teste de usabilidade quantas explicações exibidas tinham erro
  técnico** — métrica nova no protocolo da Etapa 4. É o único número que diz se
  a autoverificação funcionou na prática com este app.
- `EXPLANATION_PROVIDER=curated` continua desligando a IA por completo. As
  sessões de teste de usabilidade rodam assim (Mágico de Oz), com explicações
  escritas à mão: o que se avalia na Etapa 4 é a interface, não o modelo.

## Fontes

- DHULIAWALA, S. et al. **Chain-of-Verification Reduces Hallucination in Large
  Language Models.** Findings of the ACL, 2024.
- HUANG, J. et al. **Large Language Models Cannot Self-Correct Reasoning Yet.**
  ICLR, 2024.
- OWASP. **Top 10 for LLM Applications**, 2025 — LLM09 (desinformação).
- ADR 0002 deste repositório, itens 1 a 3 (texto-base como fonte de verdade,
  gerador com duas implementações, validadores determinísticos).


## Atualização (07/11/2026): pesquisa na web como referência (D8)

O texto-base deixou de vir só da biblioteca. Para assuntos fora dela, a IA
pesquisa na web (Gemini com a ferramenta Google Search) e escreve um texto de
referência com as fontes encontradas, guardado na tabela `pesquisas`. A
autoverificação e os validadores passam a conferir a explicação contra esse
texto.

- (+) O aluno pode pedir qualquer assunto técnico, sem conteúdo pré-gravado.
- (+) A referência vem de fora do modelo e as fontes ficam visíveis para o aluno.
- (−) O texto de referência é escrito pela própria IA a partir das fontes: um
  erro de leitura dela passa para a referência. Mitigação: só há referência
  com pelo menos uma fonte, o aluno vê as fontes, e "Está errada" tira a
  explicação de circulação.
- (−) Cada assunto novo custa uma pesquisa (cota da API). Mitigação: a
  pesquisa é guardada e reaproveitada para o mesmo assunto.


## Atualização (07/11/2026): uma pergunta de checagem por padrão

No plano gratuito do Gemini, a cota da chave acabou em poucos testes: cada
explicação gastava até cerca de 12 chamadas (5 de verificação por tentativa,
até 2 tentativas, mais o rascunho). O teto de perguntas de checagem caiu de 3
para 1 (`AUTOVERIFICACAO_PERGUNTAS`, de 1 a 6), e a verificação passa a custar
3 chamadas: perguntas, uma resposta independente e o veredito.

- (+) Quase metade das chamadas por explicação.
- (−) Menos afirmações conferidas uma a uma. Mitigação: a pergunta que fica é a
  mais arriscada (o prompt ordena por risco, priorizando o mecanismo), e o
  veredito continua comparando o rascunho inteiro com o texto-base.
- Com cota disponível (plano pago), voltar a 3 é só mudar a variável.


## Atualização (09/11/2026): referência sem busca na web (D9)

No plano gratuito, a ferramenta Google Search da API do Gemini respondeu
HTTP 429 mesmo sem nenhum uso no dia: a cota dela é zero nesse plano. Para que
o app explique qualquer assunto sem depender de faturamento, a referência pode
ser escrita pela própria IA, com o conhecimento dela (`PESQUISA_PROVIDER=ia`).
Com `PESQUISA_PROVIDER=gemini`, a busca é tentada primeiro e esse modo é a
reserva.

- (+) Funciona com qualquer cota em que a IA funcione, sem custo extra de busca.
- (−) Sem fonte externa, a autoverificação compara a IA com ela mesma: é o
  caso em que a autocorreção mais falha (Huang et al., 2024). Mitigações: o
  prompt manda deixar de fora o que não for consenso; o aluno é avisado, na
  conversa, de que a explicação não tem fontes e deve ser conferida com o
  material da disciplina; "Está errada" continua tirando a explicação de
  circulação; com faturamento ativo, voltar para `gemini` restaura as fontes.

Troca de modelo no mesmo dia: o Gemini 3.8 Flash tem, no plano gratuito,
5 chamadas por minuto e 20 por dia; uma explicação com autoverificação faz 4.
O projeto passou a usar o Gemini 3.5 Flash Lite (15 por minuto, 500 por dia),
com a ressalva de que um modelo menor tende a ser reprovado mais vezes na
autoverificação.


## Atualização (09/11/2026): modelo maior só para a analogia

Com o Gemini 3.5 Flash Lite, as analogias saíam genéricas ("navios piratas"
em vez de elementos de One Piece). A explicação passou a ter modelo próprio
(`LLM_MODEL_EXPLICACAO`, hoje o Gemini 3.8 Flash), enquanto a referência e a
autoverificação continuam no modelo leve, que faz a maior parte das chamadas.
Se o modelo da explicação bater no limite de uso, a explicação é escrita com o
modelo leve. O prompt passou a pedir elementos próprios do universo, só os de
que o modelo tem certeza, já que um erro sobre o universo reprova a explicação.
