# Protocolo do teste de usabilidade — Etapa 4 (Avaliar)

> **Atualizado em 09/11/2026 para a interface de chat** (decisões D3 e D7): o
> aluno escreve o assunto e o universo na conversa; há uma sexta tarefa (T6). Em
> 09/11 este teste **ainda não tinha sido aplicado** (ver `resultados.md`).

| | |
|---|---|
| Tipo | Moderado, think-aloud concorrente. Objetivo **formativo**: achar problemas, não provar que o app é bom |
| Duração | 30 a 40 min por sessão |
| Participantes | **3 a 5** — integrantes do grupo não contam como participantes (ver abaixo) |
| Equipe por sessão | 1 moderador (conduz, **não ajuda**) + 1 observador (anota e cronometra) |
| Gravação | Opcional. Sem gravar, o observador anota — e aí não é preciso termo assinado |

> **Quem não pode ser participante:** quem desenhou ou programou a tela. Você já
> sabe onde ficam os botões, então sua sessão não mede nada. No questionário da
> Etapa 1 o grupo respondeu como público-alvo, o que era aceitável com o rótulo de
> proto-persona; aqui não funciona, porque o que se mede é **descoberta**. Use
> colegas de outra turma, amigos, parentes universitários — alguém que nunca viu o
> app.

> **Quantos bastam.** Com 3 a 5 participantes você encontra a maior parte dos
> problemas graves. O que **não** dá para fazer com esse n é afirmar número: nada
> de "80% dos usuários conseguiram". Relate contagem absoluta: "4 de 5
> concluíram T3".

---

## 0. Antes do dia

- [ ] App rodando e estável nas seis tarefas (`docker compose up --wait`, ou
      `uv run uvicorn` + `npm run dev`)
- [ ] **Avaliação heurística feita e os problemas de severidade 3 e 4 corrigidos.**
      Esta ordem não é burocracia: é desperdício gastar a sessão de um participante
      com um problema que o grupo acharia sozinho em 20 minutos
      (`avaliacao-heuristica.md`)
- [ ] Auditoria WCAG conferida (`auditoria-wcag.md`) — o automatizado já roda no CI
- [ ] Piloto com 1 pessoa: mede o tempo total e revela tarefa mal redigida. O
      piloto **não entra** nos resultados
- [ ] Cartões de tarefa impressos em fonte ≥ 18pt e alto contraste, **e** em
      arquivo digital
- [ ] Planilha de registro aberta, com códigos P1, P2…
- [ ] SUS pronto no formato escolhido (`sus.md`)
- [ ] **Analogias prontas para o universo de cada participante.** No modo
      pré-gravado só existe a de futebol; os outros universos recebem a
      explicação padrão e a tarefa T2 perde o sentido (percurso cognitivo, P12).
      Pergunte o universo no convite e escreva a explicação antes, no formato de
      `apps/api/content/explanations/tcp-entrega-confiavel/futebol.json`, ou use
      a IA com cota suficiente para as sessões

### Se algum participante usa ampliação ou leitor de tela

- Pergunte **no convite** qual dispositivo e quais recursos usa. Não presuma.
- Peça que traga **o próprio dispositivo, já configurado**. O que você quer saber é
  se o app funciona no ambiente real dele, não num ambiente que você preparou.
- Dê mais tempo e **não compare o tempo dele com o dos outros**.
- Relate os achados dele como **qualitativos**, sem generalizar para "pessoas com
  baixa visão" — é um participante, não uma amostra.

---

## 1. Roteiro do moderador

### 1.1 Boas-vindas (3 min)

> "Oi, [nome]. Obrigado por topar. Eu sou [nome] e o [nome] vai só anotar.
>
> A gente fez um app que explica matéria difícil usando coisas de que a pessoa
> gosta — jogo, série, futebol. Vou pedir que você faça algumas coisas nele.
>
> **O que está sendo testado é o app, não você.** Se algo ficar difícil, o problema
> é do app, e descobrir isso é exatamente o que eu preciso. Pode criticar sem
> medo — crítica sincera é o que mais ajuda. Elogio não conserta nada.
>
> Leva uns 35 minutos. Pode pedir pausa ou parar quando quiser, sem explicar.
>
> Antes de começar: precisa de algum ajuste? Letra maior, mais luz, que eu leia as
> tarefas em voz alta?"

