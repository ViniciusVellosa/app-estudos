# Avaliação heurística — Etapa 4 (Avaliar)

| | |
|---|---|
| Avaliadores | **Os integrantes do grupo** — 3 a 5 pessoas |
| Como | Cada um avalia **sozinho primeiro**, depois o grupo consolida |
| Objeto | O app em `apps/web`, versão `54c6a6d` (ver o resultado abaixo) |
| Percurso | As mesmas tarefas T1 a T5 do teste (`protocolo-teste.md`) |
| Tempo | 40 a 60 min por avaliador, mais 30 min de consolidação |

> **Por que sozinho primeiro.** Se o grupo avalia junto, a primeira opinião ancora
> as outras e vocês acham menos problemas. Nielsen é explícito: avaliadores
> independentes encontram conjuntos diferentes de problemas, e é a união deles que
> dá valor ao método. Juntar só na consolidação.

> **Faça isto ANTES do teste com usuários, não depois.** O método é analítico e
> barato: vocês mesmos acham a maior parte dos problemas óbvios. Gastar a sessão de
> um participante com um botão mal rotulado que o grupo teria achado em 20 minutos
> é desperdiçar o recurso mais escasso da Etapa 4. Corrija severidade 3 e 4 antes
> de chamar a primeira pessoa.

---

## As heurísticas

Dez de Nielsen, mais três extensões específicas deste projeto:

| Código | Heurística | Pergunta-guia neste app |
|---|---|---|
| **H1** | Visibilidade do status | O aluno sabe quando a explicação está sendo gerada, e de onde ela veio? |
| **H2** | Correspondência com o mundo real | A linguagem é a do aluno? A analogia usa o universo dele **corretamente**? |
| **H3** | Controle e liberdade | Dá para desligar a personalização, trocar o interesse, voltar? |
| **H4** | Consistência e padrões | Mesmos termos, ícones e posições em todas as telas? |
| **H5** | Prevenção de erros | O app evita configurações que geram explicação errada ou confusa? |
| **H6** | Reconhecer em vez de lembrar | As opções estão visíveis, sem exigir lembrar o que viu antes? |
| **H7** | Flexibilidade e eficiência | Atalho para quem já sabe? Níveis de profundidade? |
| **H8** | Estética e design minimalista | A analogia virou enfeite? Há informação irrelevante competindo? |
| **H9** | Reconhecer, diagnosticar e recuperar erros | Mensagem clara, com causa e saída? |
| **H10** | Ajuda e documentação | Ajuda contextual, fácil de achar? |
| **A1** | Acessibilidade perceptível | Contraste, zoom, reflow, foco, alvos → ver `auditoria-wcag.md` |
| **C1** | Carga cognitiva | Coerência, sinalização, segmentação, "onde a analogia falha" |
| **IA1** | Transparência da IA | Diz por que adaptou? Permite corrigir e avaliar a explicação? |

A1, C1 e IA1 não são enfeite acadêmico: são os três eixos do projeto
(acessibilidade, carga cognitiva, IA). Um problema de A1 ou IA1 vale tanto quanto
um de H4.

## Severidade (Nielsen, 0 a 4)

| Nota | Significado |
|---|---|
| 0 | Não é problema |
| 1 | Cosmético — corrigir se sobrar tempo |
| 2 | Menor — baixa prioridade |
| 3 | **Maior** — alta prioridade, corrigir antes do teste |
| 4 | **Catástrofe** — corrigir obrigatoriamente |

Ao atribuir, pese três coisas: **frequência** (acontece sempre ou só num caso?),
**impacto** (atrapalha ou impede?) e **persistência** (a pessoa aprende a
contornar ou sofre toda vez?).

---

## Registro individual

Uma tabela por avaliador. Salve como `heuristica-A1.md`, `heuristica-A2.md`…

| ID | Tela / local | Heurística | Problema | Evidência | Sev. | Sugestão |
|---|---|---|---|---|---|---|
| A1-01 | | | | print ou passo para reproduzir | | |
| A1-02 | | | | | | |

