# Projeto-base `app-estudos` — mapa, como rodar e como estender

O projeto-base fica em `assets/starter/app-estudos/`. Para criar o projeto do
aluno: `python3 scripts/novo_projeto.py <pasta> [--nome "Nome do App"]`
(copia tudo, troca o nome em `index.html` e `App.tsx`, nunca sobrescreve uma
pasta com arquivos). Estado verificado em 29/10/2026: **27 testes de API (SQLite e PostgreSQL 16)
passando** (pytest), ruff limpo, build do front com Vite 8.3.5 / TypeScript
7.0.2 / React 19.3.1, e2e com Playwright + @axe-core/playwright passando
(tags `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`), incluindo
reflow a 320px com texto 2x e alto contraste, e uso só com teclado.
**As imagens Docker não foram construídas** no ambiente de autoria (o
`compose.yaml` foi validado com `docker compose config`): confirme
`docker compose up --build` na máquina do aluno.

## Sumário
1. Mapa de arquivos
2. Como rodar (Docker, sem Docker, testes)
3. Receitas
   3.1 Novo conceito · 3.2 Explicação curada (Mágico de Oz) · 3.3 Ligar a IA ·
   3.4 Revisar rascunhos · 3.5 Novo endpoint com teste · 3.6 Nova tela acessível ·
   3.7 Nova coluna · 3.8 Build do teste de usabilidade
4. Três bugs que os testes e2e pegaram (lições)
5. Limitações conhecidas

---

## 1. Mapa de arquivos

### Raiz
| Arquivo | Para quê |
|---|---|
| `README.md` | como rodar, ligar a IA, adicionar conteúdo |
| `compose.yaml` | serviços `db` (Postgres 18), `api`, `web`; `develop.watch` (ver `backend-e-docker.md`) |
| `.env.example` | modelo do `.env` (senha do banco, provedor, IA, versão do termo) |
| `.gitignore` | `.env`, `*.db`, `.venv/`, `node_modules/`, `dist/`, relatórios do Playwright |
| `.github/workflows/ci.yml` | jobs `api` (ruff + pytest), `web` (build), `e2e` (Playwright + axe) |
| `docs/adr/0001-stack-do-projeto.md` | ADR da stack (preencher data e decisores) |
| `docs/adr/0002-ia-atras-de-interface-e-revisao-humana.md` | ADR do motor de IA com falha segura e revisão |
| `docs/requisitos/requisitos.md` | RF01–RF07 com rastreio e teste, Gherkin do RF03, RNF01–RNF06 (ISO 25010:2023) |

### API (`apps/api/`)
| Arquivo | Para quê |
|---|---|
| `pyproject.toml` | dependências; extra `llm` (anthropic, openai); grupo `dev` (pytest, httpx, ruff); `package = false` |
| `uv.lock` | versões exatas (FastAPI 0.162.0, Pydantic 2.14.2, SQLAlchemy 2.1.6, anthropic 2.3.0, openai 3.41.0…) |
| `Dockerfile` / `.dockerignore` | imagem multi-stage com uv, usuário `app`, healthcheck |
| `app/main.py` | cria o app, `lifespan` (create_all, `seed_curated`, gerador), CORS, `/v1/health` |
| `app/config.py` | `Settings` (pydantic-settings) e `get_settings()` |
| `app/db.py` | modelos `User`, `Interest`, `Explanation`, `Feedback`; engine; `get_db`; `init_db` |
| `app/security.py` | token de sessão (gera e faz hash); `DbDep`, `CurrentUser`, `ConsentedUser` |
| `app/schemas.py` | `ExplanationPayload` (6 passos), `MappingRow`, `TransferQuestion`, `Refusal`; entradas/saídas da API |
| `app/content.py` | lê `content/` (`load_concepts`, `load_curated`, `slugify`) |
| `app/routers/me.py` | sessão, consentimento, interesses, preferências, exportação, exclusão |
| `app/routers/explanations.py` | conceitos, explicação padrão, pedir explicação, avaliação |
| `app/services/explanations.py` | regra do motor: `seed_curated`, `generate_validated`, `get_explanation`, avisos `NOTICE_*` |
| `app/providers/base.py` | interface `ExplanationGenerator`, `ExplanationRequestData`, `GenerationError` |
| `app/providers/llm.py` | `GenerationResult`, `user_message`, `AnthropicGenerator`, `OpenAICompatibleGenerator`, `build_llm_generator` |
| `app/validators/grounding.py` | validadores anti-alucinação (`validate_explanation`, `quote_in_source`, `normalize`) |
| `app/prompts/explicacao_sistema.md` | prompt do sistema (versione com `PROMPT_VERSION`) |
| `app/review.py` | CLI de revisão humana: `list`, `show`, `approve`, `reject` |
| `content/concepts/tcp-entrega-confiavel.md` | o único conceito de exemplo: texto-base + `key_terms` + `forbidden_patterns` |
| `content/explanations/tcp-entrega-confiavel/futebol.json` | a única explicação curada de exemplo (com `_meta`) |
| `tests/conftest.py` | SQLite em memória (ou `TEST_DATABASE_URL` para PostgreSQL), modo curated; fixtures `banco_limpo` (automática), `client` e `auth` (sessão com consentimento) |
| `tests/test_api.py` | fluxo, fallbacks, LGPD, `FakeGenerator` (10 testes) |
| `tests/test_grounding.py` | validadores, regressão do Pokémon (10 testes com os parametrizados) |
| `tests/test_llm_adapter.py` | adaptadores de LLM com clientes falsos, injeção (5 testes) |
| `tests/test_curadas.py` | toda explicação escrita à mão passa nos validadores (1 por arquivo + 1) |

