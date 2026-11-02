# Back-end (FastAPI) e Docker

Tudo aqui descreve o projeto-base (`assets/starter/app-estudos/`). Versões
verificadas em 29/10/2026. Marcadores: **(a confirmar)** = não verificado;
**(prática)** = prática de mercado sem fonte formal.

> **Importante:** as imagens Docker do projeto-base **não puderam ser
> construídas** no ambiente em que a skill foi escrita (registro de imagens
> bloqueado). O `compose.yaml` foi validado com `docker compose config`, e a
> API e o front foram testados fora do Docker (27 testes pytest, também contra um PostgreSQL 16 local, build do
> Vite, e2e com Playwright). **Rode `docker compose up --build` na sua
> máquina e confira** antes de dizer ao professor que "sobe no Docker".

## Sumário
1. Estrutura e convenções do back-end
2. Configuração e segredos
3. Docker em uma analogia
4. Imagem da API (uv, multi-stage, não root)
5. Imagem do front (Node → nginx, SPA, cabeçalhos)
6. `compose.yaml` linha a linha
7. Comandos do dia a dia
8. CI (GitHub Actions)
9. Problemas comuns

---

## 1. Estrutura e convenções do back-end
```
apps/api/app/
├── main.py         app FastAPI, lifespan, CORS, /v1/health
├── config.py       Settings (pydantic-settings) + get_settings() com lru_cache
├── db.py           modelos SQLAlchemy 2.x, engine, SessionLocal, get_db, init_db
├── security.py     sessão por token; dependências DbDep, CurrentUser, ConsentedUser
├── schemas.py      contratos Pydantic (API e ExplanationPayload dos 6 passos)
├── content.py      lê content/ (conceitos e explicações curadas)
├── routers/        me.py, explanations.py — HTTP fino
├── services/       explanations.py — regra de negócio
├── providers/      base.py (interface), llm.py (Anthropic, compatível com OpenAI)
├── validators/     grounding.py — anti-alucinação
├── prompts/        explicacao_sistema.md
└── review.py       CLI de revisão humana
```

**Convenções usadas (siga-as ao estender):**
- **Dependências com `Annotated`** (em `security.py`):
  `DbDep = Annotated[Session, Depends(get_db)]`,
  `CurrentUser = Annotated[User, Depends(current_user)]` (401 sem token ou
  token inválido), `ConsentedUser = Annotated[User, Depends(consented_user)]`
  (403 sem consentimento). Na rota basta tipar o parâmetro:
  `def add_interest(body: InterestIn, user: ConsentedUser, db: DbDep)`.
