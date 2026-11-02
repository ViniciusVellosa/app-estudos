# Escolha de tecnologia e arquitetura

Versões verificadas em **29/10/2026** nos registros oficiais (PyPI, npm,
Docker Hub, devguide.python.org, nodejs.org, endoflife.date). **Confira na
data** antes de fixar: versões mudam toda semana. Marcadores: **(a confirmar)**
= não verificado; **(prática)** = prática de mercado sem fonte formal.

## Sumário
1. Critérios de decisão
2. Stack recomendada (com versões)
3. Alternativas e quando escolhê-las
4. Arquitetura do projeto-base
5. Modelo de dados
6. Contrato da API (REST v1)
7. Migrações: quando e como adotar o Alembic
8. Opção futura: streaming com SSE

---

## 1. Critérios de decisão
Num projeto de disciplina com IHC no centro, pese nesta ordem:
1. **Uso real:** a pesquisa indica estudo pelo **celular** (ônibus, à noite)
   → web **mobile-first**, sem loja de apps.
2. **Acessibilidade alcançável:** HTML semântico tem suporte maduro a zoom,
   reflow, leitor de tela (TalkBack, VoiceOver, NVDA) e testes automáticos
   (axe + Playwright). Cumprir WCAG 2.2 é mais fácil na web do que em nativo
   ou multiplataforma.
3. **Curva de aprendizado e prazo** da equipe.
4. **Ecossistema de IA:** SDKs oficiais em Python e TypeScript; Pydantic
   valida a saída estruturada do LLM.
5. **Rodar no Docker e demonstrar** ao professor com um comando.
6. **Privacidade (LGPD):** quanto menos dado sai para terceiros, melhor.

Para uma decisão nova: 2–3 opções, prós e contras, recomendação, ADR.

## 2. Stack recomendada

