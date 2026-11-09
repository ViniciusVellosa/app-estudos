# Auditoria WCAG 2.2 — Etapa 4 (Avaliar)

Objeto: o app em `apps/web`, versão `54c6a6d` com as correções da avaliação heurística (ver o resultado na seção 2.1).
Meta do projeto: **WCAG 2.2 nível AA** (requisito RNF01).

> **Boa notícia antes de começar:** boa parte do automatizável **já está feita e
> rodando no CI**. A seção 1 lista o que você pode marcar como coberto e citar no
> relatório; a seção 2 é o que falta, e é onde está o trabalho real.

---

## 1. O que o CI já verifica — e passa

O arquivo `apps/web/e2e/fluxo-principal.spec.ts` roda no CI a cada push (job
`e2e`, workflow `.github/workflows/ci.yml`) e cobre:

| Verificação | Como | Critério |
|---|---|---|
| Regras automáticas do axe no fluxo principal | `@axe-core/playwright` (`AxeBuilder`) | vários, incluindo `1.4.3`, `1.3.1`, `4.1.2`, `3.1.1` |
| **Sem rolagem horizontal a 320px** de largura — equivale a 1280px com zoom de 400% | `page.setViewportSize({ width: 320 })` | **`1.4.10 Realinhar (AA)`** |
| Texto ampliado e **alto contraste** permanecem usáveis | ativa o controle de alto contraste e revalida | `1.4.3`, `1.4.4` |
| **Uso só com teclado** no fluxo completo | teste "dá para usar só com o teclado" | `2.1.1 Teclado (A)`, `2.4.3 Ordem do foco (A)` |
| Nos dois formatos | projetos `celular` (Pixel 7) e `desktop` | — |

Rodar localmente:

```bash
npx playwright test
```

Para o relatório, cite o resultado com data e a execução do CI. **Não escreva que
"o app é acessível" porque o axe passou** — veja a seção 3.

### Contraste da paleta

O projeto tem a paleta em `apps/web/src/styles/paleta-contraste.json` e a skill traz
o verificador. Rode e cole a saída no relatório:

```bash
python .claude/skills/lumen-ihc-acessibilidade/scripts/contrast_check.py --palette apps/web/src/styles/paleta-contraste.json
```

Meta do projeto: **≥ 4,5:1** no texto normal (`1.4.3 AA`) e, nas explicações,
**≥ 7:1** (`1.4.6 AAA`), conforme RA01.

---

## 2. O que exige verificação manual

Nenhuma ferramenta automática cobre o que está abaixo. É aqui que você gasta a
tarde — marque ✅ passa, ❌ falha, ➖ não se aplica, e registre a evidência.

### Ampliação e layout

| # | Verificação | Como testar | Critério | Result. |
|---|---|---|---|---|
| 1 | Zoom de **200% no navegador** sem perda de conteúdo ou função | `Ctrl` + `+` até 200% | `1.4.4 (AA)` | |
| 2 | **Espaçamento de texto** ajustado (linha 1,5; parágrafo 2×; letra 0,12em; palavra 0,16em) sem cortar texto | bookmarklet de text spacing | `1.4.12 (AA)` | |
| 3 | Zoom **não bloqueado**: sem `user-scalable=no` nem `maximum-scale=1` | inspecionar a meta viewport em `apps/web/index.html` | `1.4.4 (AA)` | |
| 4 | Aumentar a **fonte do sistema** (Android/iOS) aumenta o texto do app | configurações do celular | `1.4.4 (AA)` | |
| 5 | Tooltip ou popover persiste, fecha com `Esc` e não cobre conteúdo | mouse e `Tab` | `1.4.13 (AA)` | |

> O item 1 **não** é redundante com o teste de 320px do CI: viewport estreita e
> zoom de navegador são mecanismos diferentes, e um pode passar enquanto o outro
> falha.

### Foco

