# SUS — System Usability Scale em português (Brasil)

**Versão usada:** tradução e adaptação transcultural de Lourenço, Carmona & Lopes
(2022), *Aquichan* 22(2):e2228, DOI 10.5294/aqui.2022.22.2.8 (α de Cronbach = 0,76;
n = 100 universitários). Original: Brooke (1996). Ver `references/metodos-de-avaliacao.md` §7.

**Quando aplicar:** ao final da sessão de teste, **depois** de todas as tarefas e
**antes** do debrief, para que a conversa não influencie as notas.

---

## Instruções ao participante

> Agora vou pedir que você avalie o aplicativo como um todo, pensando em tudo o
> que fez hoje. São 10 frases. Para cada uma, diga o quanto concorda, de **1
> (discordo totalmente)** a **5 (concordo totalmente)**. Não há resposta certa ou
> errada; responda pela primeira impressão. Se não tiver certeza, marque 3.

Em todas as frases, "sistema" = o aplicativo de estudos testado hoje.

| # | Afirmação | 1 Discordo totalmente | 2 | 3 | 4 | 5 Concordo totalmente |
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

### Notas sobre a redação
- **Item 7, inconsistência no artigo:** a Tabela 1 (versão de consenso) diz
  "…aprender a usar esse sistema **rapidamente**". O texto de Resultados diz "muito
  rapidamente", e o original em inglês é "very quickly". Este modelo usa a forma da
  Tabela 1. Escolha **uma** forma, use-a com todos os participantes e declare a
  escolha no relatório.
- **Âncoras:** o artigo informa a escala de 1 = discordo totalmente a 5 = concordo
  totalmente, mas a redação exata em português dos rótulos não aparece no texto lido
  (a confirmar). Rotule pelo menos os extremos.
- **Item 9:** use "segura/seguro" conforme o participante, ou "Eu me senti com muita
  segurança usando o sistema" (adaptação de gênero proposta pela skill, não validada;
  se usar, declare).
- **Item 8:** "muito pesado" foi a escolha dos tradutores para "cumbersome", palavra
  que já confundia não nativos no original (Finstad, 2006). Se um participante
  perguntar, explique de forma neutra: "pesado no sentido de trabalhoso, complicado
  de usar". Use a mesma explicação com todos.
- **Não troque a ordem, não inverta os itens negativos e não junte itens.** A
  alternância positivo/negativo faz parte do instrumento.

---

## Como pontuar

1. Itens **ímpares** (1, 3, 5, 7, 9): contribuição = resposta − 1.
2. Itens **pares** (2, 4, 6, 8, 10): contribuição = 5 − resposta.
3. Some as 10 contribuições (0 a 40) e **multiplique por 2,5** → escore de **0 a 100**.

```
SUS = 2,5 × [ (q1−1) + (5−q2) + (q3−1) + (5−q4) + (q5−1)
            + (5−q6) + (q7−1) + (5−q8) + (q9−1) + (5−q10) ]
```

**Exemplo:** respostas 4, 2, 4, 1, 4, 2, 5, 2, 4, 2 →
ímpares (3+3+3+4+3 = 16) + pares (3+4+3+3+3 = 16) = 32 × 2,5 = **80**.

**Interpretação (detalhes em `metodos-de-avaliacao.md` §7.3):**
- O escore **não é porcentagem**. Média de referência = **68** (percentil 50).
- Escala curva Sauro-Lewis: 68 ≈ C; 80,8–84,0 = A; ≥ 84,1 = A+.
- Reporte o **escore global** com média, IC 95%, nota na curva e n. Não use
  subescalas (Lewis & Sauro, 2017).
- Com 5–8 participantes, o IC é largo: o SUS é **indicador complementar**, não
  prova de usabilidade.
- **Respostas incoerentes:** se alguém marcar 5 no item 3 ("fácil") e 5 no item 2
  ("complexo"), pode ter se confundido com a alternância. Registre e comente; não
  "corrija" a resposta.

---

## Salvar as respostas para o script

Arquivo `4-avaliacao/sus-respostas.csv`, **separado por ponto e vírgula**, uma
linha por participante, com o código do participante (nunca o nome):

```csv
id;q1;q2;q3;q4;q5;q6;q7;q8;q9;q10
P01;4;2;4;1;4;2;5;2;4;2
P02;3;3;4;2;3;2;4;3;3;3
P03;5;1;5;1;4;1;5;1;5;1
```

- Valores inteiros de 1 a 5, sem espaços e sem células vazias. Se um item ficou
  sem resposta, não invente: deixe o participante fora do cálculo e relate.
- Salve em UTF-8. No Excel ou Google Planilhas: "Salvar como / Fazer download →
  CSV". Se o separador sair como vírgula, o script também aceita (ele detecta `,`,
  `;` ou tabulação).
- Rodar:
  ```
  python3 scripts/sus_calculator.py 4-avaliacao/sus-respostas.csv
  python3 scripts/sus_calculator.py 4-avaliacao/sus-respostas.csv --json
  ```
- O script mostra escore por participante, média, IC 95%, nota na curva e
  adjetivo aproximado. Ele também imprime subescalas: **não** as use como
  resultado principal.

---

## Aplicar a participantes com baixa visão

> As dicas abaixo são **inferência de boa prática**, derivadas dos princípios
> WCAG e da orientação do W3C sobre testes com usuários com deficiência. Não há
> fonte específica e verificada sobre aplicação do SUS a pessoas com baixa visão.

**Ofereça antes, sem presumir:** "Prefere responder no seu celular ou computador,
numa folha impressa em letra grande, ou que eu leia as frases e anote suas
respostas?"

| Formato | Como preparar |
|---|---|
| **Formulário digital** (Google Forms / Microsoft Forms) | Uma pergunta por item com 5 botões de opção (não use "grade de múltipla escolha", que é mais difícil com leitor de tela e com zoom); cada opção com texto completo ("1 – Discordo totalmente"…); teste antes com NVDA ou TalkBack e com zoom de 200%; o participante usa **o próprio dispositivo com a própria TA**; não use cor para indicar a escala |
| **Impresso em letra grande** | Fonte sem serifa ≥ 18 pt (ajuste à preferência do participante), alto contraste (preto sobre branco ou amarelo claro), uma frase por bloco, boa entrelinha, caixas de marcação grandes; papel fosco, sem brilho |
| **Lido em voz alta** | Leia cada frase **exatamente** como escrita, no mesmo ritmo para todos; tenha a escala impressa em letra grande na mesa ou diga "de 1, discordo totalmente, a 5, concordo totalmente" a cada item; o pesquisador anota e relê a resposta para confirmação |

- Registre no relatório o **formato de aplicação** de cada participante.
- Leitura em voz alta pode aumentar a desejabilidade social (o participante responde
  ao pesquisador). Quem leu deve ser alguém neutro, não o designer da tela, se possível.
- Dê tempo; não apresse. Permita pausas.
- Se a sessão mostrou barreiras de acessibilidade, o SUS desse participante tende a
  refleti-las. Analise junto com as observações, não isoladamente.

**Fonte:** Lourenço, D. F.; Carmona, E. V.; Lopes, M. H. B. M. Translation and
Cross-Cultural Adaptation of the System Usability Scale to Brazilian Portuguese.
*Aquichan*, v. 22, n. 2, e2228, 2022. DOI 10.5294/aqui.2022.22.2.8. Brooke, J.
(1996). Lewis & Sauro (2017, 2018). Ver `references/bibliografia.md` [70][72][77].
