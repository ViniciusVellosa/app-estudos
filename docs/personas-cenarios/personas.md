# Personas — Etapa 2 (Define)

> **Como usar este arquivo.** Ele já está estruturado; falta preencher. Cada campo
> traz entre colchetes **de onde a informação vem**:
>
> - `[questionário: pergunta N]` — preencher com o resultado da Etapa 1
> - `[hipótese da equipe]` — suposição; mantenha o rótulo no relatório
> - `[da literatura]` — vem de fonte citada, não dos seus dados
>
> Não apague os rótulos. Eles são o que torna a entrega defensável.

## Status: proto-personas

Estas são **proto-personas** — personas de hipótese, construídas sem pesquisa
externa aprofundada, conforme a classificação de Laubheimer (NN/g, 2020). O
questionário da Etapa 1 dá perfil e distribuição, não entrevistas. O limite
conhecido da técnica é **reforçar as suposições de quem escreveu**, e isso vale em
dobro aqui, porque parte dos respondentes é o próprio grupo.

Declare isso no relatório. O texto pronto está em `../pesquisa/plano-de-pesquisa.md` §7.

---

## Persona 1 — Ana (primária): estudante com baixa visão

> **Atenção, e isto é o ponto mais importante deste arquivo.** O questionário da
> Etapa 1 **não coleta dado sobre deficiência**, por decisão de privacidade (canal
> identificado, dado sensível pela LGPD art. 11 — ver
> `../pesquisa/plano-de-pesquisa.md` §3). Logo, **esta persona não vem dos seus
> dados.** Ela é construída a partir de:
>
> - os critérios da **WCAG 2.2** e os requisitos RA01 a RA24 do projeto;
> - as **Stories of Web Users** do W3C WAI, em especial *Elias* (baixa visão,
>   ajudado por texto ajustável e layout consistente);
> - as **accessibility personas do GOV.UK** (2019), em especial *Ashleigh*.
>
> Mantenha esse rótulo no relatório: é uma persona **fundamentada em literatura e
> norma**, não em evidência coletada pelo grupo. O GOV.UK afirma explicitamente
> que esse recurso **não substitui teste com usuários reais**. Se durante a Etapa 1
> algum respondente relatar uso de ampliação ou leitor de tela (pergunta 13), ele
> entra aqui como evidência — e aí diga quantos foram.

> "[citação — se algum respondente comentar algo sobre ler na tela, use a frase
> literal dele. Se não houver, **deixe sem citação** em vez de inventar uma]"

| | |
|---|---|
| Idade / curso / período | 21 anos · `[preencher]` · `[preencher]` |
| Condição | Baixa visão. **Descreva pelo comportamento, não pelo diagnóstico:** usa ampliação, aproxima o rosto da tela, cansa rápido em texto longo `[da literatura]` |
| Rotina de estudo | `[questionário: perguntas 3 e 4]` — ex.: estuda no celular, à noite, com slides em PDF |
| Universo de interesse e profundidade | `[questionário: perguntas 7 e 8]` — anote o universo **e** o nível de 1 a 5. Fã casual e fã profundo pedem explicações diferentes |
| Tecnologia e acessibilidade | Zoom de 200% a 400%; fonte do sistema aumentada; tema escuro ou alto contraste; leitor de tela às vezes, para texto longo `[da literatura]` |
| Contexto (PACT) | Ver `pact.md` |

### Objetivos

- **De experiência:** não se sentir mais lenta que a turma por causa da leitura.
- **Final (tarefa):** entender um conceito de redes a tempo da prova, sem precisar
  reler o mesmo parágrafo cinco vezes.

### Dores e barreiras

Cada dor precisa apontar para um achado ou para uma fonte. Preencha a coluna:

| Dor | Origem |
|---|---|
| Perde a linha do texto quando amplia e a página rola para o lado | `[da literatura: 1.4.10 Realinhar (AA)]` → RA05 |
| PDF de slides não reflui: ampliar significa rolar em duas direções | `[da literatura]` → RA04 |
| Texto longo sem divisão cansa antes do fim | `[da literatura: COGA]` → RA23 |
| Botão que desaparece atrás de cabeçalho fixo quando o foco chega nele | `[da literatura: 2.4.11 Foco não obscurecido (AA)]` → RA09 |
| `[questionário: pergunta 6 — o que mais atrapalhou]` | `[preencher]` |

### Como a personalização ajuda — e onde pode atrapalhar

- **Ajuda:** a analogia dá uma estrutura já conhecida para pendurar o conceito
  novo, o que reduz o esforço de manter tudo na memória de trabalho ao mesmo tempo
  em que se luta com a leitura.
- **Risco:** se a analogia vier como imagem ou tabela larga, ela **piora** a
  situação de quem amplia — vira exatamente a barreira que o projeto quer resolver
  (DP02, RA05). A tabela de mapeamento analogia↔conceito tem de virar lista
  empilhada a 320px.
- **Risco:** tom infantilizado. Alguém que já luta para ser levado a sério
  academicamente não quer explicação de desenho animado (DP18).

### Necessidades de acessibilidade e critérios

| Necessidade | Critério | Requisito |
|---|---|---|
| Ler texto ampliado sem rolagem lateral | `1.4.10 Realinhar (AA)` | RA05 |
| Ampliar a 200% sem perder conteúdo | `1.4.4 Redimensionar texto (AA)` | RA04 |
| Contraste suficiente em todos os temas | `1.4.3 Contraste mínimo (AA)` | RA01 |
| Ver onde está o foco, sempre | `2.4.7 Foco visível (AA)`, `2.4.11 (AA)` | RA09 |
| Explicação técnica sem analogia, a um toque | `3.1.5 (AAA)` / COGA | RA21, DP05 |
| Explicação longa segmentada, no ritmo dela | COGA | RA23, DP13 |