| # | Verificação | Como testar | Critério | Result. |
|---|---|---|---|---|
| 6 | Foco **sempre visível**, contorno ≥ 2px e contraste ≥ 3:1 | navegar só com `Tab`, olhando | `2.4.7 (AA)` | |
| 7 | Foco **não escondido** por cabeçalho ou rodapé fixo | `Tab` com zoom a 200% | `2.4.11 (AA)` | |
| 8 | Alvos de toque ≥ 24×24px (meta do projeto: 44×44) | medir no DevTools | `2.5.8 (AA)` | |

### Conteúdo e leitor de tela

| # | Verificação | Como testar | Critério | Result. |
|---|---|---|---|---|
| 9 | Hierarquia de títulos `h1`–`h3` na explicação, e landmarks | NVDA: lista de títulos (`Insert`+`F7`) | `1.3.1 (A)` | |
| 10 | Texto alternativo das analogias descreve **a relação**, não só a cena | leitor de tela | `1.1.1 (A)` | |
| 11 | Botões anunciam nome, função **e estado** (ex.: `aria-pressed` no modo analogia) | leitor de tela | `4.1.2 (A)` | |
| 12 | "Explicação pronta" é **anunciada** por região viva, **sem roubar o foco** | NVDA com a explicação carregando | `4.1.3 (AA)` | |
| 13 | Instruções não dependem de posição ou cor ("o botão roxo à direita") | revisar os textos da interface | `1.3.3 (A)` | |
| 14 | Informação nunca só por cor (erro, selecionado, obrigatório) | ver em escala de cinza | `1.4.1 (A)` | |

> Os itens 10 a 12 são os que o axe **nunca** pega: ele confirma que existe um
> `alt`, não que o `alt` presta; confirma que há `aria-live`, não que o anúncio faz
> sentido.

### Carga cognitiva

| # | Verificação | Critério | Result. |
|---|---|---|---|
| 15 | Ajuda no mesmo lugar em todas as telas | `3.2.6 (A)` | |
| 16 | Não pede de novo um dado já informado | `3.3.7 (A)` | |
| 17 | Sem limite de tempo nas atividades, ou ajustável | `2.2.1 (A)` | |
| 18 | Animações pausáveis; respeita `prefers-reduced-motion` | `2.2.2 (A)` | |
| 19 | Explicação técnica, sem analogia, a um toque | RA21, DP05 | |

### Como testar com leitor de tela, se você nunca usou

**NVDA** (Windows, gratuito): `Insert` liga e desliga a fala, `Insert`+`F7` lista
títulos e links, `Tab` navega pelos controles, `H` salta de título em título.

Reserve 20 minutos para se acostumar **antes** de auditar, e feche os olhos ou
desligue o monitor em parte do teste — enquanto você vê a tela, você não está
testando o leitor de tela, está conferindo se ele concorda com o que você já sabe.

---

## 2.1 Resultado da auditoria (09/11/2026)

Feita por especialista com apoio de IA (Claude, skill Lumen), com as evidências
em `evidencias/`. O que exige aparelho físico ou leitor de tela ficou marcado como
**não verificado**, e não como aprovado.

### Verificação automatizada

| Verificação | Resultado |
|---|---|
| axe (regras WCAG 2.0, 2.1 e 2.2, níveis A e AA) em todas as etapas do fluxo, no celular e no computador, nos três temas | ✅ sem violações (44 testes de ponta a ponta passando, incluindo um novo para o tema escuro com o estilo vidro) |
| Sem rolagem horizontal a 320 px com texto "Enorme" e alto contraste | ✅ `desktop-13-320px-texto-enorme-alto-contraste.jpg` |
| Paleta: 34 pares de cor (`paleta-contraste.json`) | ✅ 34 de 34 passam em `1.4.3`; os de texto também em `1.4.6 (AAA)` |
| Alvos de toque (teste `alvosGrandesOSuficiente`) | ✅ todos ≥ 24 × 24 px; botões com 44 px de altura |

### Contraste sobre o estilo vidro (DD38)

O fundo do estilo vidro tem manchas de cor, então o contraste foi medido no
**pior ponto**: a cor mais escura do fundo no tema claro (`#c4d5fd`) e a mais
clara no escuro (`#1a2b59`), lidas das capturas de tela. O texto em superfícies
de vidro fica sobre 72% a 85% de branco (ou azul-noite) e tem contraste maior que
o da tabela.

