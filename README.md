# Estudos do Seu Jeito

**Aplicativo web de apoio aos estudos que explica conteúdos técnicos por meio de
analogias com o universo de interesse do estudante: um jogo, uma série, um
esporte, um anime.**

Projeto da disciplina de **Interação Humano-Computador** do curso de Engenharia
da Computação da **UNIARA — Universidade de Araraquara**, 2026.

---

## Integrantes

- Gustavo Henrique Femiano
- Jean Domiciano de Menezes
- João Pedro de Jesus Miranda
- Vinicius Gussoni Vellosa
- Yasmim Fernandes de Paula

---

## Sobre o projeto

Na pesquisa com estudantes feita na Etapa 1, o principal obstáculo relatado ao
estudar conteúdos técnicos foi a **explicação abstrata demais** (4 de 5
respondentes), e não a dificuldade de leitura. A proposta do aplicativo é tornar
o conceito concreto comparando-o com algo que o estudante já conhece bem,
sem abrir mão da correção técnica.

### Como funciona

1. O estudante conversa com o aplicativo numa interface de chat, no modelo dos
   assistentes de IA que já usa para estudar.
2. Ele escreve **o assunto** que quer entender (por exemplo, "TCP" ou
   "árvore B") e **o universo** que quer usar na comparação.
3. A explicação chega em mensagens curtas, uma etapa por vez, seguindo o modelo
   *Teaching-With-Analogies* (Glynn): o conceito, a cena da analogia, a
   correspondência entre os elementos, **onde a comparação deixa de valer**, a
   versão técnica e uma pergunta para verificar o entendimento.
4. A qualquer momento é possível ver a **versão técnica, sem analogia**, trocar
   de universo ou marcar a explicação como errada.
5. O estudante pode fazer perguntas, que são respondidas **somente dentro do
   assunto escolhido**.

### Confiabilidade do conteúdo

Analogias geradas por IA podem soar convincentes e estar erradas. Para reduzir
esse risco, o aplicativo:

- **pesquisa o assunto na web** (API do Gemini com Google Search) e monta um
  texto de referência com fontes, que são exibidas ao estudante antes da
  explicação;
- submete cada explicação a uma **autoverificação** da própria IA, inspirada no
  método *Chain-of-Verification* (Dhuliawala et al., 2024), conferindo-a contra
  esse texto de referência;
- aplica **validadores automáticos**, como a exigência de que cada
  correspondência da analogia cite um trecho literal da referência;
- mostra a **explicação padrão, sem analogia**, quando a explicação adaptada não
  passa na verificação. Nunca exibe conteúdo reprovado.

As decisões e seus limites estão registrados no
[ADR 0003](docs/adr/0003-autoverificacao-da-ia.md).

### Acessibilidade e privacidade

- Desenvolvido para atender à **WCAG 2.2, nível AA**, com atenção a estudantes
  com **baixa visão**: texto ampliável até 200%, tema de alto contraste
  (amarelo sobre preto), reorganização do conteúdo sem rolagem lateral a 320 px,
  navegação completa por teclado e compatibilidade com leitores de tela.
- Testes automatizados com **axe-core** nas telas principais, no celular e no
  computador.
- **Nenhum dado pessoal identificável é solicitado**: não há cadastro com nome
  ou e-mail. O estudante pode ver e apagar tudo o que foi guardado, em atenção
  à **LGPD**.

---

## Etapas do projeto

O trabalho segue o ciclo de design centrado no usuário (ISO 9241-210):
**Entender → Desenhar → Avaliar**.

| Etapa | Conteúdo | Situação |
|---|---|---|
| **1. Pesquisa com usuários** | Plano de pesquisa, questionário e síntese dos resultados (n = 5) | Concluída |
| **2. Personas e cenários** | Personas, análise PACT, cenários e tarefas de teste | Concluída |
| **3. Prototipação** | Esboços de baixa fidelidade, decisões de design e o aplicativo funcional como protótipo de alta fidelidade | Concluída |
| **4. Avaliação** | Avaliação heurística, percurso cognitivo com as personas e auditoria WCAG 2.2, com correções aplicadas; protocolo do teste de usabilidade e SUS prontos | Avaliação analítica concluída; teste com usuários pendente |

O **relatório final** do projeto está em [`docs/relatorio-final.docx`](docs/relatorio-final.docx), e a avaliação da Etapa 4 em [`docs/etapa-4-avaliacao/avaliacao-etapa-4.docx`](docs/etapa-4-avaliacao/avaliacao-etapa-4.docx).

Cada documento indica a origem do que afirma (dado da pesquisa, literatura ou
hipótese da equipe), formando uma cadeia de rastreabilidade do achado da
pesquisa até o requisito, a decisão de design, o código e o teste. O ponto de
partida é o [índice da documentação](docs/README.md).

---

## Organização do repositório