**Descreva o problema, não a solução.** "O botão deveria ser azul" não é um
problema; "não dá para saber que isso é clicável" é. A solução vai na última
coluna, e às vezes a melhor solução não é a primeira que vem à cabeça.

## Consolidação (o grupo, junto)

| ID | Problema consolidado | Heurística | Achado por | Sev. média | Prioridade |
|---|---|---|---|---|---|
| P01 | | | A1, A3 | | |

- Um problema achado por **vários** avaliadores costuma ser mais grave, mas um
  achado por **um só** não é menos válido — pode ser que só ele tenha olhado ali.
- Severidade média, não a maior nem a menor.
- Ordene por prioridade e marque o que será corrigido **antes** do teste.

## Depois de corrigir

- [ ] Problemas de severidade 3 e 4 corrigidos
- [ ] Registrar em `melhorias.md`: problema → heurística → o que mudou no código
- [ ] Rodar `uv run pytest` e `npx playwright test` para garantir que a correção
      não quebrou nada
- [ ] Anotar o hash do commit da versão que vai para o teste

---

## Resultado da avaliação (09/11/2026)

| | |
|---|---|
| Avaliador | **Avaliação por especialista com apoio de IA** (Claude, com a skill Lumen de IHC e acessibilidade), a ser **revisada pelos integrantes do grupo**. Não substitui a recomendação de 3 a 5 avaliadores independentes; os integrantes devem conferir cada item e acrescentar o que acharem |
| Versão avaliada | commit `54c6a6d` (estilo vidro), em modo pré-gravado (`EXPLANATION_PROVIDER=curated`) e com IA (Gemini) |
| Percurso | tarefas T1 a T6 (`protocolo-teste.md`), no celular (Pixel 7) e no computador (1280 px), nos temas claro, escuro e alto contraste, e a 320 px com texto "Enorme" |
| Evidências | capturas em `evidencias/` (o nome do arquivo indica dispositivo e passo) |

### Problemas encontrados

| ID | Problema | Heurística | Evidência | Sev. | Situação |
|---|---|---|---|---|---|
| **P03** | O termo de consentimento mostrava ao usuário uma nota de desenvolvimento: "Este texto é um modelo: adapte-o ao termo aprovado no seu projeto". Confunde e tira credibilidade justamente na tela que pede confiança | H8, H2 | `desktop-01-consentimento.jpg` | **3** | **Corrigido** |
| **P04** | O menu chamava "Leitura", e nada indicava que tamanho do texto e cores ficavam ali. A tarefa T4 ("deixe a tela mais confortável") depende de achar esse menu | H6, H10 | `desktop-11-leitura.jpg` | **3** | **Corrigido**: "Leitura e cores" |
| **P05** | Quem escolhia a versão técnica voltava para a analogia a cada parte nova e precisava clicar de novo em todas. Atinge diretamente a persona Caio, que prefere a linguagem técnica | H7, H3 | `desktop-07-versao-tecnica.jpg` | **3** | **Corrigido**: a escolha vale para as partes seguintes (DD39) |
| P01 | A 320 px com texto "Enorme", o símbolo ocupava metade da linha e o nome do app quebrava em sílabas ("Estu-dos"); o menu ocupa toda a primeira tela | A1, H8 | `desktop-13-320px-texto-enorme-alto-contraste.jpg` | 2 | **Corrigido em parte**: símbolo menor e nome sem hifenização. O menu ainda ocupa a primeira tela; o link "Pular para o conteúdo" atenua. Melhoria futura: menu recolhível |
| P02 | "Está errada" só responde "Obrigado, vamos conferir": não pergunta o que está errado e a explicação continua na tela, sem dizer o que acontece com ela | IA1, H1 | `desktop-08-esta-errada.jpg` | 2 | Registrado |
| P06 | O progresso ("parte 3 de 6") só é anunciado ao leitor de tela; quem enxerga não sabe quantas partes faltam | H1 | `desktop-05-parte-1.jpg` | 2 | **Mantido** por decisão anterior (DD19 tirou o contador da tela). Observar no teste com usuários |
| P07 | No modo com IA, a espera pode passar de um minuto e só aparece "Preparando e conferindo a explicação", sem estimativa | H1 | — (log da API) | 2 | Registrado. No modo pré-gravado a resposta é imediata |
| P08 | "Nova conversa" apaga a conversa atual sem confirmação nem como desfazer | H3, H5 | `desktop-05-parte-1.jpg` | 2 | Registrado |
| P09 | Ao chegar a 5 universos, o erro dizia só "Limite de 5 interesses.", sem dizer como liberar espaço | H9 | — | 2 | **Corrigido**: "Você já tem 5 universos guardados. Remova um em “Meus dados” para usar outro." |
| P12 | No modo pré-gravado só há analogia pronta para "futebol"; outro universo recebe a explicação padrão (com aviso) | H2, C1 | `desktop-05-parte-1.jpg` | 2 | Registrado. Para o teste: perguntar o universo no convite e preparar a explicação, ou usar a IA |
| P14 | A explicação pré-gravada do TCP diz, em "onde a comparação falha", que a janela "muda pelo controle de fluxo e de congestionamento", algo que o texto de referência não afirma. A regra que a IA precisa seguir (D6) não foi seguida pelo conteúdo escrito à mão | H2, IA1 | `desktop-06-onde-a-comparacao-falha.jpg` | 2 | Registrado: revisar o conteúdo ou acrescentar o fato ao texto de referência |
| P15 | Em "Fora deste conteúdo", o botão "Continuar este conteúdo" só leva o foco ao campo; não fica claro que algo aconteceu | H1 | `desktop-09-pergunta-fora-do-conteudo.jpg` | 2 | Registrado (achado no percurso cognitivo) |
| P10 | "Ir para a última mensagem" fica sempre visível, mesmo quando a última mensagem já está na tela | H8 | `desktop-05-parte-1.jpg` | 1 | Registrado |
| P11 | A mesma ação tinha dois nomes: "Escolher outro conteúdo" (na recusa) e "Estudar outro conteúdo" (no fim da explicação) | H4 | `desktop-09-pergunta-fora-do-conteudo.jpg` | 1 | **Corrigido**: "Estudar outro conteúdo" nos dois |