### Front-end (`apps/web/`)
| Arquivo | Para quê |
|---|---|
| `package.json` / `package-lock.json` | React 19.3, Vite 8.3, TS 7.0, Playwright 1.64, axe 4.14, Vitest 5 |
| `index.html` | `lang="pt-BR"`, viewport **sem** bloqueio de zoom, `color-scheme` |
| `vite.config.ts` | plugin React, porta 5173 |
| `tsconfig.json` | TypeScript estrito |
| `src/main.tsx` | monta o `App` |
| `src/api.ts` | cliente da API, token em `localStorage` (`estudos.token`), `CONSENT_VERSION`, `ApiError` |
| `src/App.tsx` | telas `consentimento`, `interesses`, `estudar`, `preferencias`, `meus-dados`; gestão de foco; região viva |
| `src/components/ExplanationView.tsx` | os 6 passos, alternância sem analogia, resposta da pergunta, avaliação |
| `src/styles/tokens.css` | cores por tema (claro, escuro, alto contraste amarelo/preto, sistema) |
| `src/styles/base.css` | layout de coluna única, foco visível, alvos de 44px, tabela→lista, quebra de palavras |
| `src/styles/paleta-contraste.json` | pares de cor para o `contrast_check.py` do Lumen (validados em AAA) |
| `e2e/fluxo-principal.spec.ts` | 3 testes: fluxo principal, 320px + texto 2x + alto contraste, só teclado |
| `playwright.config.ts` | projetos "celular" (Pixel 7) e "desktop"; sobe API (SQLite `e2e.db`) e `vite preview` na 4173 |
| `Dockerfile` / `nginx.conf` / `.dockerignore` | build Node 24 → nginx com fallback de SPA e cabeçalhos |

### Skill
| Arquivo | Para quê |
|---|---|
| `scripts/novo_projeto.py` | copia o projeto-base para a pasta do aluno |

## 2. Como rodar
```bash
# Docker (recomendado)
cp .env.example .env                  # troque POSTGRES_PASSWORD
docker compose up --build             # web http://localhost:5173 · API http://localhost:8000/docs
docker compose watch                  # dev: recarrega a API ao salvar

# Sem Docker
cd apps/api && uv sync --extra llm && uv run fastapi dev app/main.py   # SQLite dev.db; --extra llm instala os SDKs de IA
cd apps/web && npm install && npm run dev                   # Node 24; http://localhost:5173

# Testes (rode antes de dizer "terminei")
cd apps/api && uv run pytest && uv run ruff check .
cd apps/web && npm run build
cd apps/web && npx playwright install chromium && npx playwright test   # sobe API e front sozinho
```

## 3. Receitas