- [ ] Perguntar o ajuste a **todos**, sem presumir
- [ ] Se for gravar, pedir autorização **agora** e aceitar um "não" sem insistir

### 1.2 Perfil rápido (3 min)

1. Curso e período.
2. Como você costuma estudar conteúdo técnico?
3. Um universo de que você gosta muito — e quanto você conhece dele, de 1 a 5.
   *(Anote: a explicação do app vai usar isso)*
4. *(A todos)* Usa algum ajuste de tela para ler melhor?
5. Quanto você sabe de TCP hoje, de 1 a 5? *(1 = nada, 5 = domino)*

> A pergunta 5 importa na análise: analogia ajuda quem sabe pouco e pode estorvar
> quem já domina (reversão de expertise). Se um participante der 5 e reclamar da
> analogia, isso **não** é um defeito do app — é o efeito esperado, e é argumento
> para o *fading* de DP08.

### 1.3 Think-aloud (2 min)

> "Enquanto usa, **pensa em voz alta**: diz o que está procurando, o que espera que
> aconteça, o que achou estranho. Como se narrasse um jogo.
>
> Eu vou falar pouco. Se você ficar quieto, eu pergunto 'o que você está pensando?'.
> E eu **não vou poder ajudar** nas tarefas, porque quero ver como seria sem
> ninguém do lado. Se travar de vez, diz 'desisto' e a gente segue — desistir é um
> resultado válido, não é falha sua."

### 1.4 Aquecimento (2 min, não contabilizado)

> "Pra começar: abre o app e me diz, em voz alta, o que você acha que dá pra fazer
> nessa primeira tela."

Serve para a pessoa se acostumar a falar. Corrija o think-aloud se ela ficar
calada; **nunca** corrija o uso.

---

## 2. As seis tarefas

Leia a tarefa em voz alta, entregue o cartão, comece a cronometrar no "pode
começar". As tarefas vêm de `../etapa-2-personas-cenarios/cenarios.docx`.

> **O texto lido não menciona nome de botão.** Dizer "clique em ver sem comparação"
> entrega a resposta e destrói a medida — o que T3 mede é se a pessoa **acha**
> aquilo sozinha.

### T1 — Chegar à explicação

> "Você quer estudar um assunto de redes. Começa a usar o app até chegar na
> explicação de um conceito."

- **Sucesso:** chega à explicação sem ajuda, tendo passado pelo consentimento e
  escrito no chat o assunto e o universo.
- **Parcial:** chega, mas precisa de uma dica.
- **Observar:** entende o que o consentimento pede? Trava em algum passo? Os campos
  são legíveis? → RF01, RF02

### T2 — Entender onde a comparação falha

> "Lê a explicação até o fim e me diz, com suas palavras, onde a comparação deixa
> de valer."

- **Sucesso:** localiza o passo "onde a comparação falha" e explica com palavras
  próprias.
- **Ao final, pergunte:** "em uma frase, o que o TCP faz?" — anote **literal**. Não
  é nota; é sinal de que a explicação funcionou.
- **Observar:** percebe que a explicação foi gerada? Lê a tabela de mapeamento ou
  pula? A analogia distrai mais do que ensina? → DP01, DP02

### T3 — Achar a versão técnica

> "Agora você quer ver esse mesmo conteúdo sem nenhuma comparação, só nos termos
> técnicos."

- **Sucesso:** encontra e usa a versão técnica em menos de 30 segundos.
- **Observar:** procura onde? O rótulo do botão comunica? → RF04, RA21, DP05

### T4 — Ajustar a leitura

> "Essa tela está difícil de ler pra você. Ajusta o app pra ficar mais confortável."

- **Sucesso:** encontra e aplica texto ampliado ou alto contraste.
- **Observar:** procura no app ou no sistema? Acha o controle? O ajuste persiste ao
  navegar? → RF06, RA01, RA04
- **Com participante que usa ampliação:** peça que use **a própria configuração**.

### T5 — Reportar um erro

