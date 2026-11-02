# Plano de pesquisa — Etapa 1 (Entender)

Projeto da disciplina de IHC: app de apoio a estudos que explica conteúdos
técnicos usando o universo de interesse do aluno, com atenção a carga cognitiva e
acessibilidade para pessoas com baixa visão.

| | |
|---|---|
| Natureza | **Trabalho de disciplina, e só isso.** Não será publicado nem reaproveitado em outro trabalho |
| Prazo final do projeto inteiro | **09/11/2026** (as 4 etapas) |
| Tempo previsto para esta etapa | **1 a 2 dias** |
| Responsável | [preencher: nome] |
| Grupo | [preencher: integrantes] |
| Orientação | [preencher: professor(a)] |
| Versão | 3.0 — 02/11/2026 (questionário por WhatsApp) |

---

## 1. Objetivo

Levantar, com o esforço que o prazo permite, **como as pessoas estudam conteúdo
técnico, o que as faz desistir de uma explicação, quais interesses elas têm e que
ajustes de leitura fazem na tela** — o suficiente para sustentar as personas da
Etapa 2 e preencher a coluna "Rastreio" dos requisitos.

## 2. Método, declarado como ele é

**Instrumento único:** questionário de 12 perguntas enviado por **WhatsApp**, em
duas mensagens de texto (`questionario.md`). A pessoa responde na própria conversa.

**Quem responde:**

| Grupo | n esperado | O que isso vale |
|---|---|---|
| Integrantes do grupo, respondendo como parte do público-alvo | 3 a 5 | **Hipótese da equipe**, não evidência externa |
| Amigos, colegas de turma e parentes universitários | 10 a 20 | Amostra de conveniência pequena |

**O que este desenho é:** levantamento exploratório de conveniência, que serve
para formar **proto-personas** — personas de hipótese, construídas sem pesquisa
externa, que a literatura de IHC reconhece como ponto de partida legítimo e barato
(Laubheimer, NN/g, 2020).

**O que ele não é:** não permite generalizar, não mede nada e não substitui
pesquisa com o público real. O limite conhecido da proto-persona é **reforçar as
suposições de quem a escreveu** — e quando a própria equipe responde, esse risco
cresce.

**Isso é um problema?** Para um trabalho de disciplina, não, **desde que o
relatório declare o desenho**. O que custa nota não é amostra pequena; é
apresentar opinião da equipe como achado de pesquisa. O texto pronto está no §7.

### Por que WhatsApp funciona aqui

- Taxa de resposta muito maior que link de formulário, no círculo de contatos.
- Texto de conversa respeita o tamanho de fonte do celular e funciona com leitor
  de tela — **desde que enviado como texto, nunca como print**.
- Custo zero de ferramenta.

**O preço:** a coleta **não é anônima** — você vê quem responde. Isso muda o que
pode ser prometido (veja §3) e tira do questionário a pergunta sobre deficiência.

### Dois ajustes de custo quase zero

1. **Inclua pelo menos 3 pessoas de fora do grupo.** É a diferença entre hipótese
   fechada e hipótese testada de leve.
2. **Procure 1 pessoa que aumente a letra ou use zoom** — pode ser um parente mais
   velho com o celular. É diretamente relevante ao foco do projeto. Se não
   encontrar, **declare no relatório** em vez de simular.

## 3. Ética — resolve em uma conversa