### 3.1 Adicionar um conceito
1. Crie `apps/api/content/concepts/<slug>.md`:
   ```markdown
   ---
   slug: dns-resolucao
   title: Resolução de nomes no DNS
   discipline: Redes de Computadores
   reviewed_by: "Prof. Fulano"          # informativo (o código não lê)
   reviewed_at: "2026-11-05"
   key_terms: [resolvedor, servidor raiz, TLD, servidor autoritativo, cache, TTL]
   forbidden_patterns:                  # sem acento, minúsculas (texto normalizado)
     - "o navegador (pergunta|consulta) (direto|diretamente) (ao|o) servidor raiz"
   ---
   Texto-base revisado, em parágrafos curtos. É a ÚNICA fonte de verdade técnica…
   ```
   O arquivo **precisa** começar com `---` e ter `slug` e `title`; use o mesmo
   slug no nome do arquivo e no front-matter (o código usa o do front-matter).
2. Peça a revisão do professor da disciplina **por pull request** (ele vê o
   diff do texto-base). Preencha `reviewed_by`/`reviewed_at`.
3. Escreva os `forbidden_patterns` a partir dos erros clássicos e teste cada
   um (comando em `construcao-do-app.md`, seção 6).
4. Reinicie a API (`docker compose restart api`): o conteúdo é lido uma vez.
5. Acrescente ao menos uma explicação curada (3.2) e o teste da 3.2.

### 3.2 Explicação curada (Mágico de Oz)
1. Copie `content/explanations/tcp-entrega-confiavel/futebol.json` para
   `content/explanations/<slug>/<interesse>.json`. **O nome do arquivo tem de
   ser o interesse normalizado** (`slugify`: minúsculas, sem acento, espaços →
   `-`; "League of Legends" → `league-of-legends.json`), porque
   `load_curated` monta o caminho assim.
2. `_meta`: `interest_label`, `level` (`iniciante`), `status` (`approved`),
   `reviewed_by`, `note`. Depois, os 6 campos do `ExplanationPayload`, com
   `trecho_base` **copiado** do texto-base.
3. Ao subir, `seed_curated` valida cada arquivo com os mesmos validadores da
   IA; **reprovada é pulada** com `WARNING curada reprovada <arquivo>: [erros]`
   no log — ela simplesmente não aparece para o aluno. Olhe o log
   (`docker compose logs api | grep curada`).
4. Editou o JSON depois? Ao reiniciar, `seed_curated` **atualiza** o conteúdo
   no banco (sem tirar do estado `under_review` o que foi marcado como
   errado). Com `docker compose watch`, salvar em `content/` já reinicia a API.
5. `tests/test_curadas.py` (já incluído) valida **todas** as curadas com os
   mesmos validadores da IA, então uma curada reprovada quebra o `pytest` em
   vez de sumir em silêncio. Rode `uv run pytest tests/test_curadas.py -v`
   depois de criar ou editar uma.

