# Cenários — Etapa 2 (Define)

Design baseado em cenários (Rosson e Carroll): primeiro o **cenário-problema**,
que descreve a situação atual **sem** a solução; depois o **cenário de
atividade/interação**, que mostra a mesma situação com o app. Cada um fecha com
**claims**: as vantagens (+) e os riscos (−) da decisão de design.

> O cenário-problema é o que prova que o projeto resolve algo real. Escrevê-lo
> depois da solução é a inversão mais comum em trabalho de disciplina — e dá para
> notar, porque o problema sai suspeitosamente moldado à solução.

> Rótulos de origem: `[questionário: pergunta N]` · `[hipótese da equipe]` ·
> `[da literatura]`

---

## Cenário 1 — Ana (baixa visão)

### 1.1 Cenário-problema (como é hoje)

> **Ator:** Ana, 21 anos, baixa visão `[da literatura: W3C WAI, Elias; GOV.UK,
> Ashleigh]`
>
> São 22h de domingo. A prova de Redes é quarta. Ana abre no celular o PDF dos
> slides que o professor postou e precisa entender entrega confiável no TCP.
>
> Ela amplia para conseguir ler. O PDF não reflui: cada aumento de zoom obriga a
> arrastar a página para os lados para completar uma linha. Ela lê três palavras,
> arrasta, lê mais três, e no fim da linha já não lembra o começo da frase. O
> diagrama de sequência, que explicaria tudo, é uma imagem — ampliada, vira um
> borrão de setas.
>
> Depois de vinte minutos ela leu um slide e meio. Fecha o PDF e abre o vídeo de
> alguém explicando, mas o vídeo tem 47 minutos e ela não sabe em que trecho está
> o assunto. Vai dormir achando que o problema é ela ser lenta.

**O que esse cenário diz sobre o projeto:** a barreira não é a falta de analogia.
É o **formato do material**. Vale registrar — contraria a intuição de que a
personalização é o diferencial principal.

### 1.2 Cenário de atividade/interação (como será)

1. Ana abre o app no celular. A fonte respeita o tamanho que ela já configurou no
   sistema, e o tema está no alto contraste que ela escolheu na primeira visita.
2. Ela escolhe o conceito "entrega confiável no TCP".
3. O app mostra a explicação em **passos curtos**, um por tela, com progresso
   visível: conceito → cena do universo dela → quem é quem → onde a comparação
   falha → versão técnica → uma pergunta para testar.
4. O universo é `[questionário: pergunta 7]`, que ela informou no início, no nível
   que ela declarou `[questionário: pergunta 8]`.
5. Em qualquer passo, um botão **"ver sem comparação"** troca para a versão técnica
   literal, sem recarregar a página e sem perder o lugar.
6. O texto reflui: a 320px de largura, nada rola para o lado. A tabela que mapeia
   analogia↔conceito vira lista empilhada.
7. Quando a explicação termina de carregar, uma região viva anuncia "Explicação
   pronta" — sem roubar o foco de onde Ana estava.
8. Se a comparação não fizer sentido, ela toca em "trocar universo" ou avisa que
   está errada.

**Claims**

| | Afirmação |
|---|---|
| (+) | Texto que reflui resolve a barreira central do cenário-problema `[da literatura: 1.4.10]` |
| (+) | Segmentar em passos curtos permite parar e retomar — essencial num contexto de interrupção e de leitura que cansa `[da literatura: COGA, RA23]` |
| (+) | A analogia dá estrutura conhecida para pendurar o conceito novo, reduzindo o que precisa ser mantido na memória de trabalho de uma vez |
| (−) | Se a analogia vier como **imagem** ou tabela larga, o app reproduz exatamente a barreira do PDF. Mitigação: DP02 corta elemento decorativo; a tabela empilha |
| (−) | Tom infantilizado afasta quem já luta para ser levado a sério. Mitigação: DP18 |
| (−) | Um passo por tela aumenta o número de toques. Para quem navega com ampliação, cada toque custa. Mitigação: progresso visível e navegação por teclado (RA11) |

---

## Cenário 2 — Rafa (sem deficiência, sem tempo)

### 2.1 Cenário-problema (como é hoje)

> **Ator:** Rafa, `[questionário: perguntas 1 e 2]`
>
> `[Escreva a narrativa a partir da pergunta 6 — a opção mais marcada é o núcleo do
> problema. Mantenha no presente, sem mencionar o app, e use um detalhe concreto de
> alguma resposta real. Se a opção mais marcada for "explicação abstrata, sem
> exemplo", o cenário é sobre ler a definição três vezes e continuar sem saber o
> que ela significa na prática.]`
>
> `[Se a pergunta 5 mostrar uso frequente de IA, inclua isso: ele já pede ao
> ChatGPT, recebe uma resposta que parece boa, e não tem como saber se está certa.
> Esse é o cenário-problema mais forte que seus dados podem dar, porque é o
> concorrente real do app.]`

