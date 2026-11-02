# ADR 0001 — Stack do projeto

- **Status:** aceita
- **Data:** AAAA-MM-DD
- **Decisores:** (nomes da equipe)

## Contexto
A pesquisa com usuários indicou que os alunos estudam principalmente pelo
celular (ônibus, à noite). O projeto precisa cumprir WCAG 2.2 AA, ter
avaliação com usuários (incluindo pessoa com baixa visão) e caber no prazo da
disciplina. A equipe conhece Python e um pouco de React.

## Decisão
Web mobile-first (React + Vite + TypeScript), API em Python com FastAPI,
PostgreSQL, tudo em Docker Compose. A IA fica atrás de uma interface e pode
ser desligada (`EXPLANATION_PROVIDER=curated`).

## Alternativas consideradas
- **App nativo / React Native:** acesso a recursos do celular, mas testes de
  acessibilidade automatizados mais fracos e publicação em loja.
- **Supabase/Firebase:** mais rápido, mas menos aprendizado de back-end e
  dados em provedor externo (LGPD).
- **Node.js no back-end:** uma linguagem só; a equipe domina mais Python.

## Consequências
- (+) Roda no navegador do celular sem instalação; axe e Playwright no CI.
- (+) `docker compose up` sobe o projeto em qualquer máquina.
- (−) Sem recursos nativos (notificações push limitadas).