| Texto | Tema | Pior fundo | Contraste | `1.4.3 (AA)` | `1.4.6 (AAA)` |
|---|---|---|---|---|---|
| Texto principal `#0f1b2d` | claro | `#c4d5fd` | 11,76:1 | ✅ | ✅ |
| Texto secundário `#3d4a5c` | claro | `#c4d5fd` | 6,12:1 | ✅ | ❌ (só AA) |
| Links e botões `#12499c` | claro | `#c4d5fd` | 5,81:1 | ✅ | ❌ (só AA) |
| Alerta `#a3141c` | claro | `#c4d5fd` | 5,34:1 | ✅ | ❌ (só AA) |
| Texto principal `#e8eefb` | escuro | `#1a2b59` | 11,77:1 | ✅ | ✅ |
| Texto secundário `#b3c2da` | escuro | `#1a2b59` | 7,59:1 | ✅ | ✅ |
| Links e botões `#8fb8ff` | escuro | `#1a2b59` | 6,83:1 | ✅ | ❌ (só AA) |
| Alerta `#ffb3b3` | escuro | `#1a2b59` | 8,05:1 | ✅ | ✅ |

O texto das explicações (texto principal) mantém a meta AAA de RA01 nos dois
temas. Textos secundários, links e alertas ficam em AA no pior ponto do fundo:
atende à meta do projeto (WCAG 2.2 AA), mas não à meta "com estrela" de RA01
para esses elementos. No tema de alto contraste não há vidro (21:1).

### Checklist manual (seção 2)

| # | Verificação | Critério | Resultado | Evidência / observação |
|---|---|---|---|---|
| 1 | Zoom de 200% sem perda | `1.4.4 (AA)` | ✅ | Por equivalência: 200% numa tela de 1280 px equivale a 640 px de largura, e o app reflui até 320 px (400%) sem perda |
| 2 | Espaçamento de texto | `1.4.12 (AA)` | ✅ | Estilo de teste injetado (linha 1,5; parágrafo 2×; letra 0,12em; palavra 0,16em): nenhum texto cortado, sem rolagem lateral. `*-14-espacamento-de-texto.jpg` |
| 3 | Zoom não bloqueado | `1.4.4 (AA)` | ✅ | `index.html`: `width=device-width, initial-scale=1`, sem `user-scalable=no` nem `maximum-scale` |
| 4 | Fonte do sistema aumenta o texto | `1.4.4 (AA)` | ➖ não verificado | Precisa de aparelho. O CSS usa `rem` sobre 100% da fonte do navegador, o que deveria respeitar o ajuste |
| 5 | Tooltip / popover | `1.4.13 (AA)` | ➖ não se aplica | O app não tem tooltips nem popovers |
| 6 | Foco visível, ≥ 2px, ≥ 3:1 | `2.4.7 (AA)` | ✅ | Contorno de 3 px na cor `--focus`: 7,88:1 no claro, 9,33:1 no escuro, amarelo no alto contraste |
| 7 | Foco não encoberto pelo cabeçalho ou rodapé fixos | `2.4.11 (AA)` | ✅ | Teste automatizado do rodapé + `scroll-padding`; no celular e com texto ampliado, cabeçalho e rodapé deixam de ser fixos |
| 8 | Alvos ≥ 24 × 24 px | `2.5.8 (AA)` | ✅ | Teste automatizado; meta de 44 px atendida nos botões |
| 9 | Títulos e landmarks | `1.3.1 (A)` | ⚠️ | `header`, `nav` e `main` presentes. No chat, os títulos das partes são `h3` logo abaixo de um `h1` (sem `h2`): não viola o critério, mas é má prática para quem navega por títulos. Severidade 1 |
| 10 | Texto alternativo das analogias | `1.1.1 (A)` | ➖ não se aplica | Não há imagens de conteúdo; o símbolo do app é decorativo (`aria-hidden`) |
| 11 | Nome, função e estado dos botões | `4.1.2 (A)` | ✅ no código, ➖ não ouvido | `aria-pressed` no botão da versão técnica, conferido pelos testes. Não foi ouvido com NVDA ou TalkBack |
| 12 | "Explicação pronta" anunciada sem roubar o foco | `4.1.3 (AA)` | ✅ no código, ➖ não ouvido | `role="log"` com `aria-live="polite"` e região de status; teste automatizado confirma que o foco não muda. Não foi ouvido com leitor de tela |
| 13 | Instruções sem depender de posição ou cor | `1.3.3 (A)` | ✅ | Revisão dos textos: nenhum "botão à direita" ou "botão azul" |
| 14 | Informação não só por cor | `1.4.1 (A)` | ✅ | Estados dizem em texto ("Voltar para a comparação", "Fora deste conteúdo", "Obrigado, vamos conferir") |
| 15 | Ajuda no mesmo lugar | `3.2.6 (A)` | ➖ não se aplica | O critério vale quando há mecanismo de ajuda; o app não tem. O aviso fixo sob o campo fica sempre no mesmo lugar |
| 16 | Não pedir de novo um dado já informado | `3.3.7 (A)` | ✅ | Universos já usados voltam como sugestões clicáveis |
| 17 | Sem limite de tempo | `2.2.1 (A)` | ✅ | Nenhuma atividade tem tempo |
| 18 | Animações pausáveis; `prefers-reduced-motion` | `2.2.2 (A)` | ✅ | A única animação são os pontinhos de espera, desligados por `prefers-reduced-motion` e pela opção "Reduzir animações" |
| 19 | Versão técnica a um toque | RA21, DP05 | ✅ | E a escolha vale para as partes seguintes (DD39) |

