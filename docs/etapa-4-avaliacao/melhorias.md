# Melhorias — Etapa 4 (Avaliar)

Cada linha liga um problema encontrado na avaliação ao que mudou no app.
Problemas de `avaliacao-heuristica.md` (P) e `percurso-cognitivo.md`; critérios
de `auditoria-wcag.md`.

## Corrigidas em 09/11/2026

| Problema | Heurística / critério | Sev. | O que mudou | Onde |
|---|---|---|---|---|
| P03 — nota de desenvolvimento no consentimento | H8, H2 | 3 | Nota retirada | `apps/web/src/App.tsx` |
| P04 — menu "Leitura" não indicava as cores | H6, H10 | 3 | Rótulo "Leitura e cores" | `apps/web/src/App.tsx` |
| P05 — versão técnica voltava à analogia a cada parte | H7, H3 · persona Caio | 3 | A escolha vale para as partes seguintes; estudar outro conteúdo restaura o padrão (DD39) | `apps/web/src/chat/Chat.tsx`; teste `fluxo-principal.spec.ts` |
| P01 — nome do app quebrado em sílabas a 320 px com texto enorme | A1, H8 | 2 | Símbolo menor com texto ampliado; nome sem hifenização | `apps/web/src/styles/base.css` |
| P09 — erro do limite de universos sem saída | H9 | 2 | Mensagem diz como liberar espaço ("Remova um em Meus dados") | `apps/api/app/routers/me.py` |
| P11 — mesma ação com dois nomes | H4 | 1 | "Estudar outro conteúdo" nos dois lugares | `apps/web/src/chat/Chat.tsx` |
| Auditoria — tema escuro sem verificação automática | `1.4.3`, `1.4.11` | — | Novo teste de ponta a ponta com axe no tema escuro e estilo vidro | `apps/web/e2e/acessibilidade-chat.spec.ts` |

Depois das correções: 106 testes da API e 44 de ponta a ponta passando.

## Registradas para a próxima iteração

| Problema | Heurística / critério | Sev. | Proposta |
|---|---|---|---|
| P12 — só há analogia pré-gravada para "futebol" | H2, C1 | 2 (bloqueia o teste) | Escrever as explicações dos universos dos participantes antes do teste, ou usar a IA |
| P02 — "Está errada" não pergunta o motivo nem diz o que acontece | IA1, H1 | 2 | Perguntar "o que está errado?" com opções curtas e informar que a explicação sai de circulação |
| P06 — progresso só para leitor de tela | H1 | 2 | Rever DD19 com o resultado do teste com usuários |
| P07 — espera da IA sem estimativa | H1 | 2 | Mostrar a etapa em curso ("escrevendo", "conferindo") |
| P08 — "Nova conversa" sem confirmação | H3, H5 | 2 | Confirmar ou permitir desfazer |
| P14 — conteúdo pré-gravado afirma algo fora do texto de referência | H2, IA1 | 2 | Revisar o "onde a comparação falha" do TCP ou acrescentar o fato ao texto de referência |
| P15 — "Continuar este conteúdo" sem retorno | H1 | 2 | Mensagem curta no chat ("Pode perguntar outra coisa sobre…") |
| P01 (resto) — menu ocupa a primeira tela com texto ampliado | A1 | 2 | Menu recolhível |
| P10 — "Ir para a última mensagem" sempre visível | H8 | 1 | Mostrar só quando a última mensagem estiver fora da tela |
| Títulos `h1` → `h3` no chat | `1.3.1 (A)` | 1 | Usar `h2` nos títulos das partes |
