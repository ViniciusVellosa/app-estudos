# Protocolo de teste de usabilidade — App de estudos personalizado por interesses

**Tipo:** moderado, presencial ou remoto, think-aloud concorrente · **Duração:**
45–60 min · **Participantes:** 5–8, incluindo **pelo menos 1 pessoa com baixa
visão** usando o próprio dispositivo e a própria tecnologia assistiva (ideal: 2–3)
· **Objetivo:** formativo (encontrar problemas), não somativo.
Fundamentação: `references/metodos-de-avaliacao.md` §6–§12.

**Equipe por sessão:** 1 moderador (conduz, não ajuda), 1 observador (anota na
folha de observação e cronometra). Se houver Wizard of Oz, 1 "mágico" que gera as
explicações sem ser visto.

---

## 0. Preparação (antes do dia)

- [ ] Ética resolvida com o professor (exercício de disciplina × TCC → CEP). TCLE pronto.
- [ ] Protótipo estável nas 5 tarefas; barreiras óbvias de acessibilidade já
      corrigidas (avaliação heurística + checklist de baixa visão).
- [ ] Piloto com 1 colega: tempo total, clareza das tarefas, gravação funcionando.
- [ ] Cartões de tarefa impressos (fonte ≥ 18 pt, alto contraste) **e** em arquivo
      digital acessível. Para quem usa leitor de tela, o moderador lê a tarefa.
- [ ] SEQ e SUS prontos no formato escolhido (`sus-ptbr.md`).
- [ ] Planilha de registro e códigos P01, P02…
- [ ] Explicações de referência do banco curado (se Wizard of Oz) para o universo
      informado pelo participante no recrutamento.

### Configuração de acessibilidade para participante com baixa visão
- Pergunte **no recrutamento** qual dispositivo e quais recursos usa (lupa do SO,
  zoom do navegador, ZoomText, fonte grande, tema escuro, alto contraste, leitor de
  tela, teclado ampliado, linha braille). Não presuma.
- Prefira que traga **o próprio dispositivo já configurado**. Se for usar o do
  laboratório, reserve 10 min para configurar com ele **antes** de gravar.
- Remoto: teste antes a ferramenta de vídeo com a TA (compartilhar tela com lupa
  ativa, áudio do leitor de tela na chamada). Ofereça chamada só de áudio, se preferir.
- Presencial: iluminação ajustável, sem reflexo na tela; ambiente silencioso se usa
  leitor de tela; cadeira e distância de tela livres.
- Combine pausas. Dê mais tempo por tarefa e **não** use o tempo dessa pessoa para
  comparar com os demais.
- Relate os achados desse participante como qualitativos, sem generalizar para
  "pessoas com baixa visão" (W3C WAI).

---

## 1. Roteiro do moderador

### 1.1 Boas-vindas (3 min)
> Oi, [nome]. Obrigado por vir. Eu sou [nome] e estou com [observador], que vai
> só anotar. Estamos testando um protótipo de app de estudos que explica conteúdos
> usando coisas de que você gosta. **Estamos testando o app, não você.** Se algo
> for difícil, é um problema do app, e é exatamente isso que queremos descobrir.
> Pode criticar à vontade: crítica sincera é o que mais nos ajuda.
>
> A sessão dura uns 50 minutos. Você pode pedir pausa ou parar a qualquer momento,
> sem precisar explicar.
>
> Antes de começar: precisa de algum ajuste? Letra maior, mais luz, que eu leia as
> tarefas em voz alta, pausas?

### 1.2 Consentimento (5 min)
> Este é o termo de consentimento. Ele explica o objetivo, o que vamos fazer,
> riscos, como guardamos seus dados e que você pode desistir quando quiser. Posso
> ler com você ou você prefere ler sozinho, no formato que for melhor?

Pontos a confirmar em voz alta:
- Autoriza **gravação de tela e áudio**? (Opcional: a sessão pode seguir só com notas.)
- Os dados são identificados só por código (P__); nome e gravação ficam guardados
  com acesso restrito e são descartados em [prazo].
- Se houver Wizard of Oz: o termo informa que "algumas respostas podem ser
  preparadas pela equipe"; o debrief explica tudo.
- Esclarecer dúvidas, colher o aceite (assinatura, digital ou registro em áudio)
  e entregar uma cópia.

