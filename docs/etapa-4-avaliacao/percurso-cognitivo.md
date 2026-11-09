# Percurso cognitivo com as personas — Etapa 4 (Avaliar)

| | |
|---|---|
| Método | **Percurso cognitivo** (*cognitive walkthrough*), avaliação analítica, sem usuários (Wharton et al., 1994) |
| Quem percorreu | Avaliação por especialista com apoio de IA (Claude, skill Lumen), a ser revisada pelos integrantes do grupo |
| Versão | commit `54c6a6d`, modo pré-gravado; as correções de severidade 3 (`avaliacao-heuristica.md`) já aplicadas |
| Personas | Ana (primária, baixa visão), Rafael (secundária, perfil da maioria) e Caio (cético, prefere linguagem técnica), de `../etapa-2-personas-cenarios/personas.docx` |
| Tarefas | T1 a T6, as mesmas do teste com usuários (`protocolo-teste.md`) |
| Evidências | `evidencias/` |

> **O que este documento é, e o que não é.** É uma **simulação** do raciocínio de
> cada persona, passo a passo, feita por quem conhece o sistema. Serve para achar
> onde o caminho certo não é óbvio. **Não é um teste com usuários**: nenhuma
> pessoa real usou o app nesta avaliação, e nada aqui deve ser lido como
> "a Ana conseguiu" no sentido empírico. As personas são modelos (Etapa 2), e a
> Ana, em particular, foi construída a partir da literatura, não de dados.

## Como ler

Em cada passo, as quatro perguntas do método:

1. **Objetivo:** a pessoa vai tentar fazer a coisa certa nesse ponto?
2. **Visibilidade:** ela vai perceber que a ação certa está disponível?
3. **Associação:** vai ligar a ação ao efeito que quer?
4. **Retorno:** depois de agir, vai perceber que avançou?

Legenda: ✅ sim · ⚠️ provavelmente, com hesitação · ❌ provavelmente não.

---

## T1 — Chegar à explicação

| Passo | Ana | Rafael | Caio | Observação |
|---|---|---|---|---|
| 1. Ler o consentimento e marcar "Li e concordo" | ✅ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | Texto curto, em lista. A nota de desenvolvimento que confundia foi retirada (P03) |
| 2. "Continuar" | ✅ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | O botão fica claro só depois de marcar; o estado é visível |
| 3. Escrever o assunto no chat | ✅ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | A pergunta do app é a instrução; o modelo de chat é conhecido (todos usam IA para estudar) |
| 4. Escrever o universo | ✅ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | ⚠️ ✅ ✅ ✅ | **Caio** não quer analogia; o app pede um universo mesmo assim (D2). Ele responde, mas a etapa reforça a desconfiança dele |
| 5. Ler a primeira parte | ✅ ✅ ✅ ⚠️ | ✅ ✅ ✅ ⚠️ | ✅ ✅ ✅ ⚠️ | **Retorno:** no modo pré-gravado, os universos das três personas (série de animação, jogo de tiro tático) **não têm analogia escrita**, e elas recebem a explicação padrão com um aviso. O valor central do app não aparece (P12) |

## T2 — Entender onde a comparação falha

| Passo | Ana | Rafael | Caio | Observação |
|---|---|---|---|---|
| 1. "Continuar" até a parte 4 | ✅ ✅ ✅ ⚠️ | ✅ ✅ ✅ ⚠️ | ✅ ✅ ✅ ⚠️ | O botão fica sempre no mesmo lugar (DD31). **Retorno:** quem enxerga não vê quantas partes faltam (P06); a Ana, com leitor de tela, ouve "parte 4 de 6" |
| 2. Ler "Onde a comparação não vale" | ✅ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | Título explícito. Para **Rafael**, que relatou cansaço com texto longo, uma parte por vez ajuda |

## T3 — Ver a versão técnica

| Passo | Ana | Rafael | Caio | Observação |
|---|---|---|---|---|
| 1. "Ver versão técnica" | ✅ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | Rótulo direto; o estado é dito em texto ("Voltar para a comparação") e no `aria-pressed` |
| 2. Continuar na versão técnica | ✅ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | Antes da correção P05, a parte seguinte voltava à analogia e o **Caio** teria de clicar a cada parte. Agora a escolha vale para as próximas |