| Camada | Escolha | Versão em 29/10/2026 | Observação |
|---|---|---|---|
| Runtime back-end | **Python 3.14** | imagem `python:3.14.9-slim-trixie` ([Docker Hub](https://hub.docker.com/_/python/tags?name=3.14)) | 3.14 em bugfix até 2030-10; **3.13 já é só correções de segurança**; 3.15 saiu em 09/10/2026 sem imagem oficial visível; **piso 3.11** (SQLAlchemy 2.1 e pydantic-settings exigem) — [devguide](https://devguide.python.org/versions/) |
| Framework API | **FastAPI 0.162** | 0.162.0 (23/10/2026) | OpenAPI automático em `/docs`; SSE nativo desde 0.135 — [PyPI](https://pypi.org/project/fastapi/) |
| Validação | **Pydantic 2.14** + pydantic-settings 2.16 | 2.14.2 / 2.16.2 | valida entradas, configurações e a saída da IA |
| ORM | **SQLAlchemy 2.1** (modo síncrono) + psycopg 3.3 | 2.1.6 / 3.3.6 | síncrono é mais simples e basta aqui |
| Gerenciador Python | **uv 0.13.6** | 0.13.6 (27/10/2026) | `uv.lock`; guia oficial de Docker — [docs.astral.sh](https://docs.astral.sh/uv/guides/integration/docker/) |
| Banco | **PostgreSQL 18** | 18.6 (`postgres:18-alpine`) | EOL 14/11/2030; 19 ainda RC (GA prevista 19/11/2026, a confirmar); **14 tem EOL em 12/11/2026** — [endoflife.date](https://endoflife.date/postgresql) |
| Runtime do build web | **Node.js 24 LTS** | `node:24-alpine` (tag a confirmar) | segurança até 30/04/2028; 26 LTS também serve (até 04/2029); **evite 22** (EOL 04/2027; Vitest 5 e axe-core/playwright 4.14 pedem ≥ 22.12) — [nodejs.org](https://nodejs.org/en/about/previous-releases) |
| UI | **React 19.3** | 19.3.1 | — |
| Build | **Vite 8.3** | 8.3.5 (Node `^20.19 \|\| >=22.12`) | — |
| Linguagem | **TypeScript 7.0** | 7.0.2 | compila o projeto-base; se alguma ferramenta der atrito, fixe 6.x/5.x (a confirmar compatibilidade de plugins) |
| E2E | **Playwright 1.64** + **@axe-core/playwright 4.14** | 1.64.1 / 4.14.0 (Node ≥ 22.12) | acessibilidade no CI |
| Testes API | pytest 9.2 + `TestClient` (httpx) | 9.2.0 | — |
| Unidade front | Vitest 5 | 5.0.5 | configurado, **ainda sem testes** no projeto-base |
| Servidor estático | nginx | `nginx:alpine` (tags a confirmar) | SPA + cabeçalhos de segurança |
| Infra | Docker + Compose | Compose ≥ 2.22 para `watch` | — |
| CI | GitHub Actions | versões das actions a confirmar | — |

O projeto-base declara faixas amplas no `pyproject.toml` (ex.:
`fastapi[standard]>=0.115`, `requires-python = ">=3.12"`) e fixa as versões
exatas no `uv.lock` (FastAPI 0.162.0, Pydantic 2.14.2, SQLAlchemy 2.1.6,
anthropic 2.3.0, openai 3.41.0). No front, `package.json` usa `^` e o
`package-lock.json` fixa. Foi verificado com Vite 8.3.5, TypeScript 7.0.2 e
React 19.3.1.

## 3. Alternativas e quando escolhê-las
Versões e detalhes das alternativas **não foram verificados** na pesquisa
(a confirmar antes de decidir).

| Opção | Escolha se… | Cuidado |
|---|---|---|
| Node.js no back-end (Fastify, NestJS, Hono) | a equipe só domina TypeScript e quer uma linguagem só | validar a saída da IA com Zod; reescrever os validadores |
| Next.js full-stack | quer front e back no mesmo projeto, com SSR | mais "mágica", separação menos didática; desnecessário para uma SPA servida por nginx |
| React Native / Expo | precisam de recurso nativo (notificação, offline pesado) | axe/Playwright não se aplicam; testar com TalkBack/VoiceOver em aparelho real |
| Flutter | equipe já sabe Dart | árvore de semântica própria; testes manuais de leitor de tela obrigatórios |
| Supabase / Firebase | prazo curtíssimo, sem back-end próprio | menos aprendizado de back-end e Docker; dados em terceiro (LGPD, transferência internacional) |
| SQLite | protótipo local de uma pessoa, testes | já é usado nos testes e no modo sem Docker; não use com vários usuários concorrentes |

## 4. Arquitetura do projeto-base
**Monólito modular em camadas** (ports & adapters simplificado). Nada de
microsserviços: um processo de API, um banco, um servidor estático.

```
 [Navegador do celular]
   SPA React (apps/web, servida pelo nginx)  --HTTP/JSON + Bearer token-->
 [API FastAPI] (apps/api/app)
   main.py ........ lifespan: create_all, seed_curated, monta o gerador
   routers/ ....... HTTP fino: me.py (sessão, consentimento, interesses, prefs, LGPD)
   │                explanations.py (conceitos, explicação, avaliação)
   ▼
   services/explanations.py ... regra: aprovada? → gera? → valida → rascunho → padrão
   │        │
   │        ▼
   │   providers/  (interface ExplanationGenerator)
   │     ├── generator=None  → modo "curated" (só conteúdo escrito à mão)
   │     └── llm.py          → AnthropicGenerator | OpenAICompatibleGenerator (Ollama)
   │        │
   │        ▼
   │   validators/grounding.py ... checagens determinísticas anti-alucinação
   ▼
   db.py (SQLAlchemy) ──► [PostgreSQL 18]  (SQLite nos testes e sem Docker)

 content/  (arquivos versionados no Git = FONTE DE VERDADE técnica, revisada por PR)
   concepts/<slug>.md ............ texto-base + key_terms + forbidden_patterns
   explanations/<slug>/<interesse>.json ... explicações curadas (Mágico de Oz)
```

Decisões-chave (ADR 0001 e 0002 em `docs/adr/`):
- `EXPLANATION_PROVIDER=curated|llm` escolhe o modo; `LLM_BACKEND=anthropic|openai_compatible`
  escolhe o adaptador. Trocar de provedor não muda nada fora de `providers/`.
- **Conteúdo técnico em arquivos, não no banco:** a revisão acontece por pull
  request — quem revisa vê exatamente o que mudou no texto-base.
- **Falha segura:** qualquer falha, recusa ou explicação não revisada →
  explicação padrão (texto-base) com aviso. O aluno nunca fica sem resposta
  nem recebe conteúdo reprovado.
- **Cache = tabela `explanations`:** explicação aprovada para (conceito,
  interesse normalizado, nível) é reaproveitada entre alunos → menos custo e
  revisão humana possível.

## 5. Modelo de dados
Tabelas reais (`apps/api/app/db.py`, criadas com `Base.metadata.create_all`):

```
users        id (uuid, str 36, PK) · token_hash (sha256, único) · consent_version
             · consent_at · created_at · reading_prefs (JSON)
interests    id · user_id → users (ON DELETE CASCADE) · label (≤ 60) · depth (1–3)
explanations id · concept_slug · interest_label (normalizado: "Futebol" → "futebol")
             · level · provider (curated | llm:anthropic | llm:openai_compatible)
             · prompt_version · status · payload (JSON, os 6 passos) · created_at
feedback     id · explanation_id → explanations · user_id → users (ON DELETE CASCADE)
             · kind (util | errada | confusa) · comment (≤ 500) · created_at
```

- **Conceitos não estão no banco:** vêm de `content/concepts/*.md`
  (`app/content.py`, `load_concepts()` com cache em memória).
- **`reading_prefs` é uma coluna JSON** em `users` (`font_scale` 1–3, `theme`
  claro/escuro/alto-contraste/sistema, `reduced_motion`) — validada pelo
  schema `ReadingPrefs`, não pelo banco. Evita uma tabela só para três campos.
- **`depth`** do interesse atende ao achado de Walkington & Bernacki: o ganho
  da personalização depende de a profundidade casar com o quanto o aluno
  conhece o universo (Lumen, `carga-cognitiva-e-personalizacao.md`).
- **Ciclo de vida de `explanations.status`:**
  `draft` (gerada pela IA, aguardando revisão) → `approved` | `rejected` (via
  `python -m app.review`); `approved` → `under_review` quando alguém marca
  "Tem um erro" (`kind="errada"`); curadas entram como `approved` (ou o
  `status` do `_meta` do arquivo). Só `approved` é servida (salvo
  `SERVE_ONLY_APPROVED=false`, que serve também o `draft` com aviso).
- **Por que `explanations` não tem `user_id` (LGPD):** a explicação para
  "TCP × futebol" é a mesma para todo aluno que gosta de futebol. Sem vínculo
  com a pessoa, (a) ela pode ser reaproveitada e revisada uma vez só, (b)
  apagar um aluno (`DELETE /v1/me`) não deixa rastro pessoal nela, (c) o que
  vai ao provedor de IA é só o rótulo do interesse. O vínculo pessoal fica em
  `interests` e `feedback`, que são apagados em cascata com o usuário.
- Sem nome, e-mail ou senha: minimização (LGPD, art. 6º, III) e menos carga
  cognitiva no login (WCAG 3.3.8).

## 6. Contrato da API (REST v1)
Gerado dos routers (`app/routers/me.py`, `app/routers/explanations.py`, `app/main.py`).
Documentação interativa: http://localhost:8000/docs. Autenticação: cabeçalho
`Authorization: Bearer <token>` recebido em `POST /v1/session`.

| Método | Rota | Acesso | Corpo → resposta | Erros |
|---|---|---|---|---|
| GET | `/v1/health` | público | → `{"status":"ok"}` (healthcheck do Docker) | — |
| POST | `/v1/session` | público | → 201 `{token, user_id}` | — |
| POST | `/v1/consent` | sessão | `{version, accepted}` → 204. `accepted=false` revoga **e apaga os interesses** | 409 versão ≠ `CONSENT_VERSION` |
| GET | `/v1/me/interests` | sessão + consentimento | → `[{id, label, depth}]` | 403 sem consentimento |
| POST | `/v1/me/interests` | sessão + consentimento | `{label (2–60), depth (1–3)}` → 201 | 400 se já há 5; 422 inválido |
| DELETE | `/v1/me/interests/{id}` | sessão + consentimento | → 204 | 404 de outro aluno/inexistente |
| GET | `/v1/me/reading-prefs` | sessão | → `{font_scale, theme, reduced_motion}` | — |
| PUT | `/v1/me/reading-prefs` | sessão | mesmo formato → mesmo formato | 422 |
| GET | `/v1/me/export` | sessão | → `{user_id, consent_version, consent_at, interests, reading_prefs}` (LGPD art. 18, II e V) | 401 |
| DELETE | `/v1/me` | sessão | → 204; apaga usuário, interesses e avaliações (art. 18, VI) | 401 |
| GET | `/v1/concepts` | público | → `[{slug, title, discipline}]` | — |
| GET | `/v1/concepts/{slug}/neutral` | público | → `{slug, title, base_text}` | 404 |
| POST | `/v1/explanations` | sessão + consentimento | `{concept_slug, interest_id, level: iniciante\|intermediario}` → `ExplanationOut` | 404 conceito/interesse |
| POST | `/v1/explanations/{id}/feedback` | sessão | `{kind: util\|errada\|confusa, comment?}` → 204; `errada` → `under_review` | 404 |

`ExplanationOut`: `id` (nulo na explicação padrão), `concept_slug`,
`interest_label`, `provider` (`curated`, `llm:…` ou `neutral`), `status`
(`approved`, `draft` ou `neutral`), `personalized`, `payload` (os 6 passos ou
nulo), `neutral_text`, `notice` (aviso ao aluno), `created_at`.

Convenções: rotas versionadas (`/v1`); mensagens de erro em português
simples no campo `detail` (o front mostra ao aluno — heurística 9 de Nielsen,
via Lumen); `204` sem corpo para comandos.

## 7. Migrações: quando e como adotar o Alembic
O projeto-base usa `Base.metadata.create_all` no `lifespan`: cria tabelas que
faltam, mas **não altera tabelas existentes**. Basta enquanto o esquema muda
toda semana e os dados são descartáveis (`docker compose down -v` recria).

Adote o **Alembic** (1.20.1 em 29/10/2026, https://pypi.org/project/alembic/)
quando houver dados que não podem ser perdidos (ex.: rodada do teste de
usabilidade) ou quando a primeira coluna nova precisar entrar num banco já
populado **(prática)**:
```bash
cd apps/api
uv add alembic
uv run alembic init migrations
# migrations/env.py: from app.db import Base; target_metadata = Base.metadata
#                    e a URL vinda de get_settings().database_url
uv run alembic revision --autogenerate -m "esquema inicial"
uv run alembic stamp head        # banco que já existia (criado pelo create_all)
uv run alembic revision --autogenerate -m "adiciona coluna X"   # revise o arquivo gerado!
uv run alembic upgrade head
```
Depois: troque `init_db()` por `alembic upgrade head` na subida (comando no
Compose ou no `lifespan`), mantenha `create_all` só nos testes com SQLite e
registre a mudança num ADR. O autogenerate não detecta tudo (ex.: renomear
coluna vira apagar + criar): sempre leia a migração **(prática)**.

## 8. Opção futura: streaming com SSE
**Não implementado no projeto-base.** Faz sentido só se a geração pelo LLM
ficar lenta (vários segundos) e o teste mostrar ansiedade na espera.

- O FastAPI tem SSE nativo desde **0.135.0**: `fastapi.sse.EventSourceResponse`
  e `ServerSentEvent(data=..., event=..., id=..., retry=...)`; funciona com
  POST; manda *ping* a cada 15 s e define `Cache-Control: no-cache` e
  `X-Accel-Buffering: no` (evita buffer no nginx) —
  https://fastapi.tiangolo.com/tutorial/server-sent-events/
- **Não transmita tokens crus.** A saída precisa passar pelo schema e pelos
  validadores antes de chegar ao aluno (OWASP LLM05/LLM09). Mande **eventos de
  fase** e, no fim, **só o JSON validado**:
  ```python
  # esboço, não testado — confira a API na doc da sua versão do FastAPI
  from fastapi.concurrency import run_in_threadpool
  from fastapi.sse import EventSourceResponse, ServerSentEvent

  @router.post("/explanations/stream", response_class=EventSourceResponse)
  async def stream_explanation(body: ExplanationRequest, request: Request, user: ConsentedUser, db: DbDep):
      # carregar concept, interest e gen = request.app.state.generator como em request_explanation
      yield ServerSentEvent(event="status", data={"fase": "Buscando o conteúdo revisado…"})
      yield ServerSentEvent(event="status", data={"fase": "Adaptando ao seu interesse…"})
      out = await run_in_threadpool(get_explanation, db, concept, interest.label, interest.depth, body.level, gen)
      yield ServerSentEvent(event="status", data={"fase": "Conferindo com o texto-base…"})
      yield ServerSentEvent(event="result", data=out.model_dump(mode="json"))
  ```
  (`get_explanation` é síncrono: rode em thread para não travar o laço de
  eventos.)
- No front: `EventSource` do navegador só faz GET; para POST, leia o corpo com
  `fetch` + `ReadableStream` **(prática)**. Anuncie cada fase na região viva
  `role="status"` já existente (nunca cada token; o MDN recomenda criar a
  região viva antes de atualizá-la —
  https://developer.mozilla.org/en/AJAX/WAI_ARIA_Live_Regions), use
  `aria-busy` no contêiner (a confirmar) e ofereça "Cancelar" — fechar a
  conexão deve abortar a chamada ao LLM (detecção de desconexão no gerador
  SSE a confirmar).

Fontes: PyPI e npm (páginas dos pacotes citados, 29/10/2026);
https://devguide.python.org/versions/ ; https://nodejs.org/en/about/previous-releases ;
https://endoflife.date/postgresql ; https://hub.docker.com/_/postgres ;
https://fastapi.tiangolo.com/tutorial/server-sent-events/ ;
https://github.com/fastapi/full-stack-fastapi-template (referência de stack
FastAPI + React + Postgres + Playwright).