### Cenário-chave

`cenarios.md` → Cenário 1.

---

## Persona 2 — Rafa (secundária): estudante sem deficiência, sem tempo

> Esta persona **sim** deve sair do questionário. É o perfil da maioria dos seus
> respondentes, inclusive do grupo.

> "[citação — use a resposta mais expressiva da pergunta 6 ou um comentário solto
> que alguém mandou junto]"

| | |
|---|---|
| Idade / curso / período | `[questionário: perguntas 1 e 2]` |
| Rotina de estudo | `[questionário: perguntas 3 e 4]` |
| Uso de IA | `[questionário: pergunta 5]` — se a maioria já usa, isso muda o projeto: o app não compete com o caderno, compete com o ChatGPT |
| Universo de interesse e profundidade | `[questionário: perguntas 7 e 8]` |
| Atitude diante da personalização | `[questionário: perguntas 9 a 12]` — lembre de **inverter 10 e 12** |

### Objetivos

- **De experiência:** entender rápido, sem sentir que está perdendo tempo.
- **Final (tarefa):** `[preencher a partir da pergunta 6]`

### Dores e barreiras

| Dor | Origem |
|---|---|
| `[questionário: pergunta 6, opção mais marcada]` | `[preencher: quantos de quantos]` |
| `[questionário: pergunta 6, segunda mais marcada]` | `[preencher]` |

### Como a personalização ajuda — e onde pode atrapalhar

- **Ajuda:** `[questionário: perguntas 9 e 10]`
- **Risco:** se a pergunta 12 tiver média alta, o risco principal é **perda de
  confiança por erro factual sobre o universo** — e aí a prioridade de engenharia
  passa a ser o validador anti-alucinação, não o visual (DP10, RF05).
- **Risco:** se a pergunta 11 tiver média alta, as pessoas querem a versão técnica
  disponível. Isso confirma RF04 e DP05 e **sobe a prioridade** do botão "sem
  analogia".

### Necessidades de acessibilidade

Mesmo sem deficiência declarada, `[questionário: pergunta 13]` deve mostrar
quantos usam modo escuro, fonte aumentada ou zoom. **Esse número é o argumento
mais forte do seu relatório:** se metade dos respondentes sem deficiência já
ajusta a leitura, acessibilidade deixa de ser "recurso para um grupo" e passa a
ser requisito geral.

### Cenário-chave

`cenarios.md` → Cenário 2.

---

## Persona 3 — opcional, se houver dados que a sustentem

Só crie se o questionário revelar um perfil claramente distinto dos dois acima —
por exemplo, alguém que **não** usa IA e desconfia da personalização (pergunta 12
alta, pergunta 9 baixa). Esse perfil é valioso: é o cético, e desenhar para ele
evita um app que só agrada quem já estava convencido.

**Não invente uma terceira persona para "ficar mais completo".** Três personas
fracas valem menos que duas sustentadas.

---

## Espectro de personas (Microsoft Inclusive Design)

A mesma necessidade aparece em três intensidades. É o argumento de "resolver para
um, estender para muitos", e cabe em um parágrafo do relatório:

| Necessidade: ler conteúdo denso na tela | Quem |
|---|---|
| **Permanente** | Baixa visão (Ana) |
| **Temporária** | Olho dilatado após consulta, conjuntivite, pós-cirurgia |
| **Situacional** | Celular sob o sol, no ônibus em movimento, 2h da manhã na véspera da prova (Rafa) |

As três se beneficiam das **mesmas** decisões: contraste alto, texto que reflui,
segmentação, foco visível. É por isso que RA01 a RA10 não são "requisitos de
acessibilidade" à parte — são requisitos do produto.

---

## Checklist antes de fechar a Etapa 2

- [ ] Cada campo `[questionário: pergunta N]` foi substituído por dado real
- [ ] Cada campo `[hipótese da equipe]` e `[da literatura]` **manteve** o rótulo
- [ ] Nenhuma citação foi inventada: ou é frase literal de alguém, ou não existe
- [ ] A persona 1 declara que vem de literatura e norma, não dos seus dados
- [ ] Cada dor aponta para um número do questionário ou para uma fonte
- [ ] Cada persona tem um cenário em `cenarios.md`
- [ ] A coluna "Rastreio" de `../requisitos/requisitos.md` foi preenchida

## Fontes

- **Laubheimer, NN/g (2020)** — proto-persona, persona qualitativa e estatística;
  o risco de a proto-persona reforçar suposições da equipe.
- **Pruitt e Grudin (2003)** — personas como veículo de dados qualitativos e
  quantitativos para a equipe.
- **Microsoft Inclusive Design** — "recognize exclusion", "solve for one, extend to
  many"; espectro permanente / temporário / situacional.
- **W3C WAI, Stories of Web Users** — Elias (baixa visão), Ashleigh, entre outras;
  as histórias "represent the experiences of some people with disabilities".
- **GOV.UK accessibility personas (2019)** — e a ressalva explícita de que
  **não substituem teste com usuários reais**.
- **Walkington e Bernacki** — universo de interesse e profundidade de engajamento.
- **WCAG 2.2** (W3C) — critérios citados por número e nível.
- `references/processo-de-design.md` §3; `assets/templates/persona.md`.
