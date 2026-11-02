# Questionário por WhatsApp — Etapa 1

| | |
|---|---|
| Como é aplicado | Duas mensagens de texto no WhatsApp. A pessoa responde na conversa |
| Itens | 12, sendo 1 aberta. As duas últimas são opcionais |
| Tempo de resposta | 3 a 4 min |
| n esperado | 13 a 25 (grupo + amigos, colegas e parentes universitários) |

---

## Como enviar — 3 regras que valem mais que o conteúdo

**1. Mande como texto, nunca como imagem ou print.** Texto no WhatsApp respeita o
tamanho de fonte que a pessoa configurou no celular e funciona com leitor de tela.
Um print do questionário quebra as duas coisas de uma vez — e seria contradição
num projeto sobre acessibilidade.

**2. Duas mensagens, nesta ordem.** Primeiro o convite (Mensagem 1), depois as
perguntas (Mensagem 2). Mandar tudo junto vira um bloco que ninguém lê no celular.

**3. Individual, não em grupo.** Em grupo, a primeira resposta ancora as
seguintes: as pessoas leem o que o colega respondeu e repetem. Além disso, expõe
as respostas de todos para todos.

---

## Mensagem 1 — convite e consentimento

> Oi! Tô fazendo um trabalho da disciplina de Interação Humano-Computador, na
> UNIARA. A gente tá projetando um app que explica matéria difícil usando coisas
> que a pessoa gosta (jogos, séries, futebol, etc.).
>
> Você responderia 12 perguntas rápidas? Leva uns 3 minutos, é tudo múltipla
> escolha, e não tem resposta certa ou errada.
>
> Sobre os seus dados: eu **não vou registrar seu nome nem seu número** junto das
> respostas — quando eu passar pra planilha, você vira só um código tipo R01. As
> respostas vão ser usadas só neste trabalho da faculdade, analisadas junto com as
> dos outros, e apago tudo até 09/11. Nada é publicado nem
> compartilhado.
>
> Pode pular qualquer pergunta. Se não quiser participar, só ignora, de boa. 🙂
>
> Qualquer dúvida é comigo: Vinicius G. Vellosa — vgvellosa@uniara.edu.br
>
> **Se você responder, considero que você concordou em participar e que tem 18 anos
> ou mais.**

> **Por que o texto não diz "anônimo":** no WhatsApp você vê quem está respondendo.
> A resposta não é anônima na coleta, só passa a ser **pseudonimizada** quando você
> transcreve. Prometer anonimato aqui seria promessa falsa, e é o tipo de detalhe
> que um professor de IHC nota. O texto acima diz exatamente o que acontece.

---

## Mensagem 2 — as perguntas

> Valeu! 🙏 Pode responder assim: **1-b, 2-c, 3-a…** (ou do jeito que for mais
> fácil pra você)
>
> **1.** Qual seu curso?
>
> **2.** Sua idade:
> a) 18–20  b) 21–24  c) 25–29  d) 30–39  e) 40+
>
> **3.** Onde você MAIS estuda?
> a) Celular  b) Notebook/PC  c) Tablet  d) Papel impresso
>
> **4.** O que você usa pra estudar? *(pode marcar várias)*
> a) Slide/PDF do professor  b) Livro  c) Vídeo  d) App de estudo
> e) IA (ChatGPT, Gemini, Claude…)  f) Anotação própria  g) Grupo de estudo
>
> **5.** Com que frequência você usa IA pra estudar?
> a) Nunca  b) Raramente  c) Algumas vezes por mês  d) Toda semana  e) Quase todo dia
>
> **6.** Pensa no último conteúdo que você custou a entender. O que mais atrapalhou?
> *(pode marcar até 2)*
> a) Muitos termos novos  b) Explicação abstrata, sem exemplo  c) Texto demais
> d) Falta de tempo  e) Material ruim de ler (letra pequena, PDF ruim)
> f) Não ver utilidade no conteúdo
>
> **7.** Cita UM jogo, série, time, banda ou obra que você gosta muito:
>
> **8.** Quanto você conhece desse universo? *(1 = sou fã casual, 5 = conheço a
> fundo, sei regras e detalhes)*
> 1 – 2 – 3 – 4 – 5
>
> **Agora 4 frases. Responde de 1 a 5:** *(1 = discordo totalmente,
> 5 = concordo totalmente)*
>
> **9.** Eu entendo melhor um conceito quando ele é comparado com algo que eu já conheço.
>
> **10.** Eu ficaria preocupado(a) se a comparação simplificasse demais o conteúdo.
>
> **11.** Eu gostaria de poder ver a mesma explicação SEM comparação, só com os
> termos técnicos.
>
> **12.** Se a comparação tivesse um erro sobre o universo que eu gosto, eu
> perderia a confiança no app.
>
> **Últimas duas, e são opcionais** (se não quiser responder, pula):
>
> **13.** Você usa algo pra ler melhor na tela? *(pode marcar várias)*
> a) Aumentar a letra do sistema  b) Zoom / lupa  c) Modo escuro
> d) Alto contraste  e) Leitor de tela ou leitura em voz alta  f) Não uso nada
>
> **14.** Ler texto longo na tela cansa você?
> a) Nunca  b) Às vezes  c) Frequentemente  d) Sempre