> "Você percebeu que a explicação tem um erro. Avisa o app."

- **Sucesso:** encontra o caminho de reportar.
- **Observar:** espera que isso exista? Confia que serve pra algo? → RF05, DP10

### T6 — Tirar uma dúvida

> "Você ficou com uma dúvida sobre o conteúdo. Pergunta pro app. Depois,
> pergunta algo que não tem nada a ver com a matéria."

- **Sucesso:** faz a pergunta pelo campo do chat e, diante da recusa, encontra
  uma saída ("Continuar este conteúdo" ou "Estudar outro conteúdo").
- **Observar:** entende por que o app recusou? Fica frustrado ou acha razoável?
  → RF11, D5

### SEQ — depois de **cada** tarefa

Uma pergunta, imediatamente, antes de passar à seguinte:

> "No geral, quão fácil ou difícil foi fazer isso? De 1, muito difícil, a 7, muito
> fácil."

Anote o número **e** o que a pessoa disser junto. O comentário vale mais que o número.

---

## 3. Fechamento

1. **SUS** — aplicar agora, **depois de todas as tarefas e antes da conversa
   final**, para que o debrief não contamine as notas (`sus.md`).
2. **Debrief** (5 min):
   - O que foi mais confuso?
   - Você usaria isso antes de uma prova? Por quê?
   - A comparação com [universo dele] ajudou ou atrapalhou?
   - Tem algo que eu não perguntei?
3. Agradecer e explicar o que acontece com as anotações.

---

## 4. Folha de registro (uma por participante)

```
Participante: P__        Data: ___/___/___      Moderador: ______
Dispositivo: ____________   Usa ajuste de leitura: ____________
Conhecimento prévio de TCP (1-5): ___   Universo informado: ___________

| Tarefa | Sucesso (S/P/N) | Tempo | Erros | SEQ (1-7) | Observação |
|--------|-----------------|-------|-------|-----------|------------|
| T1     |                 |       |       |           |            |
| T2     |                 |       |       |           |            |
| T3     |                 |       |       |           |            |
| T4     |                 |       |       |           |            |
| T5     |                 |       |       |           |            |
| T6     |                 |       |       |           |            |

Frase do T2 ("o que o TCP faz?"), literal:
_________________________________________________

Citações marcantes (literais):
_________________________________________________

SUS: ___   Formato de aplicação: ___________
```

Salve como `dados/P1-registro.md`. **Sem nome** — só o código.

---

## 5. Como analisar (e o que não afirmar)

| Medida | Como relatar |
|---|---|
| Sucesso por tarefa | Contagem absoluta: "4 de 5 concluíram T3". **Nunca** só porcentagem com n = 5 |
| Tempo | Mediana, e só como contexto. Com 5 pessoas, tempo varia demais para comparar |
| SEQ | Por tarefa, junto do comentário. Tarefa com SEQ baixo é onde o protótipo precisa mudar |
| SUS | Escore global, média e n. Sem subescalas (`sus.md`) |
| Problemas | Lista priorizada por severidade, cada um ligado a uma heurística ou critério WCAG |

**Declare:** objetivo formativo, n pequeno, amostra de conveniência, e que achados
de participante com tecnologia assistiva são qualitativos.

**Rastreabilidade — o fecho do projeto:**

```
problema observado → heurística ou critério WCAG → mudança no protótipo
```

Isso vai para `melhorias.md`. É o que mostra que a avaliação **mudou** o projeto, e
não foi um ritual no fim do relatório.

## Fontes

- **Nielsen** — teste formativo, severidade, avaliação heurística antes do teste
  com usuários.
- **Think-aloud concorrente** e a regra de o moderador não ajudar
  (`references/metodos-de-avaliacao.md` §6).
- **SEQ** (Single Ease Question), 7 pontos, aplicada após cada tarefa.
- **W3C WAI** — achados de participantes com deficiência relatados como
  qualitativos, sem generalização.
- **Reversão de expertise** — base da pergunta 5 do perfil e de DP08.
- `references/metodos-de-avaliacao.md` §6 e §12;
  `assets/templates/protocolo-teste-usabilidade.md`.
