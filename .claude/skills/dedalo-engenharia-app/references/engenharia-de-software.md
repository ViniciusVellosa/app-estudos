# Engenharia de software do app — processo, requisitos, qualidade, testes e segurança

Base: Sommerville, *Engenharia de Software* (requisitos, processos, testes; o
Oráclitos tem o resumo da disciplina); ISO/IEC/IEEE 29148 (requisitos);
ISO/IEC 25010:2023 (qualidade de produto); ISO 9241-210 (projeto centrado no
humano, via Lumen); OWASP. Pesquisa feita em 29/10/2026.

Marcadores: **(a confirmar)** = fato de conhecimento consolidado cuja fonte
primária não foi reaberta na pesquisa; **(prática)** = prática de mercado sem
fonte normativa. O que não tem marcador foi conferido na fonte indicada.

## Sumário
1. Processo: sprints alinhados ao Lumen, Scrum essencial, definição de pronto
2. Requisitos: qualidade (29148), histórias INVEST, Gherkin, MoSCoW, casos de uso
3. Matriz de rastreabilidade
4. Qualidade de produto: ISO/IEC 25010:2023 (9 características) aplicada ao app
5. Documentação de arquitetura: C4 e ADR
6. Prototipação vista pela engenharia
7. Testes: pirâmide, o que o projeto-base testa, dublês, limites da automação
8. Segurança: OWASP Top 10:2025, ASVS 5.0, segredos, cadeia de suprimentos
9. Fluxo de Git: GitHub flow, Conventional Commits, checklist de PR

---

## 1. Processo

### 1.1 Iterativo e incremental, casado com o ciclo do Lumen
O Lumen trabalha em **Entender → Desenhar → Avaliar** (ISO 9241-210). A
engenharia anda junto, em sprints de 1–2 semanas, entregando sempre algo que
roda:

| Sprint | Fase do Lumen | Engenharia (Dédalo) | Entrega verificável |
|---|---|---|---|
| 0 | Entender (plano de pesquisa) | Visão, ADR de stack, criar o projeto-base (`scripts/novo_projeto.py`), CI verde | `docker compose up --build` sobe; `uv run pytest` passa |
| 1 | Entender (síntese, personas, cenários) | Requisitos RF/RNF a partir dos achados; matriz de rastreabilidade; contrato da API revisado | `docs/requisitos/requisitos.md` com rastreio |
| 2 | Desenhar (baixa → alta fidelidade) | Telas no React com conteúdo **curado** (Mágico de Oz) para os conceitos das tarefas | e2e com axe passando |
| 3 | Avaliar (heurística) | Correções da avaliação; textos-base revisados pelo professor; `forbidden_patterns` | testes de regressão dos achados |
| 4 | Avaliar (teste de usabilidade + SUS) | Build do teste (`SERVE_ONLY_APPROVED=true`), métricas sem dado pessoal; IA opcional atrás de variável | roteiro de teste executável sem IA |
| 5 | Relatório | Correções do teste, documentação final, ADRs atualizados | release `v1.0.0` |

A IA **não está no caminho crítico**: se o LLM atrasar, o teste com usuários
acontece com explicações curadas (seção 6).

### 1.2 Scrum essencial para 1–3 pessoas (Scrum Guide 2020) (a confirmar)
Fonte: https://scrumguides.org/scrum-guide.html
- **Responsabilidades:** Product Owner, Scrum Master, Developers. Numa dupla,
  uma pessoa acumula PO (fala com o professor/usuários) e a outra SM.
- **Eventos:** Sprint (≤ 1 mês), Sprint Planning, Daily (15 min — numa dupla,
  uma mensagem diária basta **(prática)**), Sprint Review (mostre ao professor),
  Retrospectiva.
- **Artefatos e compromissos:** Product Backlog → *Product Goal*; Sprint
  Backlog → *Sprint Goal*; Incremento → *Definition of Done*.