## T4 — Ajustar a leitura

| Passo | Ana | Rafael | Caio | Observação |
|---|---|---|---|---|
| 1. Achar "Leitura e cores" | ⚠️ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | **Ana** provavelmente tenta primeiro o zoom do próprio celular (é o que ela usa em todo lugar), e o app funciona com ele: reflui sem rolagem lateral. O menu agora diz "cores" (P04) |
| 2. Escolher o tamanho e o tema; "Salvar preferências" | ✅ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | Opções com rótulos em texto, agrupadas em cartões |
| 3. "Voltar para a conversa" | ✅ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | A conversa continua onde estava |

## T5 — Avisar que a explicação está errada

| Passo | Ana | Rafael | Caio | Observação |
|---|---|---|---|---|
| 1. "Está errada" | ✅ ✅ ✅ ⚠️ | ✅ ✅ ✅ ⚠️ | ✅ ✅ ✅ ⚠️ | Visível na barra de ações. **Retorno:** "Obrigado, vamos conferir", mas a explicação continua na tela e o app não pergunta o que está errado (P02). **Caio** e **Rafael**, sensíveis a erro, tendem a querer dizer qual é o erro |

## T6 — Perguntar algo, inclusive fora do conteúdo

| Passo | Ana | Rafael | Caio | Observação |
|---|---|---|---|---|
| 1. Escrever uma pergunta no campo | ✅ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | O texto do campo diz "Pergunte sobre este conteúdo" |
| 2. Ler a recusa ("Fora deste conteúdo") | ✅ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | ✅ ✅ ✅ ✅ | Explica o motivo e oferece duas saídas |
| 3. "Continuar este conteúdo" | ✅ ✅ ⚠️ ⚠️ | ✅ ✅ ⚠️ ⚠️ | ✅ ✅ ⚠️ ⚠️ | O botão só leva o foco ao campo; não fica claro o que ele faz nem que algo aconteceu (P15) |

---

## Achados do percurso

| Achado | Personas | Liga a | Severidade |
|---|---|---|---|
| No modo pré-gravado, nenhuma das três personas recebe analogia: só existe a de futebol | todas | P12 | 2 no produto; **bloqueante para o teste com usuários** se não for tratado (preparar as explicações dos universos dos participantes ou usar a IA) |
| O app pede um universo mesmo a quem prefere a versão técnica | Caio | D2, RF08 adiado | 2 |
| Sem indicação visível de quantas partes faltam | Ana (sem leitor de tela), Rafael | P06, DD19 | 2 |
| "Está errada" não colhe o motivo nem diz o que acontece com a explicação | Rafael, Caio | P02 | 2 |
| "Continuar este conteúdo" não dá retorno | todas | P15 | 2 |
| A versão técnica voltava à analogia a cada parte | Caio | P05 | 3, **corrigido** |
| O menu de leitura não indicava as cores | Ana | P04 | 3, **corrigido** |

## Limites desta avaliação

- As respostas às quatro perguntas são **inferências** do avaliador sobre as
  personas, não observações. O percurso acha problemas de descoberta e de
  retorno; não diz se a analogia **ensina**, que é a pergunta central do projeto.
- A Ana usaria leitor de tela em textos longos. Os anúncios (`role="log"`,
  `aria-pressed`, região de status) estão implementados e passam na verificação
  automática, mas **não foram ouvidos com NVDA ou TalkBack** nesta avaliação
  (ver `auditoria-wcag.md`).
- Nenhuma conclusão sobre pessoas com baixa visão deve ser tirada daqui: "nada
  sobre nós sem nós". O passo seguinte é o teste com participantes reais,
  incluindo, se possível, uma pessoa com baixa visão.

## Fontes

- Wharton, C.; Rieman, J.; Lewis, C.; Polson, P. *The cognitive walkthrough
  method: a practitioner's guide*. In: Nielsen, J.; Mack, R. (orgs.). *Usability
  Inspection Methods*. New York: Wiley, 1994. p. 105–140.
- Personas e cenários: `../etapa-2-personas-cenarios/`.
- Biblioteca do Lumen: `references/metodos-de-avaliacao.md`.
