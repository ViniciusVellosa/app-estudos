# SUS — System Usability Scale em português

**Versão usada:** tradução e adaptação transcultural brasileira de **Lourenço,
Carmona e Lopes (2022)**, *Aquichan* 22(2):e2228, DOI
`10.5294/aqui.2022.22.2.8` (α de Cronbach = 0,76; n = 100 universitários).
Instrumento original: **Brooke (1996)**.

Usar a versão validada, e não uma tradução própria, é o que permite comparar o seu
escore com a média de referência da literatura. **Cite a fonte no relatório.**

| | |
|---|---|
| Quando aplicar | Ao final da sessão, **depois** de todas as tarefas e **antes** do debrief |
| Por que nessa ordem | Se a conversa final vier primeiro, ela contamina as notas |
| Quantas vezes | Uma, sobre o app como um todo. Não aplique por tarefa |

---

## Instruções ao participante

> "Agora quero que você avalie o aplicativo como um todo, pensando em tudo o que
> fez hoje. São 10 frases. Para cada uma, diga o quanto concorda, de **1, discordo
> totalmente**, a **5, concordo totalmente**. Não há resposta certa ou errada —
> responda pela primeira impressão. Se não tiver certeza, marque 3."

Em todas as frases, "sistema" = o aplicativo testado hoje.

| # | Afirmação | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 1 | Eu acho que gostaria de usar esse sistema frequentemente. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | Eu achei esse sistema desnecessariamente complexo. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | Eu achei esse sistema fácil de usar. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | Eu achei que precisaria de ajuda de uma pessoa técnica para ser capaz de usar esse sistema. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | Eu achei que as várias funções desse sistema foram bem integradas. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | Eu acho que o sistema apresenta muita inconsistência. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | Eu imagino que a maioria das pessoas pode aprender a usar esse sistema rapidamente. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8 | Eu achei esse sistema muito pesado para usar. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 9 | Eu me senti muito seguro usando o sistema. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 10 | Eu precisei aprender muitas coisas antes que pudesse utilizar esse sistema. | ☐ | ☐ | ☐ | ☐ | ☐ |

**1 = discordo totalmente · 5 = concordo totalmente.** Rotule os extremos em texto
no formulário, não só os números.

### Regras que não podem ser quebradas

- **Não troque a ordem** dos itens.
- **Não inverta os itens negativos** no formulário. A alternância
  positivo/negativo faz parte do instrumento; a inversão acontece **no cálculo**.
- **Não junte nem corte itens.** Nove itens não são um SUS.
- Se um participante perguntar o que é "muito pesado" (item 8), explique de forma
  neutra: "pesado no sentido de trabalhoso, complicado de usar" — e use **a mesma**
  explicação com todos.

### Duas notas de redação, para você decidir e declarar

**Item 7:** a Tabela 1 do artigo (versão de consenso) traz "aprender a usar esse
sistema **rapidamente**"; o texto de Resultados traz "muito rapidamente", e o
original inglês é "very quickly". Este arquivo usa a forma da Tabela 1. Escolha
**uma**, use com todos e declare a escolha.

**Item 9:** use "segura" ou "seguro" conforme o participante. A forma neutra
"Eu me senti com muita segurança usando o sistema" **não é validada** — se usar,
declare no relatório.

---

## Como pontuar

1. Itens **ímpares** (1, 3, 5, 7, 9): contribuição = **resposta − 1**
2. Itens **pares** (2, 4, 6, 8, 10): contribuição = **5 − resposta**
3. Some as 10 contribuições (0 a 40) e **multiplique por 2,5** → escore de 0 a 100

```
SUS = 2,5 × [ (q1−1) + (5−q2) + (q3−1) + (5−q4) + (q5−1)
            + (5−q6) + (q7−1) + (5−q8) + (q9−1) + (5−q10) ]
```

**Exemplo.** Respostas 4, 2, 4, 1, 4, 2, 5, 2, 4, 2:
ímpares (3+3+3+4+3 = 16) + pares (3+4+3+3+3 = 16) = 32 × 2,5 = **80**.

### Interpretar sem exagerar