```
.
├── apps/
│   ├── api/                  Back-end (Python, FastAPI)
│   │   ├── app/
│   │   │   ├── routers/      Rotas da API
│   │   │   ├── services/     Pesquisa na web, explicações, autoverificação, perguntas
│   │   │   ├── providers/    Integração com os modelos de IA
│   │   │   ├── validators/   Validadores automáticos do conteúdo
│   │   │   └── prompts/      Instruções enviadas à IA
│   │   ├── content/          Conteúdos pré-gravados (texto-base e explicações)
│   │   └── tests/            Testes da API (pytest)
│   └── web/                  Front-end (TypeScript, React)
│       ├── src/              Interface: chat, preferências de leitura, dados do usuário
│       └── e2e/              Testes de ponta a ponta e de acessibilidade (Playwright + axe)
├── docs/
│   ├── etapa-1-pesquisa/           Plano, questionário e síntese da pesquisa
│   ├── etapa-2-personas-cenarios/  Personas, PACT e cenários
│   ├── etapa-3-prototipo/          Esboços e decisões de design
│   ├── etapa-4-avaliacao/          Protocolo do teste, SUS, heurísticas, auditoria WCAG
│   ├── requisitos/                 Requisitos funcionais e não funcionais
│   └── adr/                        Registros de decisões de arquitetura
├── compose.yaml              Orquestração com Docker (banco, API e front-end)
└── .env.example              Modelo de configuração (sem segredos)
```

---

## Tecnologias

| Parte | Tecnologias |
|---|---|
| Front-end | TypeScript, React 19, Vite |
| Back-end | Python 3.12+, FastAPI, Pydantic, SQLAlchemy |
| Banco de dados | PostgreSQL 18 |
| Inteligência artificial | API do Gemini (geração, autoverificação e pesquisa com Google Search) |
| Infraestrutura | Docker e Docker Compose |
| Testes | pytest, Playwright, axe-core |

---

## Como executar

### Pré-requisitos

- [Git](https://git-scm.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (inclui o Docker Compose)
- Opcional, para usar a IA: uma chave da API do Gemini, gerada em
  [Google AI Studio](https://aistudio.google.com/apikey)

### 1. Obter o código e criar a configuração

```bash
git clone https://github.com/ViniciusVellosa/app-estudos.git
cd app-estudos
cp .env.example .env
```

No Windows (PowerShell), troque a última linha por `Copy-Item .env.example .env`.

O arquivo `.env` guarda a configuração local e **não é enviado ao repositório**.
Antes de subir, troque o valor de `POSTGRES_PASSWORD`.

### 2. Subir o aplicativo

```bash
docker compose up --build --wait
```

| Serviço | Endereço |
|---|---|
| Aplicativo | <http://localhost:5173> |
| Documentação da API | <http://localhost:8000/docs> |

Para encerrar: `docker compose down`.

Com a configuração padrão, o aplicativo funciona **sem IA**: o assunto
disponível é *Entrega confiável no TCP*, com explicação pré-gravada. Esse é o
modo usado no teste de usabilidade, para que as sessões não dependam de rede
nem de cota da API.

### 3. Ativar a IA (opcional)

No arquivo `.env`, defina:

```
EXPLANATION_PROVIDER=llm
LLM_BACKEND=openai_compatible
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
LLM_MODEL=gemini-3.8-flash
LLM_API_KEY=sua-chave-aqui
PESQUISA_PROVIDER=gemini
```

Antes de abrir o navegador, é possível conferir a configuração com uma chamada
real à API (requer o [uv](https://docs.astral.sh/uv/)):

```bash
cd apps/api
uv sync --extra llm
uv run python -m app.smoke --pesquisa "árvore B" "futebol"
```

O teste mostra o texto pesquisado, as fontes encontradas e se a explicação foi
aprovada na verificação. Depois, suba o aplicativo novamente com
`docker compose up --build --wait`.

> O plano gratuito da API do Gemini tem limites de uso. Cada explicação gera
> algumas chamadas ao modelo (rascunho, verificação e, para assuntos novos, a
> pesquisa). Se aparecer o erro HTTP 429, o limite foi atingido; o erro
> HTTP 503 indica sobrecarga temporária do serviço.

### Executar os testes

```bash
# API
cd apps/api
uv run pytest

# Interface, acessibilidade e fluxos completos (sobe a API e o front-end sozinho)
cd apps/web
npm install
npx playwright install chromium
npx playwright test
```

### Executar sem Docker

Requer o [uv](https://docs.astral.sh/uv/) e o [Node.js](https://nodejs.org/) 24.

```bash
# Terminal 1: API, com banco SQLite local
cd apps/api
uv sync --extra llm
uv run fastapi dev app/main.py

# Terminal 2: front-end
cd apps/web
npm install
npm run dev
```

---

## Dados da pesquisa

As respostas do questionário da Etapa 1 **não fazem parte deste repositório**.
Os documentos apresentam apenas resultados agregados e respostas identificadas
por códigos (R01 a R05), conforme o compromisso assumido com os participantes.

---

## Uso de ferramentas de IA no desenvolvimento

Ferramentas de IA generativa (Claude, da Anthropic) foram usadas como apoio na
programação, na revisão de acessibilidade e na organização da documentação.
As decisões de projeto, a pesquisa com usuários e a avaliação são da equipe,
e as fontes consultadas estão citadas nos documentos de cada etapa.
