# Documentação do projeto

App de apoio a estudos que explica conteúdos técnicos usando o universo de
interesse do aluno. Projeto da disciplina de **Interação Humano-Computador** —
UNIARA, Engenharia da Computação. Entrega: **09/11/2026**.

## Por etapa

O ciclo da disciplina é **Entender → Desenhar → Avaliar**. Cada pasta é uma etapa:

| Etapa | Pasta | O que tem | Estado |
|---|---|---|---|
| **1. Pesquisa com usuários** *(Entender)* | [`etapa-1-pesquisa/`](etapa-1-pesquisa/) | Plano, questionário por WhatsApp, consentimento, roteiro de conversa opcional | Instrumentos prontos; falta coletar |
| **2. Personas e cenários** *(Define)* | [`etapa-2-personas-cenarios/`](etapa-2-personas-cenarios/) | Personas, PACT, cenários com claims, tarefas T1–T5 | Estruturado; campos esperam os dados da Etapa 1 |
| **3. Prototipação** *(Desenhar)* | [`etapa-3-prototipo/`](etapa-3-prototipo/) | O app em `apps/` é o protótipo de alta fidelidade; tokens já validados | Falta baixa fidelidade e o registro de decisões |
| **4. Avaliação** *(Avaliar)* | [`etapa-4-avaliacao/`](etapa-4-avaliacao/) | Protocolo do teste, SUS validado, avaliação heurística, auditoria WCAG | Instrumentos prontos; falta executar |

## Transversal — não pertence a uma etapa só

| Pasta | O que é | Por que fica fora das etapas |
|---|---|---|
| [`requisitos/`](requisitos/) | Requisitos funcionais (RF) e não funcionais (RNF), com rastreio e critérios de aceite | É **saída da Etapa 2** na metodologia, mas o código e os testes apontam para ele; mover quebraria essa ligação. A coluna "Rastreio" é preenchida ao fim da Etapa 1 |
| [`adr/`](adr/) | Registros de decisão de arquitetura | Decisões de engenharia, tomadas e revisadas ao longo de todo o projeto |

## A cadeia de rastreabilidade

É o que diferencia um projeto de IHC de uma coleção de artefatos soltos. Cada elo
está em uma pasta diferente, e cada documento diz de onde vem o que afirma:

```
achado da pesquisa          → etapa-1-pesquisa/sintese.md
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
| **T1–T5** | Tarefas do teste de usabilidade | `etapa-2-personas-cenarios/cenarios.md` |
| **P1, P2…** · **R01, R02…** | Participante de conversa · respondente do questionário | `etapa-1-pesquisa/` |

## Rótulos de origem

Os documentos marcam de onde vem cada afirmação. **Não apague os rótulos** — eles
são o que torna a entrega defensável numa arguição:

- `[questionário: pergunta N]` — preencher com dado real da Etapa 1
- `[hipótese da equipe]` — suposição; mantém o rótulo no relatório
- `[da literatura]` — vem de fonte citada, não dos seus dados
- **(a confirmar)** / **(manual)** — não apresentar como fato consolidado

## Ordem sugerida até 09/11

1. Enviar o questionário (`etapa-1-pesquisa/questionario.md`) — depende de outras
   pessoas responderem, então é o primeiro a sair
2. Tabular e escrever `etapa-1-pesquisa/sintese.md`
3. Preencher os campos `[questionário: pergunta N]` da Etapa 2 e a coluna
   "Rastreio" dos requisitos
4. Esboços de baixa fidelidade e `decisoes-de-design.md` (Etapa 3)
5. Avaliação heurística em grupo, corrigir severidade 3 e 4
6. Teste com 3 a 5 pessoas de fora do grupo, com SUS
7. `resultados.md` e `melhorias.md`
