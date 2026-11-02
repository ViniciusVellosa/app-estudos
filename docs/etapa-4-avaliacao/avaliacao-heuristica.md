# Avaliação heurística — Etapa 4 (Avaliar)

| | |
|---|---|
| Avaliadores | **Os integrantes do grupo** — 3 a 5 pessoas |
| Como | Cada um avalia **sozinho primeiro**, depois o grupo consolida |
| Objeto | O app em `apps/web`, versão [preencher: hash do commit] |
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