- **`get_db` com `yield`**: uma sessão por requisição, fechada no fim.
- **`lifespan`** (padrão oficial; `@app.on_event` está obsoleto e não se
  mistura com lifespan — https://fastapi.tiangolo.com/advanced/events/): na
  subida, `init_db()` (create_all), `seed_curated()` (carrega e **valida** as
  explicações curadas) e monta `app.state.generator` (fica `None` no modo
  curated ou se a IA falhar ao iniciar — o app continua só com curado).
- **Routers finos**, regra em `services/`, nada de SQL nos routers além de
  buscas simples por dono (`Interest.user_id == user.id`).
- **Toda entrada e saída tipada** (`response_model=`); limites no schema
  (`max_length=60`, `ge=1, le=3`) em vez de `if` espalhado.
- **Erros em português simples** em `HTTPException(status, "mensagem")`: o
  front mostra o `detail` ao aluno.
- Banco **síncrono** (mais simples de aprender); chamadas ao LLM também são
  síncronas, com timeout. Async só se houver muita I/O concorrente
  **(prática)**.

## 2. Configuração e segredos
`app/config.py` lê variáveis de ambiente (12-factor **(prática)**) e o
arquivo `.env` (`SettingsConfigDict(env_file=".env", extra="ignore")`).
Nome do campo em maiúsculas = nome da variável.

| Variável | Padrão | Para quê |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./dev.db` | no Compose: `postgresql+psycopg://…@db:5432/…` |
| `CONTENT_DIR` | `content` | pasta dos textos-base e explicações curadas |
| `CORS_ORIGINS` | `["http://localhost:5173"]` | **lista JSON** (pydantic-settings lê listas como JSON): `'["http://localhost:4173"]'` |
| `EXPLANATION_PROVIDER` | `curated` | `curated` (sem IA) ou `llm` |
| `LLM_BACKEND` | `anthropic` | `anthropic` ou `openai_compatible` (Ollama etc.) |
| `LLM_MODEL`, `LLM_API_KEY`, `LLM_BASE_URL` | vazios | chave com `repr=False` |
| `LLM_TIMEOUT_S` / `LLM_MAX_OUTPUT_TOKENS` | 30 / 1500 | limites de custo e espera |
| `PROMPT_VERSION` | `1` | gravado em cada explicação gerada |
| `SERVE_ONLY_APPROVED` | `true` | só serve explicação revisada |
| `CONSENT_VERSION` | `2026-1` | versão do termo (o front envia a mesma em `src/api.ts`) |

Regras:
- `.env` fora do Git (`.gitignore`) e fora da imagem (`.dockerignore`);
  `.env.example` versionado com valores fictícios.
- **`VITE_*` é embutida no JavaScript no build** e fica visível para
  qualquer um (https://vite.dev/guide/env-and-mode). Mudar `VITE_API_URL`
  exige **rebuild** da imagem web; segredo ali nunca.
- `get_settings()` tem `lru_cache`: nos testes, o ambiente é configurado
  **antes** de importar o app (`tests/conftest.py`).
- Mudou `CONSENT_VERSION`? Mude também `CONSENT_VERSION` em
  `apps/web/src/api.ts`, senão `POST /v1/consent` devolve 409.

## 3. Docker em uma analogia
- **Imagem** = **marmita congelada**: receita pronta, com código e todas as
  dependências, igual em qualquer cozinha.
- **Contêiner** = a marmita **aquecida e servida** (a imagem em execução);
  pode jogar fora e esquentar outra.
- **Dockerfile** = a **receita**; *multi-stage* = cozinhar numa cozinha
  bagunçada (build) e levar só o prato pronto para o balcão (imagem final).
- **Compose** = o **cardápio do restaurante**: quais pratos saem juntos e em
  que ordem (`depends_on`).
- **Volume** = a **geladeira**: o que precisa sobreviver quando a marmita
  acaba (dados do Postgres). `docker compose down -v` **esvazia a geladeira**.
- **Rede do Compose** = a cozinha interna: os serviços se chamam pelo nome
  (`db`), não por `localhost`.

## 4. Imagem da API (`apps/api/Dockerfile`)
Segue o guia oficial do uv (https://docs.astral.sh/uv/guides/integration/docker/):

| Linha | Por quê |
|---|---|
| `FROM python:3.14-slim AS builder` | estágio de build |
| `COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /uvx /bin/` | binário do uv **pinado** (para build reprodutível, pine também por digest) |
| `ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_NO_DEV=1 UV_PYTHON_DOWNLOADS=0` | bytecode pré-compilado (subida mais rápida); cópia em vez de link (cache em outro filesystem); **sem dependências de dev** (pytest e ruff não vão para a imagem); usa o Python da imagem |
| `RUN --mount=type=cache,target=/root/.cache/uv --mount=type=bind,source=uv.lock,… uv sync --locked --no-install-project --extra llm` | camada só de dependências: só é refeita quando `uv.lock`/`pyproject.toml` mudam. `--extra llm` instala `anthropic` e `openai` |
| `COPY . /app` + `uv sync --locked --extra llm` | o código, em camada separada |
| `FROM python:3.14-slim` (estágio final) | imagem enxuta sem cache do uv |
| `groupadd --system app && useradd --system --gid app --home /app app` + `USER app` | **não root** (o guia do uv não cobre isso; foi acrescentado) |
| `COPY --from=builder --chown=app:app /app /app` | o usuário `app` precisa de escrita em `/app` (o `compose watch` sincroniza arquivos para lá) |
| `ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1` | usa o `.venv`; logs sem buffer |
| `HEALTHCHECK … python -c "import urllib.request; …/v1/health"` | a imagem slim não tem `curl`; usa o próprio Python |
| `CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]` | servidor de produção do FastAPI (sem recarga) |

`.dockerignore` da API: `.venv`, `__pycache__`, caches, `*.db`, `.env`. O
`.venv` **precisa** ficar fora (é específico da plataforma). Testes rodam no
host (`uv run pytest`), não no contêiner — a imagem não tem pytest.

## 5. Imagem do front (`apps/web/Dockerfile` + `nginx.conf`)
- Estágio `node:24-alpine AS build`: copia `package.json` e
  `package-lock.json` primeiro (cache), `npm ci` com cache mount, copia o
  resto, `ARG VITE_API_URL=http://localhost:8000` → `ENV` → `npm run build`
  (`tsc -b && vite build`).
- Estágio final `nginx:alpine`: copia `nginx.conf` e o `dist/`. A tag não está
  pinada nem verificada: fixe uma versão estável (a confirmar no Docker Hub).
  O nginx padrão inicia como root e os *workers* rodam sem privilégio; para
  não root total, existe a variante *unprivileged* na porta 8080 (a confirmar).
- `nginx.conf`:
  - `try_files $uri $uri/ /index.html;` → **fallback de SPA** (qualquer rota
    desconhecida devolve o app).
  - `/assets/` com `Cache-Control: public, max-age=31536000, immutable`
    (arquivos com hash no nome).
  - Cabeçalhos: `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`,
    `Content-Security-Policy: default-src 'self'; connect-src 'self' http://localhost:8000; img-src 'self' data:; style-src 'self'`.
  - **A CSP tem a URL da API fixa.** Mudou `VITE_API_URL`? Mude o
    `connect-src` também, senão o navegador bloqueia as chamadas.
  - Pegadinha do nginx: `add_header` dentro de um `location` **substitui** os
    do nível `server`. Por isso o `nginx.conf` do projeto-base repete os
    cabeçalhos de segurança dentro de `location /assets/` (ou use um `include`)
    (https://nginx.org/en/docs/http/ngx_http_headers_module.html#add_header).
- Melhoria possível **(prática)**: nginx como proxy reverso (`location /api/ { proxy_pass http://api:8000/; }`),
  `VITE_API_URL` relativa e `connect-src 'self'` — some o CORS, a porta 8000
  deixa de ser publicada e não precisa rebuild para mudar o endereço.

## 6. `compose.yaml` linha a linha
```yaml
services:                                   # sem "version:" — obsoleto, só gera aviso
  db:
    image: postgres:18-alpine
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-estudos}  # valor do .env ou padrão
      POSTGRES_USER: ${POSTGRES_USER:-estudos}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?defina POSTGRES_PASSWORD no .env}  # obrigatória
    volumes:
      - pgdata:/var/lib/postgresql          # Postgres 18+ (até o 17: /var/lib/postgresql/data)
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]  # $$ = $ literal
      interval: 5s
      timeout: 5s
      retries: 10
    # sem "ports": o banco só é acessível pela API, dentro da rede do Compose
  api:
    build: ./apps/api
    env_file: .env                          # LLM_*, EXPLANATION_PROVIDER etc.
    environment:                            # sobrescreve o que veio do env_file
      DATABASE_URL: postgresql+psycopg://${POSTGRES_USER:-estudos}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB:-estudos}
      CORS_ORIGINS: '["http://localhost:5173"]'
    depends_on:
      db:
        condition: service_healthy          # espera o pg_isready passar
        restart: true                       # reinicia a API se o Compose reiniciar o db
    ports: ["8000:8000"]                    # publicada porque o navegador chama a API direto
    develop:
      watch:                                # docker compose watch (Compose ≥ 2.22)
        - { action: sync+restart, path: ./apps/api/app, target: /app/app }
        - { action: sync+restart, path: ./apps/api/content, target: /app/content }
        - { action: rebuild, path: ./apps/api/pyproject.toml }
        - { action: rebuild, path: ./apps/api/uv.lock }
  web:
    build:
      context: ./apps/web
      args: { VITE_API_URL: http://localhost:8000 }   # embutida no build
    depends_on: [api]
    ports: ["5173:80"]                      # nginx na 80 do contêiner
volumes:
  pgdata:
```
(Mostrado com sintaxe compacta; o arquivo real usa a forma expandida.)

Pontos verificados nas docs do Docker:
- `version:` é obsoleto (https://docs.docker.com/reference/compose-file/version-and-name/).
- `condition: service_healthy` + `restart: true` e o healthcheck `pg_isready`
  são o padrão oficial (https://docs.docker.com/compose/how-tos/startup-order).
- **Postgres 18 mudou o `PGDATA`** para `/var/lib/postgresql/18/docker` e o
  volume deve ir em `/var/lib/postgresql`; no 17 e anteriores, em
  `/var/lib/postgresql/data` — montar no lugar errado **não persiste** os
  dados (https://hub.docker.com/_/postgres).
- `develop.watch` exige Compose **2.22+**, só vale para serviços com `build:`,
  e o `USER` do contêiner precisa de escrita no `target`
  (https://docs.docker.com/compose/how-tos/file-watch/).
- `POSTGRES_PASSWORD_FILE` permite ler a senha de um Docker secret
  (`/run/secrets/…`) em vez de variável — opção para deploy.

**Pegadinha do `watch`:** `content/` é só sincronizado (`sync`), mas a API
lê o conteúdo uma vez (`load_concepts` com `lru_cache`) e semeia as curadas
na subida. Editou `content/`? `docker compose restart api` (ou troque a ação
para `sync+restart`).

## 7. Comandos do dia a dia
```bash
cp .env.example .env                      # e troque POSTGRES_PASSWORD
docker compose config                     # valida o arquivo e mostra as variáveis resolvidas
docker compose up --build                 # sobe tudo (web :5173, API :8000/docs)
docker compose up --build -d --wait       # em segundo plano, espera ficar saudável
docker compose watch                      # desenvolvimento: recarrega a API ao salvar
docker compose ps                         # estado e saúde
docker compose logs -f api                # acompanha logs
docker compose restart api                # depois de editar content/
docker compose exec api python -m app.review list      # revisão humana
docker compose exec db psql -U estudos -d estudos      # console do banco
docker compose exec db pg_dump -U estudos estudos > backup.sql
docker compose build --pull --no-cache web             # rebuild limpo (ex.: mudou VITE_API_URL)
docker compose down                       # para (dados ficam no volume)
docker compose down -v                    # para e APAGA o banco
```
Sem Docker: `cd apps/api && uv sync --extra llm && uv run fastapi dev app/main.py`
(SQLite `dev.db`) e `cd apps/web && npm install && npm run dev`.

## 8. CI (`.github/workflows/ci.yml`)
Roda em `push` na `main` e em todo PR. Versões das actions
(`actions/checkout@v5`, `astral-sh/setup-uv@v6`, `actions/setup-node@v5`,
`actions/upload-artifact@v4`) **a confirmar** na data.

| Job | Passos | Observação |
|---|---|---|
| `api` | checkout → setup-uv → `uv sync --locked` → `uv run ruff check .` → `uv run pytest -q` | tem um **service container** `postgres:18-alpine` com `--health-cmd pg_isready` e porta 5432 mapeada (job no runner → `localhost`; job em contêiner → nome do serviço; só em runner Linux — https://docs.github.com/en/actions/tutorials/use-containerized-services/create-postgresql-service-containers). **Hoje os testes usam SQLite** (`conftest.py` força `DATABASE_URL=sqlite://`): o Postgres fica pronto para testes de integração futuros |
| `web` | checkout → Node 24 com cache npm → `npm ci` → `npm run build` | build falha em erro de tipo (`tsc -b`) |
| `e2e` | `needs: [api, web]` → uv + Node → `uv sync --locked` → `npm ci && npx playwright install --with-deps chromium` → `npx playwright test` → em falha, sobe `playwright-report` | o `playwright.config.ts` sobe sozinho a API (uvicorn + SQLite `e2e.db`, `CORS_ORIGINS='["http://localhost:4173"]'`) e o front (`vite preview` na 4173). Com `BASE_URL` definido, testa um ambiente já no ar (ex.: `docker compose up --wait`) |

Falha de axe ou de reflow **quebra o CI** — é de propósito (DoD). O CI não
constrói as imagens Docker; acrescentar um job `docker compose build` é um
bom próximo passo **(prática)**.

## 9. Problemas comuns

| Sintoma | Causa provável | Solução |
|---|---|---|
| Front mostra "Não foi possível conectar ao servidor"; console: *blocked by CORS policy* | origem do front não está em `CORS_ORIGINS` (caso real: API liberava só `:5173`, o `vite preview` rodava na `:4173`) | `CORS_ORIGINS='["http://localhost:4173"]'` — **lista JSON**; no Compose, edite `environment:` da `api` (ele sobrescreve o `.env`) |
| Console: *Refused to connect … violates Content Security Policy* | `VITE_API_URL` mudou, a CSP do nginx não | atualize `connect-src` em `nginx.conf` e reconstrua `web` |
| API não conecta no banco (*connection refused* em `localhost:5432`) | dentro do contêiner, `localhost` é o próprio contêiner | host = nome do serviço: `@db:5432` (já está no `compose.yaml`) |
| Dados somem ao recriar o contêiner do Postgres | volume no caminho errado para a versão (18 → `/var/lib/postgresql`; ≤ 17 → `/var/lib/postgresql/data`) | corrija o caminho; trocou de major com volume antigo? `pg_dump` + restaurar (ou `down -v` se os dados não importam) |
| Banco não sobe depois de trocar 17 ↔ 18 | volume com dados de outra major | idem acima; não reaproveite volume entre majors sem `pg_upgrade` |
| Mudei `VITE_API_URL` e nada mudou | é embutida no **build** | `docker compose build web && docker compose up -d web` |
| Mudei o código e não apareceu | imagem antiga | `docker compose up --build` ou use `docker compose watch` |
| Editei `content/` e a explicação não mudou | conteúdo lido uma vez na subida (`lru_cache`, `seed_curated`) | `docker compose restart api` |
| *Bind for 0.0.0.0:5173 failed: port is already allocated* | `npm run dev` ou outro serviço usando a porta | pare o outro processo ou troque o lado esquerdo (`"5174:80"`) **e** inclua a nova origem em `CORS_ORIGINS` |
| *required variable POSTGRES_PASSWORD is missing a value* / *env file … .env not found* | falta o `.env` | `cp .env.example .env` e troque a senha |
| API sobe e loga "IA desativada: defina LLM_API_KEY e LLM_MODEL" | `EXPLANATION_PROVIDER=llm` sem chave/modelo | preencha o `.env`; enquanto isso o app segue no modo curado |
| IA local (Ollama) não responde de dentro do Docker | `localhost` no contêiner não é o seu computador | `LLM_BASE_URL=http://host.docker.internal:11434/v1`; no **Linux**, acrescente à `api`: `extra_hosts: ["host.docker.internal:host-gateway"]`, e faça o Ollama escutar fora do loopback (`OLLAMA_HOST=0.0.0.0`) — conhecimento geral de Docker (a confirmar) |
| *Permission denied* ao escrever em `/app` ou num volume montado | contêiner roda como `app` (não root) e o diretório é de outro dono | `COPY --chown=app:app` (já feito); em bind mount, ajuste o dono no host ou use volume nomeado; não volte para root |
| Playwright: *Executable doesn't exist … chromium* | navegador do Playwright não instalado | `npx playwright install chromium` (no CI: `--with-deps`); ou aponte `CHROMIUM_PATH` para um Chromium existente |
| e2e falha em "sem rolagem horizontal" a 320px | palavra longa ("congestionamento") com fonte 2x estoura a coluna; o estouro de **nó de texto** não aparece nas caixas dos elementos | `overflow-wrap: break-word; hyphens: auto` no `body` e recuo menor nas listas (`padding-left: 1.25em`); meça `document.documentElement.scrollWidth` |
| `uv sync --locked` falha no CI | `uv.lock` desatualizado em relação ao `pyproject.toml` | rode `uv lock` localmente e faça commit do lock |
| `npm ci` falha | `package-lock.json` ausente/desatualizado | `npm install` local e commit do lock |

Fontes: https://docs.astral.sh/uv/guides/integration/docker/ ;
https://docs.docker.com/build/building/best-practices/ ;
https://docs.docker.com/compose/how-tos/startup-order ;
https://docs.docker.com/compose/how-tos/file-watch/ ;
https://hub.docker.com/_/postgres ; https://vite.dev/guide/env-and-mode ;
https://fastapi.tiangolo.com/advanced/events/ ; doc do GitHub Actions citada.