### Resumo

- **Automatizado:** nenhuma violação nas regras WCAG A e AA do axe, em todo o
  fluxo, nos dois formatos e nos três temas.
- **Manual:** 13 itens aprovados, 1 com observação de severidade 1 (títulos),
  5 sem aplicação ou não verificáveis aqui.
- **Não verificado:** leitor de tela (NVDA, TalkBack) e ajuste de fonte do
  sistema em aparelho físico. Precisam de alguém com o equipamento, de
  preferência uma pessoa que use essas tecnologias no dia a dia.

## 3. O que escrever no relatório, e o que não escrever

**Não escreva:** "o app está em conformidade com a WCAG 2.2 AA".

**Escreva:** "o app foi avaliado contra a WCAG 2.2 nível AA por verificação
automatizada (axe no CI, sem erros críticos em [data]) e por checklist manual de
19 itens, com [n] falhas identificadas e [n] corrigidas. Ferramentas automáticas
cobrem apenas parte dos critérios, e a auditoria não incluiu teste com usuários
com deficiência além de [o que você conseguiu fazer]."

A diferença entre as duas frases é a diferença entre uma afirmação que não se
sustenta e uma que você pode defender item por item. **Ferramenta automática pega
só uma parte dos problemas** — diga isso explicitamente; é um dos pontos que a
disciplina cobra.

## 4. Fechamento

- [ ] Checklist da seção 2 preenchido com evidência
- [ ] Falhas registradas como problemas, com severidade, junto das da avaliação
      heurística
- [ ] Falhas de severidade 3 e 4 corrigidas **antes** do teste com usuários
- [ ] Cada correção registrada em `melhorias.md`: critério → o que mudou
- [ ] `npx playwright test` e `uv run pytest` passando depois das correções

## Fontes

- **WCAG 2.2** (W3C) — todos os critérios citados por número e nível.
- **W3C WAI** — orientação de que ferramentas automáticas cobrem parte dos
  critérios e não substituem avaliação manual nem teste com usuários.
- **Low Vision Task Force / COGA** (W3C) — base de RA20 a RA23.
- `references/acessibilidade.md` (RA01 a RA24);
  `assets/templates/checklist-baixa-visao.md`; `scripts/contrast_check.py`.
- Cobertura automatizada: `apps/web/e2e/fluxo-principal.spec.ts` e
  `.github/workflows/ci.yml`.