### 1.3 Perfil rápido (3 min)
1. Curso e período.
2. Como você costuma estudar conteúdo técnico (vídeo, PDF, apps, IA)?
3. Interesses fora da faculdade e **quanto** conhece desse universo (fã casual ×
   conhece a fundo).
4. *(Opcional, a todos)* Usa algum ajuste de tela ou recurso para ler melhor?
5. Quanto você sabe hoje sobre TCP/IP? (1 = nada, 5 = domino)

### 1.4 Instruções de think-aloud (2 min)
> Enquanto usa o app, peço que **pense em voz alta**: diga o que está procurando,
> o que espera que aconteça, o que está achando estranho. Como se narrasse um jogo.
> Vou falar pouco; se você ficar em silêncio, posso perguntar "o que está pensando?".
> Eu não vou poder ajudar a fazer as tarefas, porque queremos ver como seria sem
> ninguém do lado. Se travar, pode dizer "desisto" e seguimos.

### 1.5 Tarefa de prática (2 min, não contabilizada)
> Para aquecer: abra o app e me diga, em voz alta, o que acha que dá para fazer
> nesta primeira tela.

Ajude o participante a se acostumar a falar. Corrija só o think-aloud, nunca o uso.

---

## 2. Tarefas

Leia cada tarefa em voz alta e entregue o cartão. Comece a cronometrar no "pode
começar". **Critério de sucesso definido antes.** Após cada tarefa, aplique o SEQ.

### T1 — Configurar interesses
> Você acabou de instalar o app. Configure-o para que as explicações usem **[o
> universo que você citou]** como referência.

- **Sucesso:** interesse salvo e visível no perfil, com nível de profundidade escolhido.
- **Parcial:** interesse salvo, sem nível de profundidade (se o protótipo pedir).
- **Observar:** encontra a configuração? Entende "profundidade"? Pedido redundante
  de dados (3.3.7)? Alvos e campos legíveis com ampliação?

### T2 — Pedir uma explicação de TCP/IP pelo seu interesse
> Você tem prova de redes semana que vem e não entendeu **TCP/IP**. Peça ao app
> uma explicação usando o seu interesse e leia até achar que entendeu.

- **Sucesso:** gera a explicação e chega à seção "onde a analogia quebra" (ou a
  menciona ao resumir).
- **Ao final, peça:** "Em uma frase, com suas palavras, o que o TCP faz?" (registrar
  literal; não é nota, é sinal de compreensão).
- **Observar:** percebe que a explicação foi gerada (status, anúncio para leitor de
  tela)? Lê a tabela de mapeamento? A analogia distrai (detalhe sedutor)? Rótulo
  "explicado com base em…" é notado (G11)?
- **Logo após o SEQ:** aplicar o questionário de carga de Leppink (10 itens, 0–10),
  se adotado.

### T3 — Mudar para a explicação neutra
> Agora você quer conferir a mesma explicação **sem a analogia**, só com os termos
> técnicos. Faça isso.

- **Sucesso:** chega à versão técnica do mesmo conteúdo sem perder o lugar.
- **Observar:** encontra o controle (signifier)? Entende o estado atual (ligado ou
  desligado)? Consegue voltar para a versão com analogia (H3)?

### T4 — Ajustar a leitura (texto maior e alto contraste)
> Você vai estudar à noite no ônibus e quer **letras maiores e mais contraste**.
> Deixe o app assim e volte à explicação.

- **Sucesso:** texto ampliado (configuração do app ou do sistema) **e** tema de alto
  contraste ativo, explicação legível sem rolagem horizontal.
- **Para participante com baixa visão:** pergunte antes "você costuma fazer isso
  pelo app ou pelo celular?" e aceite o caminho dele como sucesso. Observe se o app
  respeita o ajuste do sistema.
- **Observar:** layout quebra a 200–400%? Foco coberto por barra fixa? Tabela de
  mapeamento vira lista? Botões continuam alcançáveis?

### T5 — Avaliar a explicação
> Diga ao app se a explicação ajudou e **aponte algo** que estava errado ou confuso
> na analogia.

