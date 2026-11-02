# Etapa 3 — Prototipação (Desenhar)

> **Boa parte desta etapa já está entregue, em código.** Este arquivo diz onde cada
> coisa está e o que falta.

## O protótipo de alta fidelidade é o próprio app

Não há Figma a fazer: o app funcional no repositório **é** o protótipo de alta
fidelidade. Houde e Hill lembram que protótipo é "qualquer representação de uma
ideia de design, independente do meio" — e um app que roda representa melhor do que
uma tela estática, especialmente nas três dimensões que importam aqui:

| Dimensão (Houde e Hill) | Onde está |
|---|---|
| **Role** — que papel tem na vida do usuário | O fluxo de seis passos em `apps/web/src/App.tsx` |
| **Look and feel** — o que se vê e sente | Tokens em `apps/web/src/styles/tokens.css`; temas claro, escuro e alto contraste |
| **Implementation** — como funciona | API em `apps/api`, com os dois provedores de explicação |

Rodar para demonstrar:

```bash
docker compose up --wait
```

## Design tokens — já validados

A paleta está em `apps/web/src/styles/paleta-contraste.json` e os tokens em
`apps/web/src/styles/tokens.css`.

**Verificado em 02/11/2026:** os **22 pares de cor passam** `1.4.3 Contraste
mínimo (AA)` **e** `1.4.6 Contraste melhorado (AAA, 7:1)` nos três temas. O menor
valor foi 5,33:1, numa borda, onde o critério aplicável é `1.4.11` e exige 3:1.
Isso cumpre a meta com estrela do requisito RA01.

Reproduzir o resultado:

```bash
python .claude/skills/lumen-ihc-acessibilidade/scripts/contrast_check.py --palette apps/web/src/styles/paleta-contraste.json
```

Cole essa saída no relatório. É resultado medido, não afirmação.

## O que falta para fechar a etapa

- [ ] **Baixa fidelidade.** Esboço em papel ou wireframe das telas principais,
      fotografado. É o que mostra que houve processo de design, e não só código
      escrito direto. Mesmo rascunho a lápis serve — e é rápido
- [ ] **`decisoes-de-design.md`** neste diretório: cada decisão visual apontando
      para um achado da Etapa 1, uma persona da Etapa 2 ou um critério WCAG.
      Formato: *decisão → origem → critério*
- [ ] Frames ou prints em **320px de largura**, para o relatório mostrar o reflow
      (o CI já testa isso; aqui é a evidência visual)
- [ ] Print dos três temas lado a lado

### Por que a baixa fidelidade importa, mesmo com o app pronto

O professor avalia o **processo**, não só o produto. Um app bonito sem rastro de
design parece ter nascido pronto. Dois rascunhos a lápis, datados e com anotação do
que mudou depois, mostram iteração — que é o princípio (4) da ISO 9241-210.

Se os esboços foram feitos depois do código, **diga isso**. Registrar a ordem real
vale mais que fingir um processo linear que não aconteceu.

## Rastreabilidade

```
achado (Etapa 1) → persona/cenário (Etapa 2) → decisão de design (aqui) →
elemento no código → tarefa do teste (Etapa 4)
```

Decisões que já estão tomadas no código e precisam ser **registradas** aqui com sua
origem:

| Decisão no código | Origem |
|---|---|
| Explicação em seis passos, um por tela, com progresso | RA23, DP13 — segmentação e ritmo do aluno |
| Botão "ver sem analogia" sempre visível | RF04, RA21, DP05 — e a pergunta 11 do questionário |
| Três temas: claro, escuro e alto contraste | RF06, RA01, RA20 — e a pergunta 13 |
| Tabela de mapeamento que empilha a 320px | RA05, `1.4.10 Realinhar (AA)` |
| Região viva anunciando "explicação pronta" | RA13, `4.1.3 Mensagens de status (AA)` |

## Fontes

- **Houde e Hill (1997)** — "What do prototypes prototype?": role, look and feel,
  implementation; e o aviso de que protótipos não são autoexplicativos.
- **ISO 9241-210:2019** — princípio (4), processo iterativo.
- **WCAG 2.2** (W3C) — critérios citados por número e nível.
- `references/processo-de-design.md` §5; `references/acessibilidade.md` (RA01–RA24).
