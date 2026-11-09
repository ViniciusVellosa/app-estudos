# Documentação do projeto

App de apoio a estudos que explica conteúdos técnicos usando o universo de
interesse do aluno. Projeto da disciplina de **Interação Humano-Computador** —
UNIARA, Engenharia da Computação. Entrega: **09/11/2026**.

## Tecnologias

| Parte | Linguagem | Principais ferramentas |
|---|---|---|
| Front-end (`apps/web`) | **TypeScript**, com HTML e CSS | React 19, Vite; aplicação web responsiva (celular e computador) |
| Back-end (`apps/api`) | **Python 3.12+** | FastAPI, Pydantic v2, SQLAlchemy 2; SDKs da Anthropic/OpenAI para a IA |
| Banco de dados | **SQL** | PostgreSQL 18 |
| Infraestrutura | YAML (Compose) e Dockerfile | Docker Compose: `docker compose up --wait` |
| Testes | Python e TypeScript | pytest (API); Playwright + axe-core (ponta a ponta e acessibilidade) |

## Por etapa

O ciclo da disciplina é **Entender → Desenhar → Avaliar**. Cada pasta é uma etapa:

| Etapa | Pasta | O que tem | Estado |
|---|---|---|---|
| **1. Pesquisa com usuários** *(Entender)* | [`etapa-1-pesquisa/`](etapa-1-pesquisa/) | Plano de pesquisa, instrumento do questionário e síntese dos resultados (.docx); base anonimizada R01–R05 | Concluída: n = 5, coleta de 02 a 07/11 |
| **2. Personas e cenários** *(Define)* | [`etapa-2-personas-cenarios/`](etapa-2-personas-cenarios/) | Personas (Ana, Rafael, Caio), PACT e cenários com claims e tarefas T1–T5 (.docx) | Concluída em 07/11 com os dados da Etapa 1 |
| **3. Prototipação** *(Desenhar)* | [`etapa-3-prototipo/`](etapa-3-prototipo/) | O app em `apps/` é o protótipo de alta fidelidade; tokens de cor já validados | Concluída: esboços de baixa fidelidade, `decisoes-de-design.md` (DD01–DD39) e o app com as decisões D1–D9 |
| **4. Avaliação** *(Avaliar)* | [`etapa-4-avaliacao/`](etapa-4-avaliacao/) | Avaliação heurística, percurso cognitivo, auditoria WCAG, evidências, resultados e melhorias; protocolo do teste e SUS validado | Avaliação analítica concluída em 09/11 (heurística, percurso cognitivo, auditoria WCAG; `resultados.md`, `melhorias.md`). Teste com usuários e SUS: instrumentos prontos, não aplicados |

## Transversal — não pertence a uma etapa só

| Pasta | O que é | Por que fica fora das etapas |
|---|---|---|
| [`requisitos/`](requisitos/) | Requisitos funcionais (RF) e não funcionais (RNF), com rastreio e critérios de aceite | É **saída da Etapa 2** na metodologia, mas o código e os testes apontam para ele; mover quebraria essa ligação. Rastreio preenchido com os dados da Etapa 1; inclui as decisões de projeto D1–D6 (07/11) |
| [`adr/`](adr/) | Registros de decisão de arquitetura | Decisões de engenharia, tomadas e revisadas ao longo de todo o projeto. O ADR 0002 (revisão humana) será substituído em parte pelo 0003 (autoverificação da IA, decisão D6) |

## A cadeia de rastreabilidade

É o que diferencia um projeto de IHC de uma coleção de artefatos soltos. Cada elo
está em uma pasta diferente, e cada documento diz de onde vem o que afirma:

```
achado da pesquisa          → etapa-1-pesquisa/sintese.docx
  → persona / cenário       → etapa-2-personas-cenarios/
    → requisito (RF/RNF)    → requisitos/requisitos.md
      → decisão de design   → etapa-3-prototipo/decisoes-de-design.md
        → elemento no código→ apps/web, apps/api
          → tarefa do teste → etapa-4-avaliacao/protocolo-teste.md
            → resultado     → etapa-4-avaliacao/resultados.md
              → melhoria    → etapa-4-avaliacao/melhorias.md
```

## Códigos usados nos documentos

| Prefixo | O que é | Onde está definido |
|---|---|---|
| **RF**, **RNF** | Requisito funcional e não funcional | `requisitos/requisitos.md` |
| **RA** | Requisito de acessibilidade (RA01–RA24) | Biblioteca do Lumen, `references/acessibilidade.md` |
| **DP** | Diretriz de personalização (DP01–DP18) | Biblioteca do Lumen, `references/carga-cognitiva-e-personalizacao.md` |
| **H**, **A1**, **C1**, **IA1** | Heurísticas de Nielsen e extensões do projeto | `etapa-4-avaliacao/avaliacao-heuristica.md` |
| **T1–T5** | Tarefas do teste de usabilidade | `etapa-2-personas-cenarios/cenarios.docx` |
| **D1–D6** | Decisões de projeto tomadas antes da Etapa 3 | `requisitos/requisitos.md` |
| **P1, P2…** · **R01, R02…** | Participante de conversa · respondente do questionário | `etapa-1-pesquisa/` |

## Rótulos de origem

Os documentos marcam de onde vem cada afirmação. **Não apague os rótulos** — eles
são o que torna a entrega defensável numa arguição:

- `[questionário: item N]` — dado real da Etapa 1, com a contagem sobre n = 5
- `[hipótese da equipe]` — suposição; mantém o rótulo no relatório
- `[da literatura]` — vem de fonte citada, não dos seus dados
- **(a confirmar)** / **(manual)** — não apresentar como fato consolidado

## Ordem sugerida até 09/11

Concluído: questionário aplicado (n = 5), síntese, personas, PACT, cenários, rastreio dos requisitos e decisões D1–D6.

Falta:
1. Esboços de baixa fidelidade e `etapa-3-prototipo/decisoes-de-design.md`
2. ADR 0003 (autoverificação da IA) e implementação das decisões D1–D6 no app, com testes
3. Avaliação heurística em grupo; corrigir severidade 3 e 4
4. Auditoria WCAG (automática + checklist manual)
5. Teste com 3 a 5 pessoas de fora do grupo, com SUS
6. `etapa-4-avaliacao/resultados.md` e `melhorias.md`
7. **09/11:** apagar os dados da pesquisa (Forms e CSV), como prometido aos participantes