- Alternativa: **Kanban** (visualizar fluxo, limitar WIP; Kanban Guide 2020,
  https://kanbanguides.org/) (a confirmar). Para quem não tem cerimônias fixas,
  um quadro do GitHub Projects com colunas *A fazer / Fazendo (WIP ≤ 2) /
  Revisão / Pronto* resolve **(prática)**.

### 1.3 Definição de pronto (DoD) do projeto
Uma história só está **pronta** quando (é o mesmo checklist do PR, seção 9):
1. Critérios de aceite (Gherkin) atendidos e demonstráveis.
2. Teste automatizado novo ou atualizado; `uv run pytest` e `uv run ruff check .`
   passam em `apps/api`; `npm run build` passa em `apps/web`.
3. Se mexeu em tela: `npx playwright test` passa (axe sem violações, reflow a
   320px, teclado) e o checklist manual do Lumen foi aplicado.
4. Nenhum segredo no diff; nenhuma variável `VITE_*` com segredo.
5. Impacto LGPD avaliado: dado pessoal novo? → atualizar termo, exportação
   (`/v1/me/export`) e exclusão (`DELETE /v1/me`), e o teste
   `test_delete_me_erases_everything`.
6. Decisão de arquitetura → ADR em `docs/adr/`.
7. Revisado por outra pessoa (ou, sozinho, relido no dia seguinte **(prática)**).
8. Roda no Docker (`docker compose up --build`) — se não puder verificar, o PR
   diz isso explicitamente.

---

## 2. Requisitos

### 2.1 Fontes e técnicas
Fontes: achados da pesquisa (Lumen), personas e cenários, restrições da
disciplina, legislação (LGPD; LBI, art. 63), normas (WCAG 2.2 / ABNT NBR
17225). Técnicas (Sommerville) (a confirmar): entrevistas e questionários
(reaproveite os do Lumen), cenários, casos de uso, prototipação e **validação**
com o professor (validade, consistência, completude, realismo,
verificabilidade).

### 2.2 Características de um bom requisito — ISO/IEC/IEEE 29148:2018 (a confirmar)
Fonte: https://www.iso.org/standard/72089.html

| Requisito individual | Pergunta de checagem | Exemplo ruim → bom no app |
|---|---|---|
| Necessário | Se tirar, alguém sente falta? | — |
| Apropriado | Está no nível certo (não é solução disfarçada)? | "usar Redis" → "explicação aprovada responde em < 1 s" |
| Não ambíguo | Só uma leitura possível? | "explicação boa" → "explicação com os 6 passos e ≥ 1 limite concreto" |
| Completo | Diz tudo para implementar e testar? | incluir o que acontece se a IA falhar |
| Singular | Uma coisa só? | separar "informar interesse" de "consentir" |
| Viável | Cabe no prazo e na tecnologia? | "IA nunca erra" → inviável; vira RNF de validação + revisão |
| Verificável | Dá para escrever um teste? | "acessível" → "WCAG 2.2 AA; axe sem violações; reflow a 320px" |
| Correto | Reflete a necessidade real (pesquisa)? | rastrear até o achado |
| Conforme | Segue o padrão de escrita do projeto? | formato história + Gherkin |

Para o **conjunto**: completo, consistente, viável, compreensível, validável.

**Requisitos de IA tendem a violar "verificável".** Transforme-os em medidas:
taxa de reprovação nos validadores, taxa de recusa, latência p95, nota de
rubrica na revisão humana, ausência de `forbidden_patterns` (ver
`construcao-do-app.md`, seção Avaliação).

### 2.3 Histórias de usuário + INVEST (a confirmar)
Formato: *Como <papel>, quero <ação>, para <benefício>*. INVEST (Bill Wake,
2003, https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/):
**I**ndependente, **N**egociável, **V**aliosa, **E**stimável, pequena
(**S**mall), **T**estável. História que não cabe numa sprint → quebre por
fluxo (feliz / erro / sem IA), não por camada (front / back).

### 2.4 Critérios de aceite em Gherkin (a confirmar)
Fonte: https://cucumber.io/docs/gherkin/reference/ — há localização em
português com `# language: pt` (`Funcionalidade`, `Cenário`, `Dado`,
`Quando`, `Então`, `E`, `Mas`).

```gherkin
# language: pt
Funcionalidade: Explicação personalizada (RF03)
  Cenário: explicação curada revisada
    Dado que aceitei o termo e informei o interesse "futebol"
    Quando peço a explicação de "Entrega confiável no TCP"
    Então vejo os seis passos, inclusive "4. Onde a comparação falha"
    E a mensagem "Explicação pronta." é anunciada na região viva (WCAG 4.1.3)
    E posso ver a explicação sem analogia com um toque (DP05 do Lumen)

  Cenário: interesse sem explicação revisada
    Dado que informei o interesse "xadrez"
    Quando peço a explicação de "Entrega confiável no TCP"
    Então vejo a explicação padrão e um aviso com o motivo
```
Cada cenário vira teste: o primeiro está em `apps/web/e2e/fluxo-principal.spec.ts`;
o segundo em `tests/test_api.py::test_unknown_interest_falls_back_to_neutral`.

### 2.5 Priorização MoSCoW (a confirmar)
DSDM/Agile Business Consortium
(https://www.agilebusiness.org/dsdm-project-framework/moscow-prioririsation.html):
**M**ust, **S**hould, **C**ould, **W**on't (desta vez). Orientação DSDM: Must
≤ ~60% do esforço. Sugestão para o app: Must = RF01–RF04, RF06, RF07 e os RA
do Lumen; Should = RF05 (avaliação); Could = IA ligada no teste; Won't =
login com e-mail, app nativo.

### 2.6 Casos de uso (Cockburn) (a confirmar)
Use quando o fluxo tem muitas exceções (ex.: pedir explicação: aprovada /
rascunho / recusa / falha). Campos: ator principal, pré-condições, garantia
mínima, garantia de sucesso, cenário principal, extensões. Nível "mar"
(objetivo do usuário). Exemplo:

| Campo | UC03 Pedir explicação |
|---|---|
| Ator | Aluno com consentimento dado |
| Pré-condição | ≥ 1 interesse cadastrado |
| Garantia mínima | o aluno sempre recebe o texto-base (nunca conteúdo reprovado) |
| Cenário principal | escolhe conceito e interesse → recebe explicação aprovada nos 6 passos |
| Extensões | 3a sem aprovada e IA desligada → padrão + aviso; 3b IA recusa → padrão + aviso "comparação fiel"; 3c IA gera → rascunho em revisão → padrão + aviso; 3d falha de rede → mensagem de erro em `role="alert"` |

---

## 3. Matriz de rastreabilidade
Exigida pelo Lumen e pela 29148 (rastreio bidirecional). Mantenha em
`docs/requisitos/requisitos.md`:

| Achado | Persona/cenário | Requisito | Tela / endpoint | Teste automatizado | Tarefa do teste de usabilidade | LGPD |
|---|---|---|---|---|---|---|
| A2 estudam no ônibus | Diego / C1 | RF03, RNF01 | Estudar / `POST /v1/explanations` | e2e "aluno consente…" | T2 | interesse = dado pessoal |
| A5 baixa visão | Marta / C3 | RF06, RA04, RA05 | Leitura / `PUT /v1/me/reading-prefs` | e2e "texto ampliado e alto contraste…" | T4 | — |
| — | — | RF07 | Meus dados / `DELETE /v1/me` | `test_delete_me_erases_everything` | T5 | art. 18, VI |

(Achados e personas acima são exemplos: preencha com os da pesquisa real.)

---

## 4. Qualidade de produto — ISO/IEC 25010:2023
A revisão de 2023 tem **9 características** (a de 2011 tinha 8):
*Usability* virou **Interaction capability**, *Portability* virou
**Flexibility** e **Safety** é nova. Fonte: arc42 Quality Model,
https://quality.arc42.org/standards/iso-25010 e
https://quality.arc42.org/articles/iso-25010-update-2023 ; catálogo ISO:
https://www.iso.org/standard/78176.html

| Característica | Subcaracterísticas | No app (requisito e verificação) |
|---|---|---|
| 1. Adequação funcional | completude, correção, adequação funcionais | os 6 passos completos (schema `ExplanationPayload`); **correção** = conteúdo técnico vem do texto-base (validadores + revisão) |
| 2. Eficiência de desempenho | comportamento no tempo, utilização de recursos, capacidade | explicação aprovada vem do banco (rápida); LLM com timeout `LLM_TIMEOUT_S` e `LLM_MAX_OUTPUT_TOKENS` |
| 3. Compatibilidade | coexistência, interoperabilidade | API REST/JSON com OpenAPI em `/docs`; roda em navegadores de celular |
| 4. **Capacidade de interação** (ex-usabilidade) | reconhecibilidade da adequação, aprendizibilidade, operabilidade, proteção contra erro do usuário, **engajamento do usuário**, **inclusividade**, **assistência ao usuário**, **autodescritividade** | **território do Lumen**: inclusividade e assistência ao usuário (que substituíram "acessibilidade") = WCAG 2.2 AA, RA01–RA24; engajamento = personalização por interesse; proteção contra erro = confirmação antes de apagar dados. Verificação: axe + e2e + avaliação heurística + SUS |
| 5. Confiabilidade | **ausência de falhas** (ex-maturidade), disponibilidade, tolerância a falhas, recuperabilidade | falha/recusa da IA → explicação padrão (`test_llm_*`); healthcheck no Compose |
| 6. Segurança (*security*) | confidencialidade, integridade, não repúdio, responsabilização, autenticidade, **resistência** | token aleatório com hash, banco sem porta exposta, chave da IA só no back-end; OWASP (seção 8) |
| 7. Manutenibilidade | modularidade, reusabilidade, analisabilidade, modificabilidade, testabilidade | camadas routers/services/providers/validators; 27 testes; ruff. *A lista do arc42 pôs testabilidade em Flexibilidade; a prévia oficial a mantém aqui* (a confirmar em https://webstore.ansi.org/preview-pages/ISO/preview_ISO+IEC+25010-2023.pdf) |
| 8. **Flexibilidade** (ex-portabilidade) | adaptabilidade, **escalabilidade**, instalabilidade, substituibilidade | `docker compose up` em qualquer máquina; trocar provedor de IA por variável (`LLM_BACKEND`) = substituibilidade |
| 9. **Safety** (nova) | restrição operacional, identificação de risco, falha segura, **aviso de perigo**, integração segura | **risco = conteúdo errado gerado por IA**. Aviso de perigo: rótulo "Texto adaptado por inteligência artificial…" e `NOTICE_AI_DRAFT`; falha segura: na dúvida, explicação padrão; restrição operacional: `SERVE_ONLY_APPROVED=true` no teste com usuários |

Use a coluna da direita como RNF no `requisitos.md` (o projeto-base já traz
RNF01–RNF06 nesse formato).

---

## 5. Documentação de arquitetura

### 5.1 C4 (Simon Brown) (a confirmar)
Fonte: https://c4model.com/ — 4 níveis; para o app, os dois primeiros bastam:

| Nível | Diagrama do app |
|---|---|
| 1 Contexto | Aluno → **App de Estudos** → Provedor de LLM (opcional, externo); Professor revisor → App |
| 2 Contêineres | SPA React (nginx) → API FastAPI → PostgreSQL; API → LLM (Anthropic ou Ollama) |
| 3 Componentes (da API) | routers → services → providers (curated/llm) → validators → db; `content/` |
| 4 Código | opcional; gere da IDE se o professor pedir |

Desenhe em texto (Mermaid ou Structurizr DSL) dentro de `docs/arquitetura/`
para versionar junto do código **(prática)**. Se a disciplina exigir documento
formal, use o esqueleto arc42 (12 seções, https://arc42.org/overview) (a confirmar).

### 5.2 ADR — Architecture Decision Records
- **Nygard (2011)** (a confirmar,
  https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions):
  Título, Status (proposta/aceita/obsoleta/substituída), Contexto, Decisão,
  Consequências. Um arquivo numerado por decisão; não se edita uma decisão
  aceita, cria-se outra que a substitui.
- **MADR** (a confirmar, https://adr.github.io/madr/): Contexto e problema,
  Fatores de decisão, Opções consideradas, Resultado, Consequências, Prós e
  contras de cada opção. Bom quando há 3+ opções.
- No projeto-base: `docs/adr/0001-stack-do-projeto.md` e
  `docs/adr/0002-ia-atras-de-interface-e-revisao-humana.md` (formato Nygard com
  "Alternativas consideradas"). Preencha data e decisores.
- ADRs prováveis a seguir: 0003 provedor de LLM (e transferência
  internacional, ver LGPD em `construcao-do-app.md`); 0004 adoção do Alembic;
  0005 hospedagem da demonstração.

---

## 6. Prototipação vista pela engenharia

| Tipo | O que é | Quando usar no app |
|---|---|---|
| **Descartável** | Protótipo para validar requisitos/interface e depois jogar fora; não deve virar produção (não atende RNF, estrutura degradada — Sommerville) (a confirmar) | papel e Figma do Lumen; teste rápido de uma ideia de tela |
| **Evolutivo** | O protótipo **é** a primeira versão do sistema e vai sendo refinado | o projeto-base: comece por ele e evolua; não reescreva em outra ferramenta |
| **Contract-first** | Define o contrato da API antes de implementar; front e back avançam em paralelo | o FastAPI gera OpenAPI em `/docs` e `/openapi.json`; um mock (ex.: Prism, https://github.com/stoplightio/prism) pode servir o contrato (a confirmar) |
| **Mágico de Oz** | Um humano simula o sistema inteligente (Kelley, 1984, https://doi.org/10.1145/357417.357420) (a confirmar) | **explicações curadas** escritas à mão em `content/explanations/<conceito>/<interesse>.json` com `EXPLANATION_PROVIDER=curated`: o aluno vê exatamente a interface final, sem IA |

Fluxo recomendado: (1) papel com o Lumen → (2) contrato da API (já existe no
projeto-base; ajuste) → (3) telas React com conteúdo curado → (4) teste de
usabilidade no Mágico de Oz → (5) só então ligar o LLM, comparando com as
curadas. Isso separa "a ideia de interface funciona?" de "a IA é boa?".

---

## 7. Testes

### 7.1 Pirâmide (a confirmar)
Ham Vocke, "The Practical Test Pyramid"
(https://martinfowler.com/articles/practical-test-pyramid.html): testes de
granularidades diferentes; quanto mais alto o nível, menos testes. O *testing
trophy* (Kent C. Dodds) dá mais peso à integração e à análise estática — o
projeto-base faz isso (ruff + TypeScript estrito + muitos testes de API).

### 7.2 O que o projeto-base testa em cada nível

| Nível | Ferramenta | Arquivo | O que cobre |
|---|---|---|---|
| Estático | ruff; `tsc -b` (TypeScript estrito) | `pyproject.toml`; `tsconfig.json` | estilo/erros Python; tipos do front |
| Unidade | pytest | `tests/test_grounding.py` | cada validador: `test_curated_explanation_passes`, `test_pokemon_stop_and_wait_regression`, `test_invented_quote_is_rejected`, `test_universe_words_leaking_into_technical_text`, `test_long_scene_is_rejected`, `test_generic_limit_is_rejected`, `test_schema_requires_all_six_steps`, `test_quote_matching` (3 casos) |
| Unidade (adaptadores) | pytest + clientes falsos | `tests/test_llm_adapter.py` | `test_anthropic_returns_parsed_payload`, `test_anthropic_bad_stop_reason_raises` (max_tokens, refusal), `test_openai_compatible_parses_refusal`, `test_prompt_injection_in_interest_is_escaped` |
| Conteúdo | pytest parametrizado | `tests/test_curadas.py` | `test_curada_passa_nos_validadores[tcp-entrega-confiavel/futebol]`, `test_existe_ao_menos_uma_curada` |
| Integração (API + banco SQLite em memória) | pytest + `TestClient` | `tests/test_api.py` | `test_health`, `test_interest_requires_consent`, `test_curated_explanation_flow`, `test_unknown_interest_falls_back_to_neutral`, `test_wrong_feedback_takes_explanation_out_of_circulation`, `test_delete_me_erases_everything`, `test_revoking_consent_deletes_interests`, `test_llm_refusal_returns_neutral`, `test_llm_bad_output_is_retried_then_falls_back`, `test_llm_valid_draft_is_held_for_review` |
| Ponta a ponta + acessibilidade | Playwright + @axe-core/playwright | `apps/web/e2e/fluxo-principal.spec.ts` | fluxo das tarefas; 320px com texto 2x e alto contraste; só teclado. Projetos "celular" (Pixel 7) e "desktop" |

Total: **27 testes de API (SQLite e PostgreSQL 16)** (pytest) passando, ruff limpo; e2e passando.

### 7.3 Dublês de teste (Meszaros, via Fowler) (a confirmar)
https://martinfowler.com/bliki/TestDouble.html — *dummy, fake, stub, spy, mock*.
No projeto-base:
- `FakeGenerator` (em `test_api.py`) é um **fake/stub com contagem** (meio
  *spy*): devolve respostas pré-programadas e conta chamadas
  (`assert gen.calls == 2` prova a nova tentativa). Sem rede, sem custo, sem
  chave no CI.
- `SimpleNamespace` em `test_llm_adapter.py` substitui o cliente do SDK
  (`client.messages.parse`, `client.chat.completions.create`) → testa o
  tratamento de `stop_reason` e `finish_reason` sem chamar a API.
- Qualidade das explicações **não** se testa no CI com o LLM real: isso é
  avaliação (evals), separada (ver `construcao-do-app.md`).

### 7.4 Limites da automação de acessibilidade
Ferramentas automáticas encontram só parte dos problemas WCAG: a Deque
afirma ~57% dos problemas (por volume) com axe-core
(https://www.deque.com/automated-accessibility-testing-coverage/); o GOV.UK
(2017) achou ferramentas detectando ~30–40% de 142 barreiras plantadas
(https://accessibility.blog.gov.uk/2017/02/24/what-we-found-when-we-tested-tools-on-the-worlds-least-accessible-webpage/)
(números a confirmar). Por isso o projeto-base **também** testa coisas que o
axe não pega — rolagem horizontal medindo `document.documentElement.scrollWidth`,
ordem de foco, foco no título após troca de tela — e o Lumen faz a
avaliação manual e com pessoas (leitor de tela, baixa visão). Os e2e pegaram
3 bugs reais que o axe sozinho não pegaria (ver `projeto-base.md`).

---

## 8. Segurança

### 8.1 OWASP Top 10:2025
Edição vigente, substitui a de 2021 (https://top10.owasp.org/2025/ ; pt-BR em
https://owasp.org/Top10/2025/pt-BR/). Nomes conferidos; a frase de
significado é resumo nosso; data exata da publicação final (a confirmar).

| ID | Categoria | Em uma linha | Como o projeto-base trata |
|---|---|---|---|
| A01 | Broken Access Control | usuário acessa o que não devia | toda rota `/v1/me/*` exige `CurrentUser`/`ConsentedUser`; consultas filtram por `user_id` (interesse de outro aluno → 404). **Atenção:** qualquer sessão pode marcar qualquer explicação como "errada" (→ `under_review`); aceitável no teste, limite isso em produção |
| A02 | Security Misconfiguration | configuração insegura/padrão | CORS restrito (`CORS_ORIGINS`), banco **sem** `ports:`, cabeçalhos no nginx (CSP, nosniff, Referrer-Policy). `/docs` fica aberto: desligue em produção (`docs_url=None`) **(prática)** |
| A03 | Software Supply Chain Failures | dependências e build comprometidos | `uv.lock` e `package-lock.json` versionados; `uv sync --locked` e `npm ci` no CI e no Docker; imagem do uv pinada (`0.13.6`). Falta: Dependabot e pin por digest (8.4) |
| A04 | Cryptographic Failures | dados sem proteção criptográfica | token de sessão `secrets.token_urlsafe(32)`; banco guarda só o SHA-256. HTTPS **não** vem no Compose local: em qualquer deploy, TLS no proxy |
| A05 | Injection | dados viram comando (SQL, HTML, prompt) | ORM SQLAlchemy (consultas parametrizadas); React escapa texto (nada de `dangerouslySetInnerHTML`); injeção de prompt tratada como OWASP LLM01 (`construcao-do-app.md`) |
| A06 | Insecure Design | falha de desenho, não de código | ADR 0002 (IA atrás de interface, falha segura, revisão humana); limites no schema (5 interesses, 60 caracteres) |
| A07 | Authentication Failures | identificação/sessão frágil | sessão anônima por token aleatório; **sem expiração** e guardado em `localStorage` (exposto a XSS → CSP estrita mitiga). Se criar login com senha: Argon2id (OWASP Password Storage Cheat Sheet: ≥ 19 MiB, 2 iterações, paralelismo 1) (a confirmar) |
| A08 | Software or Data Integrity Failures | código/dados alterados sem verificação | conteúdo técnico só muda por PR revisado (`content/`); explicações curadas passam pelos validadores ao subir (`seed_curated`) |
| A09 | Security Logging and Alerting Failures | não registrar nem alertar | logs de recusa e de geração reprovada, sem identificador do aluno. Não há alerta: para o projeto, revise logs manualmente **(prática)** |
| A10 | Mishandling of Exceptional Conditions | erro tratado de forma insegura | toda falha do provedor vira `GenerationError` → explicação padrão; o front mostra mensagens claras em `role="alert"` e nunca o erro cru |

### 8.2 OWASP ASVS 5.0
Primeira versão maior em ~6 anos; níveis **L1/L2/L3**, com o L1 rebalanceado
para ser alcançável (fonte secundária: SoftwareMill, 02/06/2025,
https://softwaremill.com/whats-new-in-asvs-5-0/ ; repositório
https://github.com/OWASP/ASVS ; data oficial de lançamento a confirmar).
Para o projeto de disciplina, mire **L1** e use os capítulos de autenticação
(V6), criptografia (V11) e logging (V16) como checklist **(prática)**.

### 8.3 Segredos
- Tudo por variável de ambiente (`app/config.py`, pydantic-settings). `.env`
  no `.gitignore` e no `.dockerignore`; `.env.example` versionado só com
  valores fictícios.
- `LLM_API_KEY` tem `repr=False` (não aparecem se alguém
  imprimir as configurações).
- `VITE_*` é embutida no JavaScript no build (https://vite.dev/guide/env-and-mode):
  **nunca** segredo ali. A chamada ao LLM é só no back-end.
- `${POSTGRES_PASSWORD:?…}` no `compose.yaml` faz o Compose falhar se a senha
  não estiver definida.
- No CI, segredos em *GitHub Secrets*; varredura de segredos (ex.: gitleaks)
  no pipeline (OWASP Secrets Management Cheat Sheet) (a confirmar).
- Vazou uma chave? **Revogue no provedor primeiro**, depois limpe o histórico
  — apagar o commit não basta **(prática)**.

### 8.4 Cadeia de suprimentos
- Lockfiles: `apps/api/uv.lock` (`uv sync --locked` falha se estiver
  desatualizado) e `apps/web/package-lock.json` (`npm ci`).
- Faixas compatíveis no manifesto, versões exatas no lock.
- Imagens base por tag (`python:3.14-slim`, `node:24-alpine`, `postgres:18-alpine`,
  `nginx:alpine`): tags mudam com o tempo; para reprodutibilidade, pine por
  digest e reconstrua com `--pull` periodicamente
  (https://docs.docker.com/build/building/best-practices/).
- **Dependabot** (não incluído no projeto-base) **(prática)**; esboço de
  `.github/dependabot.yml` (ecossistemas `uv`, `npm`, `github-actions`,
  `docker`; nomes a confirmar na doc do GitHub):
  ```yaml
  version: 2
  updates:
    - { package-ecosystem: uv, directory: /apps/api, schedule: { interval: weekly } }
    - { package-ecosystem: npm, directory: /apps/web, schedule: { interval: weekly } }
    - { package-ecosystem: github-actions, directory: /, schedule: { interval: weekly } }
  ```
- Varredura de imagem (Docker Scout ou Trivy) **(prática)**.

---

## 9. Fluxo de Git

- **GitHub flow** (https://docs.github.com/en/get-started/using-github/github-flow)
  (a confirmar): `main` sempre funcionando → branch curta por história
  (`feat/rf05-avaliacao`) → PR → CI verde + revisão → merge. Para 1–3 pessoas é
  suficiente; nada de git-flow com `develop`/`release`.
- **Conventional Commits 1.0.0** (https://www.conventionalcommits.org/en/v1.0.0/)
  (a confirmar): `<tipo>[escopo opcional]: <descrição>`. `feat` ↔ MINOR,
  `fix` ↔ PATCH, `!` ou `BREAKING CHANGE:` ↔ MAJOR; também `docs`, `test`,
  `refactor`, `ci`, `build`, `chore`. Ex.: `feat(api): avaliação de explicação`,
  `fix(web): quebra de palavra longa a 320px`, `test(grounding): regressão pokémon`.
- **SemVer** (https://semver.org/) (a confirmar): `0.y.z` durante a disciplina;
  `v1.0.0` na entrega final.
- **Checklist de PR = DoD** (cole em `.github/pull_request_template.md`):
  ```markdown
  - [ ] Critérios de aceite atendidos (história: RF__)
  - [ ] Teste novo/atualizado; `uv run pytest` e `uv run ruff check .` passam
  - [ ] `npm run build` passa; se mexeu em tela, `npx playwright test` passa
  - [ ] Checklist manual do Lumen aplicado (se mexeu em tela)
  - [ ] Sem segredos no diff; nada sensível em `VITE_*`
  - [ ] Impacto LGPD avaliado (dado novo → termo, exportação, exclusão)
  - [ ] ADR criado/atualizado (se houve decisão de arquitetura)
  - [ ] Rodei `docker compose up --build` (ou explico por que não deu)
  ```

Fontes: Sommerville, *Software Engineering* 10ª ed. (https://software-engineering-book.com/);
ISO/IEC/IEEE 29148:2018; ISO/IEC 25010:2023 via arc42; Scrum Guide 2020;
OWASP Top 10:2025; OWASP ASVS 5.0; docs do Docker, Vite e GitHub citadas acima;
Lumen: `processo-de-design.md`, `acessibilidade.md`, `metodos-de-avaliacao.md`.
