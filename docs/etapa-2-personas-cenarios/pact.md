# Análise PACT — Etapa 2 (Define)

PACT (Benyon): **P**essoas, **A**tividades, **C**ontextos, **T**ecnologias. O
cenário de projeto fica na interseção dos quatro — é o que os slides da disciplina
chamam de encontrar o ponto onde as quatro dimensões se cruzam.

> Rótulos de origem, iguais aos de `personas.md`:
> `[questionário: pergunta N]` · `[hipótese da equipe]` · `[da literatura]`

---

## P — Pessoas

| Diferença | O que vale para o app |
|---|---|
| **Física (visão)** | Universitários com e sem baixa visão. Quem tem baixa visão usa ampliação de 200% a 400%, fonte do sistema aumentada, alto contraste, e às vezes leitor de tela para texto longo `[da literatura]`. Quantos dos respondentes já ajustam a leitura: `[questionário: pergunta 13]` |
| **Física (motora)** | Não é foco do projeto, mas alvo de toque pequeno atrapalha todo mundo no ônibus — RA10 cobre isso `[hipótese da equipe]` |
| **Cognitiva (conhecimento prévio)** | Varia com o período do curso. Importa porque analogia **ajuda o iniciante e estorva o avançado** (reversão de expertise) — daí o *fading* de DP08 `[da literatura]` |
| **Cognitiva (atenção, carga)** | O que mais atrapalhou na última dificuldade: `[questionário: pergunta 6]` |
| **Motivacional (interesses)** | Universos citados e profundidade de 1 a 5: `[questionário: perguntas 7 e 8]`. Fã casual e fã profundo pedem analogias diferentes (DP06) |
| **Atitude diante de IA** | Frequência de uso: `[questionário: pergunta 5]`. Se a maioria já usa IA para estudar, o app não compete com o caderno — compete com o ChatGPT, e o diferencial passa a ser o conteúdo curado e revisado (DP12) |

## A — Atividades

| Pergunta de PACT | Resposta |
|---|---|
| **Objetivo** | Entender um conceito técnico (o projeto usa "entrega confiável no TCP" como caso) a tempo de uma prova ou de uma entrega |
| **Frequência** | Alta perto de provas, quase nula fora delas `[hipótese da equipe]` |
| **Complexidade** | Uma sessão curta: escolher o conceito, ver a explicação, conferir se entendeu |
| **Interrupções** | Altas. Estudo no celular é interrompido por notificação, ônibus que chega, aula que começa `[hipótese da equipe]` |
| **Tempo** | Sessões de 5 a 15 minutos, não de uma hora `[hipótese da equipe]` |
| **Erro e consequência** | Consequência de um erro do app é **séria**: o aluno estuda errado e leva isso para a prova. Daí os validadores anti-alucinação e a revisão humana (RNF04, DP12) |

## C — Contextos

| Dimensão | Realidade |
|---|---|
| **Físico** | Celular no ônibus, quarto à noite, biblioteca, sala antes da aula. Luz variável, tela sob o sol, conexão instável `[questionário: pergunta 3]` |
| **Social** | Em geral sozinho; às vezes grupo de estudo comparando respostas `[questionário: pergunta 4, opção g]` |
| **Organizacional** | Material vem do professor, em PDF de slides — formato que **não reflui** e é a barreira concreta que o app tenta contornar. Prazo de prova é o que aciona o uso |

## T — Tecnologias

| | |
|---|---|
| **Entrada** | Toque no celular; teclado no notebook; **tudo tem de funcionar só com teclado** (RA11) |
| **Saída** | Tela com zoom do sistema, tema escuro e alto contraste; leitor de tela (NVDA, TalkBack); leitura em voz alta `[questionário: pergunta 13]` |
| **Conectividade** | Instável no ônibus. Explicação que depende de IA ao vivo pode demorar ou falhar — daí a reserva curada e a explicação padrão (RNF03) |
| **IA** | Modelo de linguagem **no back-end**, nunca no cliente; chave fora do front-end; saída validada antes de ser mostrada (RNF02, DP12) |

---

## A interseção: onde o projeto se decide

Cruzando as quatro dimensões, três conclusões que orientam o protótipo:

**1. Pessoa que amplia + contexto de ônibus + atividade interrompida = a
explicação tem de ser segmentada e retomável.** Não é escolha estética: é a
interseção de P, A e C. Sustenta RA23 e DP13.

**2. Material de origem em PDF que não reflui + pessoa com baixa visão = o maior
ganho do app não é a analogia, é o texto reflluível.** Vale registrar isso no
relatório, porque contraria a intuição de que o diferencial está na
personalização. Sustenta RA04 e RA05.

**3. Consequência séria de erro + IA no back-end = o validador vale mais que o
visual.** Se a pergunta 12 do questionário tiver média alta, isso deixa de ser
hipótese e passa a ter apoio nos dados. Sustenta RNF04, DP10 e DP12.

---

## Checklist

- [ ] Campos `[questionário: pergunta N]` substituídos por dado real
- [ ] Rótulos `[hipótese da equipe]` e `[da literatura]` mantidos
- [ ] As três conclusões da interseção revisadas contra os dados reais — se um dado
      contrariar uma delas, **mude a conclusão**, não o dado

## Fontes

- **Benyon** — PACT (Pessoas, Atividades, Contextos, Tecnologias). Edição em
  português: *Interação Humano-Computador*, Pearson, 2011. A descrição detalhada do
  PACT vem de conhecimento de manual **(a confirmar na obra)**.
- **Reversão de expertise** — analogia que ajuda o iniciante pode estorvar o
  avançado; base do *fading* (DP08).
- **WCAG 2.2** (W3C) — requisitos RA citados por número.
- `references/processo-de-design.md` §4.1; `assets/templates/cenario-pact.md`.
