# App de Estudos — projeto-base

App web (mobile-first) que explica conteúdos usando o universo de interesse
do aluno, com foco em personalização, carga cognitiva e acessibilidade
(WCAG 2.2). Gerado pela skill **Dédalo**; a parte de IHC é do **Lumen**.

## O que já funciona
- Sessão anônima (sem nome nem e-mail), consentimento e interesses.
- Explicação em seis passos: conceito → cena → quem é quem → onde a
  comparação falha → explicação técnica → pergunta de transferência.
- Explicação padrão (sem analogia) sempre a um toque.
- Motor de explicações **sem IA** (explicações escritas à mão) ou **com IA**
  (Claude ou modelo local via Ollama), com validadores anti-erro e revisão humana.
- Preferências de leitura: tamanho do texto, tema claro/escuro/alto contraste,
  redução de animações.
- "Meus dados": ver e apagar tudo (LGPD).
- Testes: 27 da API (pytest, em SQLite e PostgreSQL) e de ponta a ponta com axe (Playwright).

## Limitações conhecidas
- Sessão guardada no navegador (localStorage): limpar o navegador perde o acesso aos dados.
- Sem limite de requisições (rate limiting) ainda; adicione antes de ligar a IA em público.
- Tabelas criadas com `create_all`; adote Alembic quando o modelo de dados estabilizar.
- Qualquer sessão pode marcar uma explicação como "errada" e tirá-la de circulação até a revisão.

## Rodar com Docker (recomendado)
```bash
cp .env.example .env          # e troque POSTGRES_PASSWORD
docker compose up --build     # web: http://localhost:5173 · API: http://localhost:8000/docs
docker compose watch          # desenvolvimento: recarrega a API ao salvar
```

## Rodar sem Docker
```bash
# API (precisa do uv: https://docs.astral.sh/uv/)
cd apps/api && uv sync --extra llm && uv run fastapi dev app/main.py   # usa SQLite local; --extra llm instala os SDKs de IA
# Front-end (Node 24)
cd apps/web && npm install && npm run dev                     # http://localhost:5173
```

## Testes
```bash
cd apps/api && uv run pytest
cd apps/web && npx playwright install chromium && npx playwright test   # sobe API e front sozinho
```

## Ligar a IA
1. No `.env`: `EXPLANATION_PROVIDER=llm`, `LLM_BACKEND`, `LLM_MODEL`, `LLM_API_KEY`.
   - Sem orçamento? Instale o [Ollama](https://ollama.com), baixe um modelo e use
     `LLM_BACKEND=openai_compatible` com `LLM_BASE_URL=http://host.docker.internal:11434/v1`
     (ou `http://localhost:11434/v1` fora do Docker).
2. Explicações geradas ficam **em revisão**. Para revisar:
   ```bash
   docker compose exec api python -m app.review list
   docker compose exec api python -m app.review show 3
   docker compose exec api python -m app.review approve 3
   ```
3. Para o teste de usabilidade, use só explicações aprovadas
   (`SERVE_ONLY_APPROVED=true`, o padrão).

## Adicionar conteúdo
- **Novo conceito:** crie `apps/api/content/concepts/<slug>.md` com o
  texto-base revisado e o cabeçalho (`key_terms`, `forbidden_patterns` com as
  armadilhas conhecidas). Peça a revisão do professor da disciplina.
- **Nova explicação escrita à mão:** copie
  `content/explanations/tcp-entrega-confiavel/futebol.json` para
  `content/explanations/<slug>/<interesse>.json`. Ela é validada ao subir a API.

## Estrutura
```
apps/api    FastAPI · validators/grounding.py (anti-erro) · providers/ (curated, llm)
apps/web    React + Vite + TS · e2e/ (Playwright + axe)

docs/README.md              índice da documentação e cadeia de rastreabilidade
docs/etapa-1-pesquisa       pesquisa com usuários: plano, questionário, consentimento
docs/etapa-2-personas-cenarios  personas, PACT, cenários, tarefas T1–T5
docs/etapa-3-prototipo      o app é o protótipo; tokens validados, decisões de design
docs/etapa-4-avaliacao      protocolo do teste, SUS, heurística, auditoria WCAG
docs/requisitos             requisitos funcionais e não funcionais (RF, RNF)
docs/adr                    decisões de arquitetura

compose.yaml · .env.example · .github/workflows/ci.yml
```

As quatro pastas `etapa-*` seguem o ciclo da disciplina de IHC
(Entender → Desenhar → Avaliar). Comece por [docs/README.md](docs/README.md).