- **O escore não é porcentagem.** 80 não quer dizer "80% de aprovação".
- Média de referência da literatura: **68**, que é o percentil 50.
- Escala curva de Sauro e Lewis: 68 ≈ **C**; 80,8 a 84,0 = **A**; ≥ 84,1 = **A+**.
- **Reporte o escore global** com média, intervalo de confiança de 95%, a nota na
  curva e o **n**. Exemplo: "SUS médio = 78 (IC 95% 64–92; nota B na curva
  Sauro-Lewis; n = 5)".
- **Não use as subescalas.** O script as imprime, mas Lewis e Sauro (2017)
  recomendam relatar o escore geral. Com n = 5 elas não significam nada.
- Com 3 a 5 participantes o intervalo de confiança é **largo**. Diga isso. O SUS é
  indicador complementar, não prova de usabilidade — o que diagnostica *por que*
  são as observações e o SEQ.
- **Resposta incoerente:** se alguém marcar 5 no item 3 ("fácil") e 5 no item 2
  ("complexo"), provavelmente se confundiu com a alternância. **Registre e
  comente — não "corrija" a resposta.**

---

## Planilha e cálculo automático

Salve em `sus-respostas.csv`, uma linha por participante, **sem nome**:

```csv
id;q1;q2;q3;q4;q5;q6;q7;q8;q9;q10
P1;4;2;4;1;4;2;5;2;4;2
P2;3;3;4;2;3;2;4;3;3;3
P3;5;1;5;1;4;1;5;1;5;1
```

- Inteiros de 1 a 5, sem espaços, sem célula vazia.
- Se um item ficou sem resposta, **não invente**: deixe o participante fora do
  cálculo e relate isso.
- Salve em UTF-8. O script aceita `;`, `,` ou tabulação como separador.

A skill do Lumen traz a calculadora pronta. Neste repositório, no Windows:

```bash
python .claude/skills/lumen-ihc-acessibilidade/scripts/sus_calculator.py docs/etapa-4-avaliacao/sus-respostas.csv
```

Ela imprime escore por participante, média, IC 95%, nota na curva e a faixa de
adjetivo. Para saída em JSON, acrescente `--json`.

> **Confira o cálculo de um participante à mão** na primeira vez, com a fórmula
> acima. Não é desconfiança do script: é que num trabalho avaliado você precisa
> saber explicar de onde o número veio se o professor perguntar.

---

## Participante que usa ampliação ou leitor de tela

> As orientações abaixo são **boa prática inferida** dos princípios da WCAG e da
> orientação do W3C sobre testes com usuários com deficiência. Não há fonte
> específica verificada sobre aplicar o SUS a pessoas com baixa visão.

**Ofereça antes, sem presumir:** "prefere responder no seu celular, numa folha em
letra grande, ou que eu leia as frases e anote?"

| Formato | Como preparar |
|---|---|
| **Digital** | Um item por pergunta, 5 botões de opção; **sem** grade de múltipla escolha; cada opção com texto ("1 – Discordo totalmente"); o participante usa **o próprio dispositivo com a própria configuração** |
| **Impresso em letra grande** | Fonte sem serifa ≥ 18pt, alto contraste, uma frase por bloco, caixas grandes, papel fosco |
| **Lido em voz alta** | Leia cada frase **exatamente** como escrita, no mesmo ritmo para todos; repita a escala a cada item; anote e releia a resposta para confirmar |

- **Registre no relatório o formato usado por cada participante.**
- Leitura em voz alta aumenta a desejabilidade social: a pessoa responde para você.
  Se possível, quem lê não deve ser quem desenhou a tela.
- Se a sessão revelou barreiras de acessibilidade, o SUS dessa pessoa tende a
  refleti-las. Analise junto das observações, nunca isolado.

## Fontes

- **Lourenço, D. F.; Carmona, E. V.; Lopes, M. H. B. M.** Translation and
  Cross-Cultural Adaptation of the System Usability Scale to Brazilian Portuguese.
  *Aquichan*, v. 22, n. 2, e2228, 2022. DOI 10.5294/aqui.2022.22.2.8.
- **Brooke, J. (1996)** — SUS: a quick and dirty usability scale.
- **Sauro e Lewis** — média de referência 68; escala curva de notas.
- **Lewis e Sauro (2017)** — relatar o escore geral, não as subescalas.
- **Finstad (2006)** — "cumbersome" como termo problemático até no original.
- `references/metodos-de-avaliacao.md` §7; `assets/templates/sus-ptbr.md`;
  `scripts/sus_calculator.py`.