O trabalho é **exclusivamente de disciplina**, então se enquadra na dispensa do
art. 1º, parágrafo único, inciso VIII, da **Res. CNS 510/2016** ("atividade
exclusivamente de educação, ensino ou treinamento, sem finalidade de pesquisa
científica").

- [ ] **Confirmar com o(a) professor(a)** que a dispensa se aplica e anotar a data
      da confirmação: ____/____/______

**Consentimento:** a mensagem de convite, respondida pela pessoa, é o registro —
os arts. 2º e 15 da Res. 510/2016 admitem registro digital. Detalhes em
`consentimento.md`.

**O que muda por não ser anônimo.** Você sabe quem respondeu, então:

- O convite **não diz "anônimo"**, e sim que nome e número **não serão registrados
  junto das respostas**;
- essa promessa tem que ser cumprida na tabulação: **a planilha usa R01, R02…, sem
  nome e sem telefone**;
- em compensação, se alguém pedir para excluir as respostas, você consegue atender
  (LGPD art. 18) — o que seria impossível num formulário anônimo.

**LGPD, o mínimo que basta:**

- Nome e número de telefone ficam fora da planilha.
- Faixa etária, não data de nascimento.
- **Nenhuma pergunta sobre deficiência.** Dado sobre deficiência é sensível
  (art. 11) e, num canal onde você sabe quem é a pessoa, pedir essa declaração a um
  amigo ou parente é constrangedor e desnecessário. A pergunta 13 investiga
  **comportamento** de leitura, que é o que o projeto precisa.
- Se alguém responder em áudio: transcreva e **apague o áudio** — voz identifica.
- Respostas apagadas até **[preencher: data]**.

## 4. Acessibilidade do próprio instrumento

Pouco, mas não zero — e o professor nota:

- [ ] Enviar como **texto**, nunca como imagem ou print do questionário
- [ ] Toda âncora de escala rotulada em texto ("1 = discordo totalmente"), não só
      o número (princípio do `1.3.3 Características sensoriais (A)`)
- [ ] Opções com letra curta e digitável, para responder com o polegar
- [ ] Mandar para si mesmo primeiro e reler no celular, com a fonte aumentada
- [ ] Enviar **individualmente**, não em grupo: em grupo a primeira resposta ancora
      as demais e expõe todas as respostas a todos

## 5. Análise — contagem simples

1. Planilha com uma linha por pessoa, uma coluna por pergunta, primeira coluna com
   o código R01, R02…
2. **Inverter as perguntas 10 e 12** (6 menos o valor) antes de somar com as
   positivas: são negativas de propósito, contra viés de aquiescência.
3. Contar frequências: materiais usados, uso de IA, o que mais atrapalha, universos
   citados, quantos ajustam a leitura na tela.
4. Escrever **3 a 5 achados**, cada um com o número que o sustenta.
5. Separar as respostas da pergunta 7 e os **comentários soltos** que as pessoas
   mandarem fora da pergunta — em conversa isso acontece muito, e costuma ser o
   material mais citável para a proto-persona.

**Reporte a contagem absoluta, não só porcentagem.** Com n de 15, "60%" são 9
pessoas.

Saída: `sintese.md`, uma página.

## 6. Cronograma de 2 dias

| Quando | O quê |
|---|---|
| Dia 1, manhã | Preencher os campos `[preencher]` da Mensagem 1; mandar para si mesmo e revisar no celular |
| Dia 1, tarde | Confirmar a dispensa com o professor; enviar individualmente para grupo, turma, amigos e parentes |
| Dia 2, manhã | Cobrar quem não respondeu; fechar a coleta |
| Dia 2, tarde | Tabular, escrever `sintese.md` com 3 a 5 achados, preencher a coluna "Rastreio" dos requisitos |

Sobram 5 dias para as Etapas 2, 3 e 4 — onde está o trabalho pesado (protótipo e
avaliação). Esta etapa **não** deve consumir mais que isso.

## 7. Texto pronto para o relatório — limitações

Cole na seção de método ou de limitações. É o que transforma amostra fraca em
escolha metodológica declarada:

> **Limitações da pesquisa com usuários.** Por restrição de prazo, a Etapa 1
> empregou um questionário de 12 itens aplicado por mensagem de texto (WhatsApp) a
> uma amostra de conveniência (n = __), composta pelos integrantes do grupo,
> respondendo na condição de estudantes do público-alvo, e por colegas, amigos e
> familiares universitários. A coleta não foi anônima, dado o canal utilizado; as
> respostas foram pseudonimizadas na tabulação (R01, R02…), sem registro de nome ou
> número de telefone. O desenho é exploratório e serviu para construir
> **proto-personas**, isto é, personas de hipótese, conforme a classificação de
> Laubheimer (NN/g, 2020), e não personas qualitativas derivadas de entrevistas.
> Consequentemente: (a) os resultados não permitem generalização; (b) há risco de
> as personas refletirem suposições da própria equipe, limite reconhecido da
> técnica; (c) não foram coletados dados sobre deficiência, por serem dados
> sensíveis em canal não anônimo, de modo que as decisões de acessibilidade do
> projeto se apoiam nos critérios da WCAG 2.2 e na literatura, e não em evidência
> obtida com usuários com baixa visão. Simulação de baixa visão não foi utilizada
> como substituto, por não ser equivalente à experiência de quem usa tecnologia
> assistiva cotidianamente.

Se você conseguir um respondente que use ampliação de tela, acrescente: "um
participante relatou uso regular de ampliação de tela, e seus relatos são tratados
como qualitativos, sem generalização".

## 8. Rastreabilidade — é isso que diferencia o trabalho

```
achado do questionário → proto-persona → requisito (RF/RNF + RA/DP) →
elemento do protótipo → tarefa do teste
```

A coluna "Rastreio" em `docs/requisitos/requisitos.md` está **vazia**. Preenchê-la
é a entrega mais valiosa desta etapa, e leva meia hora:

| Requisito | O que buscar nas respostas |
|---|---|
| RF02 (informar interesses e o quanto conhece deles) | Perguntas 7 e 8 |
| RF04 (ver explicação sem analogia a um toque) | Pergunta 11 → sustenta DP05 e RA21 |
| RF06 (texto ampliado e alto contraste) | Perguntas 13 e 14 → sustentam RA01, RA04, RA20 |
| RF05 (avisar que a explicação está errada) | Pergunta 12 → sustenta DP10 |
| RF03 (explicação em passos curtos) | Pergunta 6, opções b e c |
| RNF01 (WCAG 2.2 AA) | Pergunta 13 prioriza RA01 a RA10 |

**Regra para a Etapa 2:** persona e requisito sem achado que os sustente são
suposição — rotule como tal. Com proto-personas, quase tudo será suposição
rotulada, e isso é aceitável **porque está rotulado**.

## 9. O que foi cortado, e o que você perde

Registro honesto, para o caso de o professor perguntar:

| Cortado | O que se perde |
|---|---|
| 8 a 12 entrevistas semiestruturadas | O *porquê*. Questionário dá distribuição, não explicação |
| Participantes com baixa visão | Evidência própria sobre o foco central do projeto. Ficam a norma e a literatura |
| Análise temática reflexiva (Braun e Clarke) | Profundidade analítica. Vira contagem simples |
| Termo de consentimento assinado | Nada, neste desenho: sem gravação e sem dado identificável na planilha, o consentimento na conversa basta (Res. 510/2016, arts. 2º e 15) |
| Pergunta sobre deficiência | Nada que o projeto precise: a pergunta 13 cobre o comportamento de leitura sem pedir dado sensível em canal identificado |
| Formulário web | Anonimato na coleta. Em troca, taxa de resposta muito maior |

O roteiro de entrevista continua no repositório (`roteiro-entrevista.md`), reduzido
a seis perguntas e **opcional**: se sobrar uma tarde, duas conversas de 10 minutos
rendem as citações que o questionário não dá.

## Fontes

- **Res. CNS 510/2016** — art. 1º, parágrafo único, inciso VIII (dispensa para
  atividade exclusivamente de ensino); arts. 2º e 15 (registro digital de
  consentimento); art. 17 (conteúdo do registro).
- **LGPD** (Lei 13.709/2018) — arts. 7º, 11 e 18.
- **Laubheimer, NN/g (2020)** — tipos de persona: proto-persona (hipótese, baixo
  custo, risco de reforçar suposição), qualitativa e estatística.
- **WCAG 2.2** (W3C) — critérios citados por número e nível.
- `references/processo-de-design.md` §3.1; `references/metodos-de-avaliacao.md` §11.