### 3.3 Ligar a IA
**Claude (Anthropic)** — no `.env`:
```
EXPLANATION_PROVIDER=llm
LLM_BACKEND=anthropic
LLM_MODEL=<nome atual na doc da Anthropic>
LLM_API_KEY=<sua chave>          # só aqui; nunca em VITE_*
```
**Ollama local (gratuito, sem enviar dados a terceiros):** instale
(https://ollama.com), `ollama pull <modelo>` e:
```
EXPLANATION_PROVIDER=llm
LLM_BACKEND=openai_compatible
LLM_MODEL=<nome do modelo baixado>
LLM_BASE_URL=http://host.docker.internal:11434/v1   # fora do Docker: http://localhost:11434/v1
```
No Linux, acrescente `extra_hosts: ["host.docker.internal:host-gateway"]` ao
serviço `api` (a confirmar; ver `backend-e-docker.md`).

Depois: `docker compose up -d api` e confira o log. "IA desativada: …" =
falta chave/modelo ou o pacote; **sem Docker, instale o extra:
`uv sync --extra llm`** (o `uv sync` puro não instala `anthropic`/`openai`; a
imagem Docker já instala). Com a IA ligada, gerar não significa servir:
rascunhos ficam em revisão (`SERVE_ONLY_APPROVED=true`).

### 3.4 Revisar rascunhos
```bash
docker compose exec api python -m app.review list        # draft e under_review
docker compose exec api python -m app.review show 3
docker compose exec api python -m app.review approve 3   # ou reject 3
```
Sem Docker: `uv run python -m app.review …` em `apps/api`. Revise com o
texto-base aberto. Erro técnico encontrado → novo `forbidden_patterns` + teste
de regressão em `tests/test_grounding.py` (modelo: `test_pokemon_stop_and_wait_regression`).

### 3.5 Novo endpoint com teste
Exemplo verificado: listar as avaliações do próprio aluno (completa o direito
de acesso — hoje a exportação não inclui avaliações).
1. Schema em `app/schemas.py`:
   ```python
   class FeedbackOut(BaseModel):
       explanation_id: int
       kind: str
       comment: str | None
       created_at: datetime
   ```
2. Rota em `app/routers/me.py` (importe `FeedbackOut`):
   ```python
   @router.get("/me/feedback", response_model=list[FeedbackOut])
   def list_my_feedback(user: CurrentUser):
       """Avaliações do próprio aluno (acesso, LGPD art. 18, II)."""
       return [
           FeedbackOut(explanation_id=f.explanation_id, kind=f.kind, comment=f.comment, created_at=f.created_at)
           for f in user.feedback
       ]
   ```
   Router novo? Crie `app/routers/<nome>.py` com `APIRouter(prefix="/v1", tags=[...])`
   e `app.include_router(...)` em `main.py`.
3. Teste em `tests/test_api.py`:
   ```python
   def test_list_my_feedback(client, auth):
       interest = client.post("/v1/me/interests", json={"label": "futebol", "depth": 2}, headers=auth).json()
       exp = client.post(
           "/v1/explanations", json={"concept_slug": SLUG, "interest_id": interest["id"]}, headers=auth
       ).json()
       client.post(f"/v1/explanations/{exp['id']}/feedback", json={"kind": "confusa"}, headers=auth)
       r = client.get("/v1/me/feedback", headers=auth)
       assert r.status_code == 200
       assert [f["kind"] for f in r.json()] == ["confusa"]
   ```
   **Atenção:** este teste só passa com a fixture `banco_limpo` (seção 5,
   isolamento dos testes); sem ela, um teste anterior deixa a explicação de
   futebol em `under_review`, `exp["id"]` vem `None` e a avaliação devolve 422.
4. `uv run pytest && uv run ruff check .`; acrescente o endpoint ao
   `api.ts` do front se a tela usar.

### 3.6 Nova tela no React mantendo a acessibilidade
1. Em `App.tsx`: inclua o nome no tipo `Screen` e o título em `TITLES` (vira
   o `<h1>` e o `document.title`).
2. Botão na `<nav aria-label="Principal">` com
   `aria-current={screen === "x" ? "page" : undefined}` e `onClick={() => go("x")}`.
3. Renderize dentro de `<main id="conteudo">`:
   `{screen === "x" && <MinhaTela setStatus={setStatus} />}`.
4. **Foco:** não ponha `autoFocus`; o efeito existente já move o foco para o
   `<h1>` nas trocas de tela (exceto a primeira — lição 4.3).
5. **Resultados** com `setStatus("…")` (região viva `role="status"` que já
   existe no markup inicial); **erros** com `setError` (`role="alert"`). Não
   crie outra região viva condicional — ela precisa existir antes de mudar.
6. **Formulários:** `<label htmlFor>` + `id`; dica com `aria-describedby`;
   erro com `aria-invalid` + texto que diz como corrigir; grupos em
   `<fieldset><legend>`; `noValidate` + validação própria com mensagem clara.
7. **Alvos de toque:** botões dentro de `.acoes` (quebra linha em vez de
   rolar); `button` já tem `min-height/min-width: 2.75rem` (44px, 2.5.5 AAA; o
   mínimo AA é 24px, 2.5.8).
8. **Cores só por tokens** (`var(--…)`). Cor nova → defina em
   `tokens.css` nos temas claro, escuro, alto contraste **e** no bloco
   `prefers-color-scheme: dark` de `sistema`; acrescente os pares em
   `paleta-contraste.json` e rode
   `python3 <skills>/lumen-ihc-acessibilidade/scripts/contrast_check.py --palette apps/web/src/styles/paleta-contraste.json`
   (alvo do projeto: AAA 7:1 no texto, 3:1 em bordas e foco).
9. Tamanhos em `rem`; nada de largura fixa em px; tabelas largas viram lista
   em tela estreita (veja a regra `@media (max-width: 30rem)`).
10. **Teste e2e** novo em `e2e/`: chame `semViolacoes(page)` e
    `semRolagemHorizontal(page)` na tela, inclusive a 320px com fonte
    "Enorme"; e passe pelo Lumen (checklist manual, leitor de tela).

### 3.7 Nova coluna no banco
1. Edite o modelo em `app/db.py` (ex.: `Interest.created_at: Mapped[datetime] = mapped_column(default=utcnow)`),
   o schema em `schemas.py` e a rota.
2. **Os testes passam** (SQLite em memória recriado a cada execução), **mas
   o Postgres do Docker não muda**: `create_all` não altera tabela existente →
   erro "column … does not exist". Em dev, sem dados a preservar:
   `docker compose down -v && docker compose up --build`.
3. Com dados a preservar (ex.: depois de começar o teste de usabilidade):
   **adote o Alembic** (`stack-e-arquitetura.md`, seção 7) e registre num ADR.
4. Dado pessoal novo? Inclua em `GET /v1/me/export`, garanta que
   `DELETE /v1/me` apaga, atualize o termo e o teste
   `test_delete_me_erases_everything`.

### 3.8 Build do teste de usabilidade
1. `.env`: `EXPLANATION_PROVIDER=curated` (ou `llm` com tudo já aprovado) e
   **`SERVE_ONLY_APPROVED=true`** — nenhum participante vê conteúdo não revisado.
2. **Explicações curadas para cada par (conceito × interesse) das tarefas.**
   Se o participante escolhe o próprio interesse, colete os interesses num
   pré-questionário e prepare as curadas antes; senão, a tarefa cai na
   explicação padrão (o que também é um cenário válido de testar). Rode
   `tests/test_curadas.py` (3.2) e confira o log por "curada reprovada".
3. Congele a versão: `git tag teste-usabilidade-1` (o relatório cita a tag).
4. **Celular do participante na mesma rede** **(prática)**: `localhost` no
   celular é o celular. Use o IP do computador:
   `VITE_API_URL=http://<IP>:8000` (arg de build do `web` no `compose.yaml`,
   depois rebuild), inclua `http://<IP>:5173` em `CORS_ORIGINS` (no
   `environment:` da `api`, que sobrescreve o `.env`) e `http://<IP>:8000` no
   `connect-src` do `nginx.conf`.
5. **Entre participantes:** cada um começa numa sessão nova (janela anônima ou
   "Meus dados → Apagar todos os meus dados" no fim).
6. **Métricas sem dado pessoal** — **não implementado**. Opções:
   (a) o observador mede tempo e erros pelo protocolo do Lumen (sem código);
   (b) tabela `study_events(id, session_hash, event, concept_slug, duration_ms, created_at)`
   com `session_hash = HMAC-SHA256(<sal secreto do .env>, user_id)`, **sem** o rótulo do interesse nem texto livre;
   eventos: `explanation_requested`, `neutral_toggled`, `answer_revealed`,
   `feedback_sent`, `prefs_changed` **(prática)**. Dado pseudonimizado
   continua sendo dado pessoal enquanto o sal existir (a confirmar no texto da
   LGPD); apague as métricas no prazo de retenção definido.
7. TCLE e CEP: com o Lumen (`metodos-de-avaliacao.md`, seção 11).

## 4. Três bugs que os testes e2e pegaram (lições)

| # | Sintoma | Causa | Correção | Lição |
|---|---|---|---|---|
| 4.1 | Front não carregava nada nos testes ("Não foi possível conectar ao servidor") | **CORS**: a API liberava só `http://localhost:5173`, mas o `vite preview` dos testes roda na `4173` | `CORS_ORIGINS='["http://localhost:4173"]'` no `webServer` do `playwright.config.ts` — **lista JSON**, que é como o pydantic-settings lê `list[str]` | toda nova origem (porta, IP, domínio) entra em `CORS_ORIGINS`; teste no mesmo modo em que vai rodar |
| 4.2 | Rolagem horizontal a 320px com texto 2x | a palavra "congestionamento", dentro de uma lista com recuo, não cabia na coluna; **o estouro de um nó de texto não aparece nas caixas (bounding boxes) dos elementos** | `overflow-wrap: break-word; hyphens: auto` no `body` e recuo menor nas listas (`padding-left: 1.25em`) | meça `document.documentElement.scrollWidth` contra `window.innerWidth` (função `semRolagemHorizontal`), não as caixas dos elementos; teste com o maior tamanho de fonte |
| 4.3 | Com teclado, o primeiro Tab pulava o link "Pular para o conteúdo" | o foco ia para o `<h1>` já na **primeira** tela | mover o foco só nas trocas **posteriores** (`firstScreenShown` em `App.tsx`) | gestão de foco serve para orientar após mudança; na carga inicial, deixe o foco no começo da página |

Os três passariam despercebidos só com o axe — por isso o projeto-base testa
fluxo, reflow medido e ordem de foco além das regras automáticas.

## 5. Limitações conhecidas
| Limitação | Consequência | Caminho |
|---|---|---|
| **Sem Alembic** (`create_all`) | coluna nova não chega a um banco existente | 3.7 e `stack-e-arquitetura.md` §7 |
| **Sem rate limiting** | custo da IA sem teto por aluno (OWASP LLM10) | `slowapi` ou contador por sessão **(prática)** |
| **SSE não implementado** | geração longa só mostra "Preparando a explicação…" | `stack-e-arquitetura.md` §8 |
| **Imagens Docker não construídas** no ambiente de autoria | `docker compose up --build` não verificado | rodar na máquina do aluno e registrar |
| **Sessão = token por navegador** em `localStorage` | trocar de aparelho, limpar dados ou navegação privada **perde o acesso** aos dados (que ficam órfãos no banco); token sem expiração | avisar no termo; política de retenção que apague sessões inativas; login opcional só se a pesquisa pedir |
| **Conteúdo de exemplo mínimo** | 1 conceito (`tcp-entrega-confiavel`) e 1 curada (futebol) | 3.1 e 3.2 |
| `nginx:alpine` sem versão fixa; CSP com a URL da API escrita | a imagem muda sozinha; a CSP quebra se `VITE_API_URL` mudar | fixar a tag; atualizar `connect-src` junto com `VITE_API_URL` |
| "Tem um erro" de qualquer sessão tira a explicação de circulação | um usuário pode "derrubar" conteúdo aprovado | aceitável no teste; em produção, limiar ou revisão |
| Front nunca envia `level` | sempre `iniciante` | campo na tela Estudar, se a pesquisa pedir |
| CI não constrói as imagens | Dockerfile quebrado só aparece na máquina | job `docker compose build` |
| `OpenAICompatibleGenerator` sem `"strict": true` | na API da OpenAI, aderência ao schema menos rígida | `construcao-do-app.md` §5 |

Fontes: o próprio código do projeto-base; `backend-e-docker.md`,
`stack-e-arquitetura.md`, `construcao-do-app.md`; Lumen
(`acessibilidade.md`, `metodos-de-avaliacao.md`, `scripts/contrast_check.py`).


### Corrigido depois da primeira revisão (29/10/2026)
Uma revisão do código encontrou e corrigiu: testes que compartilhavam o banco
(agora há a fixture `banco_limpo` em `conftest.py`); exportação sem as
avaliações (`/v1/me/export` agora inclui `feedback`); explicação curada
editada que não atualizava (o `seed_curated` atualiza o conteúdo, sem tirar
do estado `under_review`); `compose watch` sem reiniciar ao mudar `content/`
(agora `sync+restart`); `add_header` do nginx em `/assets/` que anulava os
cabeçalhos de segurança (agora repetidos); `npm test` sem testes
(`--passWithNoTests`); texto-base movido para o início da mensagem (permite
cache de prompt); `PSEUDONYM_SALT` removido por não ser usado.
- Depois dos testes da skill (29/10/2026): `tests/test_curadas.py` valida
  toda explicação escrita à mão; `TEST_DATABASE_URL` roda os testes no
  PostgreSQL (o CI já usa o Postgres de serviço); `extra_hosts:
  host.docker.internal:host-gateway` na API para usar Ollama no Linux; os
  testes e2e escolhem o conceito pelo nome (a lista é ordenada pelo nome do
  arquivo, então um conceito novo pode virar o padrão).

### Atenção no roteiro do teste de usabilidade
O interesse é casado pelo nome do arquivo da explicação curada (`futebol.json`
↔ "Futebol", "FUTEBOL"). Variações como "futebol de salão" ou "animes" caem na
explicação padrão. No roteiro, diga ao participante o interesse a digitar, ou
crie cópias do arquivo para as variações esperadas.