---

## Decisões de desenho, e por quê

**As opções são letras, não escalas visuais.** No WhatsApp a pessoa digita a
resposta, então ela precisa de rótulo curto e digitável. "1-b, 2-c" é o formato
mais rápido de responder com o polegar.

**Toda âncora de escala está escrita em texto** ("1 = discordo totalmente"), não
só o número solto. Quem lê com leitor de tela ou com a fonte grande não depende de
posição visual para entender a escala — é o mesmo princípio do critério
`1.3.3 Características sensoriais (A)` da WCAG, aplicado a texto de conversa.

**As perguntas 10 e 12 são negativas de propósito.** Reduzem o viés de
aquiescência, a tendência de concordar com tudo que é apresentado. **Na tabulação,
inverta as duas: 6 menos o valor**, antes de somar com as positivas. Esquecer isso
inverte o sentido do resultado.

**Não há pergunta sobre deficiência.** A versão anterior tinha, numa seção
opcional. Tirei de propósito: num formulário anônimo, perguntar isso é aceitável;
num WhatsApp, onde você sabe exatamente quem está respondendo, é pedir que um
amigo ou parente se declare para você. O projeto não precisa disso — a pergunta 13
pergunta **comportamento** ("você aumenta a letra?"), que é o que de fato alimenta
os requisitos de acessibilidade RA01, RA04 e RA20, sem exigir que ninguém revele
condição de saúde. Dado sobre deficiência é sensível pela LGPD (art. 11), e a
melhor proteção é não coletar.

**Doze perguntas, não dezoito.** No celular, em conversa, cada pergunta a mais
aumenta a chance de a pessoa parar no meio e responder "depois eu vejo".

---

## Tabular as respostas

1. Abrir uma planilha com uma linha por pessoa e uma coluna por pergunta.
2. Primeira coluna: **código** R01, R02, R03… **Não copie nome nem número de
   telefone para a planilha.** É o passo que cumpre o que você prometeu na
   Mensagem 1.
3. Transcrever as respostas da conversa para a linha da pessoa.
4. **Inverter as perguntas 10 e 12** (6 menos o valor).
5. Contar as frequências. **Reporte a contagem absoluta junto da porcentagem** —
   com n de 15, "60%" são 9 pessoas, e só a porcentagem soa a inflar o dado.
6. Separar as respostas da pergunta 7 (os universos citados) e qualquer comentário
   espontâneo que a pessoa mandar junto. Em WhatsApp as pessoas comentam fora da
   pergunta, e **esse comentário solto costuma ser o material mais útil**: é a
   frase citável que a proto-persona da Etapa 2 vai usar.

Se alguém responder em áudio, transcreva o conteúdo para a planilha e **apague o
áudio** — voz identifica a pessoa.

## Antes de mandar para a primeira pessoa

- [ ] Campos `[preencher]` resolvidos na Mensagem 1: seu nome, e-mail, data de descarte
- [ ] Mandou para **você mesmo** primeiro e leu no celular: nada cortado, numeração certa
- [ ] Testou aumentar a fonte do WhatsApp e reler — continua legível
- [ ] Vai enviar **individualmente**, não em grupo

## Fontes

- **Res. CNS 510/2016**, arts. 2º e 15 — o registro do consentimento pode ser
  escrito, sonoro, em imagem ou digital, desde que em linguagem clara; e art. 1º,
  parágrafo único, inciso VIII — atividade exclusivamente de ensino.
- **LGPD** (Lei 13.709/2018) — art. 11 (dado sensível sobre deficiência, razão de
  não perguntar), art. 18 (direito à eliminação, razão do contato na Mensagem 1).
- **WCAG 2.2** (W3C) — `1.3.3 Características sensoriais (A)`, princípio aplicado
  ao rotular as âncoras das escalas em texto.
- **Walkington e Bernacki** — profundidade do engajamento com o interesse
  (pergunta 8), base da diretriz DP06.
- Desenho de questionário: **(manual)** — livro-texto de métodos em IHC
  (Lazar, Feng e Hochheiser, *Research Methods in HCI*, 2ª ed., 2017,
  **a confirmar**).