- **Sucesso:** envia avaliação **e** um comentário ou marcação específica ("a
  referência está errada" ou similar).
- **Observar:** encontra o feedback granular (G15)? Entende o que acontece depois
  (G16)? Confirmação aparece perto do botão?

*(Opcional, se houver tempo: T6 — "Desligue a personalização por completo".)*

### SEQ — após cada tarefa

> No geral, quão **difícil ou fácil** foi completar esta tarefa?
>
> 1 Muito difícil · 2 · 3 · 4 · 5 · 6 · 7 Muito fácil

Se a resposta for **menor que 5**: "O que tornou difícil?" (anotar literal).
Tradução da skill, não validada; mantenha a mesma redação para todos. Média
histórica do original ≈ 5,3–5,6 (MeasuringU).

---

## 3. Questionários finais (8 min)

1. **SUS** (`sus-ptbr.md`), no formato escolhido pelo participante.
2. *(Opcional)* Pós-teste de conhecimento **sem o app**: 3–5 questões de TCP/IP,
   incluindo **1 de transferência** fora do universo temático.

## 4. Debrief (5 min)

1. O que foi mais útil? E o mais irritante?
2. A analogia ajudou ou atrapalhou? Em que momento?
3. Você confiaria no app para estudar para a prova? Por quê?
4. Mudaria alguma coisa na forma como o app usa seus interesses (privacidade,
   tom, frequência)?
5. *(Participante com baixa visão)* Houve algo que te obrigou a mudar seu jeito
   habitual de usar a lupa / o leitor de tela?
6. Algo que não perguntei?

- **Wizard of Oz:** revele que parte das respostas foi preparada pela equipe,
  explique por quê e pergunte se o participante tem objeção ao uso dos dados.
- Agradecer, entregar ressarcimento combinado, explicar como receberá os resultados.

---

## 5. Métricas

| Métrica | Como coletar | Unidade | Resumo |
|---|---|---|---|
| Sucesso | Critério de cada tarefa | 1 / 0,5 / 0 | Taxa por tarefa (IC de Wilson) |
| Tempo | Do "pode começar" ao sucesso ou desistência | segundos | Média geométrica (excluir ou separar participantes com TA para comparação) |
| Erros | Ação que não leva ao objetivo | contagem + descrição | Por tarefa e tipo |
| Pedidos de ajuda | "Socorro!" / perguntas ao moderador | contagem | Por tarefa |
| SEQ | Após cada tarefa | 1–7 | Média por tarefa + motivos |
| Etiquetas MAC | Análise da gravação | etiqueta | Frequência por tarefa |
| Leppink | Após T2 | IL, EL, GL (0–10) | Média por fator |
| SUS | Final | 0–100 | Média, IC 95%, curva, n |
| Compreensão | Frase em T2; pós-teste | texto / acertos | Qualitativo / % |

---

## 6. Folha do observador (uma por participante)

**Participante:** P__ · **Data:** __/__/____ · **Formato:** presencial / remoto ·
**Dispositivo e TA:** ______________________ · **Universo e profundidade:** ________

| Tarefa | Início | Fim | Sucesso (1/0,5/0) | Erros | Ajuda | SEQ | Motivo se SEQ < 5 |
|---|---|---|---|---|---|---|---|
| T1 | | | | | | | |
| T2 | | | | | | | |
| T3 | | | | | | | |
| T4 | | | | | | | |
| T5 | | | | | | | |

**Registro de incidentes**

| Hora | Tarefa | O que aconteceu (comportamento observado) | Fala literal | Etiqueta MAC | Heurística / critério WCAG | Severidade (0–4) |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |

**Específico de acessibilidade (preencher se o participante usa TA)**
- [ ] Foco ou conteúdo novo ficou fora da área ampliada
- [ ] Rolagem horizontal a zoom alto
- [ ] Texto ou controle cortado / sobreposto
- [ ] Leitor de tela não anunciou a explicação gerada / estado do botão
- [ ] Tooltip/popover sumiu ou cobriu conteúdo
- [ ] Contraste insuficiente em algum tema
- Outro: ____________________

**Citações marcantes:** ___________________________________________

**Resumo do observador (3 linhas):** ______________________________

---

## 7. Depois das sessões

1. Transferir notas para a planilha consolidada; SUS para `sus-respostas.csv`
   (`id;q1;…;q10`) e rodar `scripts/sus_calculator.py`.
2. Etiquetar as gravações (MAC) e consolidar problemas com severidade.
3. Priorizar: severidade 3–4 e barreiras de acessibilidade primeiro.
4. Registrar em `melhorias.md`: problema → evidência → mudança → critério.
5. Descartar ou anonimizar gravações conforme o TCLE.