**Resumo:** 14 problemas; nenhum de severidade 4; os **3 de severidade 3 foram corrigidos** antes de qualquer teste com usuários, como o método pede; dos 9 de severidade 2, 2 foram corrigidos (P01 em parte, P09) e 7 ficaram registrados; dos 2 de severidade 1, 1 foi corrigido. Depois das correções, os 106 testes da API e os 44 testes de ponta a ponta (com verificação automática de acessibilidade) passam.

### Pontos fortes observados

- **Controle do usuário sobre a personalização** (H3, DP05): versão técnica a um toque, troca de universo dentro da explicação, explicação padrão como reserva.
- **Transparência da IA** (IA1): aviso de explicação adaptada, aviso de referência sem fontes (DD37), fontes exibidas quando há pesquisa na web, "Está errada" em toda parte.
- **Prevenção de erros de conteúdo** (H5): autoverificação e validadores barram explicação errada antes de chegar ao aluno.
- **Recuperação** (H9): assunto fora da biblioteca e pergunta fora do conteúdo nunca terminam em beco sem saída; há sempre sugestões.

## O que este método não faz

Avaliação heurística é **analítica**: feita por quem conhece o sistema, sem
usuários. Ela encontra muitos problemas baratos, e por isso vem primeiro. Mas:

- **não substitui o teste com usuários.** Vocês sabem onde os botões estão, e
  isso torna impossível avaliar descoberta;
- **não revela o que o usuário entendeu.** Se a analogia ensina ou confunde, só o
  teste responde;
- **tende a achar problemas de interface e perder problemas de conteúdo.**

Diga isso no relatório. Reconhecer o limite do método é parte da análise.

## Fontes

- **Nielsen** — as 10 heurísticas, a escala de severidade 0 a 4 e a recomendação
  de 3 a 5 avaliadores independentes antes da consolidação.
- **Nielsen** — corrigir problemas graves **antes** das sessões com usuários, para
  não gastar tempo de participante com defeito óbvio.
- `references/metodos-de-avaliacao.md`; `assets/templates/avaliacao-heuristica.md`.