### 2.2 Cenário de atividade/interação (como será)

1. `[preencher: o caminho dele é o mesmo de Ana, mas o que ele valoriza é outro —
   velocidade e confiança no conteúdo, não reflow]`
2. …

**Claims**

| | Afirmação |
|---|---|
| (+) | Conteúdo vindo de texto-base revisado dá o que a IA genérica não dá: a garantia de que a afirmação técnica foi conferida (DP12, RNF04) |
| (+) | `[preencher a partir da pergunta 9]` |
| (−) | `[se a pergunta 12 tiver média alta]` Um único erro sobre o universo dele derruba a confiança no app inteiro. Mitigação: validador anti-alucinação, explicação padrão como reserva e o aviso de erro (RF05, DP10) |
| (−) | `[se a pergunta 11 tiver média alta]` Personalizar pode ser visto como enfeite que atrasa. Mitigação: a versão técnica a um toque (RF04, DP05) |

---

## Cenário 3 — o cético (só se os dados pedirem)

Se o questionário revelar alguém com pergunta 9 baixa e pergunta 10 ou 12 alta,
escreva o cenário dele. É o mais útil dos três: descreve a pessoa que acha que a
analogia vai simplificar demais e atrapalhar.

`[Se ninguém no questionário tiver esse perfil, não invente. Registre que não
apareceu — isso em si é um achado, e provavelmente reflete que o grupo respondeu o
próprio questionário.]`

---

## Tarefas derivadas para o teste de usabilidade (Etapa 4)

Preencher agora economiza a Etapa 4: o protocolo do teste pede exatamente isto.
O texto da coluna do meio é **lido em voz alta ao participante** — por isso não
menciona nome de botão, que seria entregar a resposta.

| ID | Tarefa (texto lido ao participante) | Critério de sucesso | Vem de |
|---|---|---|---|
| **T1** | "Você quer estudar um assunto de redes. Comece a usar o app até chegar na explicação de um conceito." | Chega à explicação sem ajuda, tendo passado pelo consentimento e informado um interesse | Cenário 1, passos 1–3; RF01, RF02 |
| **T2** | "Leia a explicação até o fim e me diga, com suas palavras, onde a comparação deixa de valer." | Localiza e compreende o passo "onde a comparação falha" | Cenário 1, passo 3; DP01 |
| **T3** | "Agora você quer ver esse mesmo conteúdo sem nenhuma comparação, só nos termos técnicos." | Encontra e usa a versão técnica em menos de 30s | Cenário 1, passo 5; RF04, RA21 |
| **T4** | "Essa tela está difícil de ler para você. Ajuste o app para ficar mais confortável." | Encontra e aplica texto ampliado ou alto contraste | Cenário 1, passo 1; RF06, RA01, RA04 |
| **T5** | "Você percebeu que a explicação tem um erro. Avise o app." | Encontra o caminho de reportar erro | Cenário 2, claim (−); RF05, DP10 |

**Métricas por tarefa (Etapa 4):** sucesso (sim/parcial/não), tempo, número de
erros, e **SEQ** — uma pergunta de facilidade logo após cada tarefa. SUS só no
final, uma vez.

**T4 com participante que usa tecnologia assistiva:** peça que use **a própria
configuração** (o zoom, a fonte, o leitor de tela que ele já usa), não a que você
preparou. O que você quer saber é se o app funciona no ambiente real dele.

---

## Checklist antes de fechar

- [ ] Cenário-problema escrito **antes** de olhar para a solução, no presente, sem
      citar o app
- [ ] Cada cenário tem claims com **pelo menos um (−)** — cenário sem risco é
      propaganda, não análise
- [ ] Cada claim (−) tem mitigação apontando para um requisito RA ou DP
- [ ] T1 a T5 revisadas: o texto lido não entrega o nome do botão
- [ ] Cada tarefa aponta para um cenário e para um requisito

## Fontes

- **Rosson e Carroll (2002)** — design baseado em cenários: cenário-problema,
  de atividade, de informação e de interação; análise de claims
  (conhecimento de manual da obra, **a confirmar**).
- **Benyon** — PACT, em `pact.md`.
- **W3C WAI, Stories of Web Users** e **GOV.UK accessibility personas (2019)** —
  base da persona Ana; o GOV.UK ressalva que **não substituem teste com usuários
  reais**.
- **WCAG 2.2** (W3C) — `1.4.10 Realinhar (AA)` e demais critérios via RA.
- **COGA** (W3C) — segmentação e ritmo controlado pelo usuário (RA23, DP13).
- `references/processo-de-design.md` §4.2; `assets/templates/cenario-pact.md`.
