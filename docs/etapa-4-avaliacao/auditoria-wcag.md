# Auditoria WCAG 2.2 — Etapa 4 (Avaliar)

Objeto: o app em `apps/web`, versão [preencher: hash do commit].
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
