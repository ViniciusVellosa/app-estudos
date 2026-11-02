# Acessibilidade digital — WCAG 2.2, normas brasileiras, baixa visão e tecnologias assistivas

Referência para o app de estudos personalizado por interesses. Estado em
**28/10/2026**. Os números [n] remetem a `bibliografia.md`.

**Marcadores de verificação**
- Sem marcador: conferido na fonte citada durante a pesquisa.
- **(a confirmar)**: texto normativo conhecido, ou dado de fonte secundária, que
  não foi reaberto na fonte primária (a página w3.org/TR/WCAG22 estava bloqueada).
  Antes de citar literalmente, confira no Understanding do W3C [10].
- **(inferência)**: aplicação ou conclusão de Lumen, não de uma fonte.

## Sumário
1. Panorama: o que vale em 2026
2. WCAG 2.2: status, POUR, novidades e remoções
3. Critérios para baixa visão (limiares exatos)
4. Critérios ligados à carga cognitiva
5. WCAG 3.0: status real
6. Documentos de apoio do W3C: COGA e Low Vision
7. Brasil: eMAG 3.1, ABNT NBR 17225:2025, LBI, Decreto 5.296
8. Tecnologias assistivas e recursos do sistema operacional
9. Ferramentas de teste e o limite da automação
10. Requisitos de acessibilidade recomendados para o app

---

## 1. Panorama: o que vale em 2026

| Documento | Status | Papel no projeto |
|---|---|---|
| **WCAG 2.2** | Recomendação W3C (05/10/2023) [7]; também **ISO/IEC 40500:2025** (21/10/2025) [8] | Requisito de conformidade: mirar **nível AA** |
| **ABNT NBR 17225:2025** | Norma brasileira, 1ª ed. 11/03/2025 [16] | Referência técnica nacional (= WCAG 2.2 A+AA, com extras) |
| **eMAG 3.1** | Abr/2014 [4]; anterior à WCAG 2.1 | Contexto histórico e governo federal |
| **LBI art. 63** | Lei 13.146/2015 [18] | Fundamento legal para sites de empresas no Brasil |
| **WCAG 3.0** | Working Draft [11][12] | Não usar como requisito |
| **COGA** (2021) e **Low Vision** (2016) | Notas e rascunhos informativos [14][15] | Fonte de necessidades de usuários e de padrões de design |

O W3C afirma que a WCAG 2 é o padrão atual, que a WCAG 3 não vai substituí-la
tão cedo e que a WCAG 2 só será descontinuada vários anos depois de a WCAG 3
ser finalizada. A recomendação é cumprir a WCAG 2.2 agora [9].

**Implicação para o app:** o critério de aceite de acessibilidade é **WCAG 2.2 AA**,
citado também como NBR 17225 (requisitos). Os critérios AAA mais úteis para baixa
visão entram como metas do projeto: 1.4.6, 2.4.13 e 2.5.5.

---

## 2. WCAG 2.2: status, POUR, novidades e remoções

### 2.1 Estrutura (conhecimento de manual, estável desde a WCAG 2.0)
- **Quatro princípios (POUR):** Perceptível, Operável, Compreensível, Robusto.
  Cada princípio tem diretrizes, e cada diretriz tem **critérios de sucesso**
  testáveis com nível **A, AA ou AAA** [10].
- A conformidade AA exige cumprir todos os critérios A e AA.
- Formato de citação adotado na skill: `1.4.10 Realinhar (AA)`. Nomes em
  português podem ser consultados no guia-wcag.com [3].

### 2.2 Os 9 critérios novos da WCAG 2.2 [7]

| Critério | Nível | Em uma linha |
|---|---|---|
| 2.4.11 Foco não obscurecido (mínimo) | AA | O componente com foco não pode ficar **totalmente** escondido por conteúdo do autor (header fixo, banner de cookies, chat) |
| 2.4.12 Foco não obscurecido (aprimorado) | AAA | **Nenhuma parte** do componente com foco fica escondida |
| 2.4.13 Aparência do foco | AAA | Indicador com área ≥ contorno de **2 CSS px** no perímetro e contraste **≥ 3:1** entre os estados com e sem foco |
| 2.5.7 Movimentos de arrastar | AA | Toda ação de arrastar tem alternativa de ponteiro único (clique/toque) |
| 2.5.8 Tamanho do alvo (mínimo) | AA | Alvo **≥ 24×24 CSS px** ou espaçamento equivalente (com exceções) |
| 3.2.6 Ajuda consistente | A | Mecanismos de ajuda na mesma ordem relativa em todas as páginas |
| 3.3.7 Entrada redundante | A | Não pedir de novo, no mesmo processo, dado já informado: preencher ou oferecer para seleção |
| 3.3.8 Autenticação acessível (mínimo) | AA | Nenhum teste de função cognitiva no login, salvo exceções |
| 3.3.9 Autenticação acessível (aprimorado) | AAA | Como 3.3.8, sem as exceções de reconhecimento de objetos e de conteúdo pessoal |

**3.3.8, exceções** [10, Understanding 3.3.8]: nenhum "cognitive function test
(such as remembering a password or solving a puzzle)" é exigido, a menos que
haja (a) **Alternativa**: outro método sem teste cognitivo; (b) **Mecanismo** de
apoio, como colar a senha ou usar gerenciador de senhas; (c) **Reconhecimento de
objetos**; (d) **Conteúdo pessoal** enviado pelo próprio usuário.

### 2.3 Removido
- **4.1.1 Parsing** "is obsolete and removed from WCAG 2.2" [7].

**Lacuna:** não foi verificado se houve errata editorial da WCAG 2.2 entre 2024
e 2026. A página "New in 2.2" mostra "Updated: 5 October 2023" [7].

---

## 3. Critérios para baixa visão (limiares exatos)

Vários limiares foram conferidos pela NBR 17225, que transcreve os critérios [16].

| Critério | Nível | Limiar / exigência | Verif. |
|---|---|---|---|
| 1.1.1 Conteúdo não textual | A | Alternativa em texto com o mesmo propósito; imagens decorativas ignoráveis por TA | (a confirmar) [10] |
| 1.3.3 Características sensoriais | A | Instruções não dependem só de forma, cor, tamanho, posição, orientação ou som | (a confirmar) [10] |
| 1.4.1 Uso de cor | A | Cor não é o único meio de transmitir informação ou distinguir elementos | (a confirmar) [10] |
| **1.4.3 Contraste (mínimo)** | AA | Texto **≥ 4,5:1**; texto grande (≥ 18 pt, ou ≥ 14 pt negrito ≈ **24 px / 18,66 px**) **≥ 3:1**. Exceções: incidental, decorativo, inativo, logotipo | NBR req. 5.11.3 [16] |
| **1.4.4 Redimensionar texto** | AA | Texto ampliável até **200%** sem TA e sem perda de conteúdo/função (exceto legendas e imagens de texto) | NBR req. 5.12.7 [16] |
| 1.4.6 Contraste (aprimorado) | AAA | Texto **≥ 7:1**; texto grande **≥ 4,5:1** | NBR rec. 5.11.2 [16] |
| (1.4.8 Apresentação visual) | AAA | Cores escolhidas pelo usuário, linha **≤ 80 caracteres**, sem justificação, entrelinha ≥ 1,5, parágrafos ≥ 1,5× a entrelinha, 200% sem rolagem horizontal | só ≤ 80 car. verificado (NBR req. 5.12.6) [16]; resto (a confirmar) |
| **1.4.10 Realinhar (Reflow)** | AA | Sem perda e sem rolagem em 2 dimensões a **320 CSS px** de largura (ou **256 CSS px** de altura para rolagem horizontal). Exceção: conteúdo que exige 2D (mapas, tabelas de dados, diagramas). "320 CSS pixels is equivalent to a starting viewport width of 1280 CSS pixels wide at 400% zoom" | [30] |
| **1.4.11 Contraste não textual** | AA | Componentes de UI (bordas de campo, estados) e gráficos necessários **≥ 3:1** contra as cores adjacentes | [10] (Understanding 1.4.11) |
| **1.4.12 Espaçamento de texto** | AA | Nada se perde com: altura de linha ≥ **1,5×** a fonte; espaço após parágrafo ≥ **2×**; letras ≥ **0,12×**; palavras ≥ **0,16×** | NBR req. 5.12.1–5.12.4 [16] |
| **1.4.13 Conteúdo em hover ou foco** | AA | Tooltip/popover **dispensável** (Esc, sem mover ponteiro/foco), **hoverable** (o ponteiro chega nele sem que suma) e **persistente** | (a confirmar) [10] |
| **2.4.7 Foco visível** | AA | Toda UI operável por teclado tem indicador de foco visível | NBR req. 5.1.1 [16] |
| **2.4.11 Foco não obscurecido (mín.)** | AA | Foco não fica totalmente oculto por conteúdo do autor | [7] |
| 2.4.13 Aparência do foco | AAA | Área ≥ perímetro × **2 CSS px**; contraste **≥ 3:1** entre os estados | NBR rec. 5.10.5 / 5.11.6 [16] |
| **2.5.8 Tamanho do alvo (mín.)** | AA | **≥ 24×24 CSS px**. Exceções: espaçamento (círculo de 24 px sem sobrepor outro alvo), equivalente que cumpre, inline em texto, controle do user agent, apresentação essencial/legal | limiar: NBR req. 5.8.7 [16]; exceções (a confirmar) [10] |
| (2.5.5 Tamanho do alvo, aprimorado) | AAA | **≥ 44×44 CSS px** | NBR rec. 5.8.6 [16] |
| 4.1.2 Nome, função, valor | A | Componentes expõem nome, função, estado e valor programaticamente; mudanças notificadas à TA | (a confirmar) [10] |

**Inferências de aplicação (Lumen):**
- **1.4.4 + 1.4.10 + 1.4.12 formam o "contrato de zoom"** da baixa visão: o layout
  sobrevive a 400% (largura 320 px) com espaçamento aumentado.
- **2.4.11 e 1.4.13 são críticos com lupa de tela.** O usuário vê só um recorte
  da tela, então um header sticky ou um banner cobre o foco, e um tooltip que
  some quando o ponteiro se move é ilegível.
- Texto com baixo contraste é a falha mais comum da web (83,9% das home pages
  em 2026) [27]. Por isso é o primeiro token a validar (`scripts/contrast_check.py`).

**Implicação para o app:** o painel "Explicação" (texto da analogia + tabela de
mapeamento) precisa ter coluna única a 320 px, tabela de mapeamento que vira lista
em telas estreitas (a exceção 2D do 1.4.10 não cobre uma tabela de duas colunas
que pode ser linearizada; inferência), botões "sem analogia", "trocar universo" e
"avaliar" com ≥ 24×24 px (meta: 44×44) e sem barra fixa cobrindo o foco.

---

## 4. Critérios ligados à carga cognitiva

| Critério | Nível | Exigência | Verif. |
|---|---|---|---|
| 2.2.1 Ajustável por tempo | A | Para todo limite de tempo: desligar, ajustar (até ≥ 10×) ou estender com aviso de ≥ 20 s e ação simples, repetível ≥ 10 vezes. Exceções: tempo real, essencial, > 20 h | (a confirmar) [10] |
| 2.2.2 Pausar, parar, ocultar | A | Conteúdo que se move, pisca ou rola automaticamente por > 5 s pode ser pausado, parado ou ocultado | (a confirmar) [10] |
| 2.2.6 Timeouts | AAA | Avisar quanto tempo de inatividade causa perda de dados (salvo se preservados > 20 h) | (a confirmar) [10] |
| 2.4.6 Cabeçalhos e rótulos | AA | Descrevem tópico ou propósito | (a confirmar) [10] |
| 2.5.7 Movimentos de arrastar | AA | Alternativa sem arrastar (ex.: exercícios "arraste a resposta") | [7] |
| 3.1.5 Nível de leitura | AAA | Texto acima do "lower secondary education" → conteúdo suplementar ou versão mais simples | (a confirmar) [10] |
| 3.2.6 Ajuda consistente | A | Ajuda na mesma ordem relativa entre páginas | [7] |
| 3.3.2 Rótulos ou instruções | A | Sempre que houver entrada de dados | (a confirmar) [10] |
| 3.3.7 Entrada redundante | A | Não pedir de novo dados já informados | [7] |
| 3.3.8 / 3.3.9 Autenticação acessível | AA / AAA | Ver 2.2 | [10] |

**Implicação para o app (inferência):**
- Login com colar senha, gerenciador de senhas, passkey ou link mágico; sem
  CAPTCHA de texto distorcido (3.3.8). A NBR 17225 trata CAPTCHA e reconhecimento
  facial no Anexo A [16].
- Quizzes e simulados: "modo sem cronômetro" ou extensão de tempo (2.2.1).
- Onboarding de interesses: não perguntar de novo o que já foi informado (3.3.7);
  ajuda sempre no mesmo lugar (3.2.6).
- Explicação "simples/literal" sempre disponível: atende 3.1.5 e a tensão com
  metáforas do COGA (seção 6).

---

## 5. WCAG 3.0: status real (out/2026)

- Continua **Working Draft**. Últimos rascunhos: WD de **03/03/2026** [11] e
  Explainer de **10/09/2026** [12]. Sem data de conclusão.
- O WD de março traz só requisitos com status "Developing" (escala: Placeholder →
  Exploratory → Developing → Refining → Mature). Divide-os em **Core** e
  **Supplemental**, usa "Applies when / Except when" e define *assertions*
  (declarações da organização sobre suas práticas, como fazer testes de
  usabilidade) [11].
- Explainer [12]: conformidade = cumprir **todos os Core Requirements**, que
  cobrem necessidades "semelhantes, mas não idênticas" às da WCAG 2.2 AA. Tags
  (Physical harm, Risk, Barrier, Friction) definem níveis abaixo da conformidade.
  **Bronze/Silver/Gold** ficam acima, com contagens "TBD". "WCAG 3 will not be
  published until it covers at least as much as WCAG 2.2."
- A Intro do W3C (25/09/2026) fala em "reporting tiers 1–6" e prevê conclusão
  "for a few more years" [9]. **Diverge da terminologia do Explainer**: o modelo
  está em fluxo.
- **APCA não está no rascunho.** Foi removida do WD de 24/07/2023. O Editor's
  Draft de 08/04/2026 diz "The contrast algorithm used in WCAG 3 is yet to be
  determined". Roselli estima que a WCAG 3 não sai antes de ~2030. O próprio
  autor da APCA (A. Somers, 15/04/2026) a chama de "draft guidance… not a final
  standard" [13]. O WD de março usa um "minimum contrast ratio test" para gráficos
  e foco e "text color adjustable" para texto [11].

**Implicação para o app:** use a razão de contraste da WCAG 2. A APCA serve no
máximo como heurística complementar de legibilidade (ex.: peso de fonte no tema
escuro), nunca como critério. Não apresente "Bronze/Silver/Gold" nem "APCA" como
fatos da WCAG 3.

---

## 6. Documentos de apoio do W3C: COGA e Low Vision

### 6.1 COGA — *Making Content Usable for People with Cognitive and Learning Disabilities* [14]
W3C Working Group Note de **29/04/2021**. Informativo: não é exigido para
conformidade e o W3C não pretende torná-lo Recomendação. **8 objetivos de design:**

| # | Objetivo | Padrões relevantes ao app |
|---|---|---|
| 1 | Ajudar a entender o que as coisas são e como usá-las | Propósito claro, design familiar e consistente, controles bem identificados, ícones que ajudam |
| 2 | Ajudar a encontrar o que precisam | Tarefas importantes fáceis de achar; **mídia em blocos (chunks)** (4.3.5); busca |
| 3 | Conteúdo claro e compreensível | Palavras claras (4.4.1), **linguagem literal (4.4.4)**, texto sucinto (4.4.5), resumos (4.4.8), uma instrução por vez (4.4.9), espaço em branco (4.4.10), alternativas para conceitos numéricos (4.4.13) |
| 4 | Evitar e corrigir erros | Nada se move inesperadamente, desfazer fácil, rótulos visíveis, evitar perda de dados e timeouts, feedback |
| 5 | Ajudar a manter o foco | Limitar interrupções (4.6.1), caminhos críticos curtos, evitar excesso de conteúdo (4.6.3) |
| 6 | Processos que não dependam de memória | Login sem memória, sem cálculos ou memorização |
| 7 | Ajuda e suporte | Ajuda humana, conteúdo alternativo para informação complexa, lembretes |
| 8 | Adaptação e personalização | Usuário controla o que se move (4.9.1), suporte à simplificação (4.9.3), interface personalizada e familiar |

**Tensão importante:** o padrão 4.4.4 (linguagem literal) pede para evitar
metáforas, e o app é baseado em analogias. Solução: personalização **opcional e
reversível**, explicação literal a um toque e tabela de mapeamento explícita (ver
`carga-cognitiva-e-personalizacao.md`).

### 6.2 *Accessibility Requirements for People with Low Vision* [15]
**First Public Working Draft de 17/03/2016**, nunca finalizado. É documento
**histórico ou de referência**. Ligá-lo à origem dos critérios 1.4.10, 1.4.12 e
1.4.13 da WCAG 2.1 é inferência; a página não diz isso.

| Seção | Necessidades |
|---|---|
| 3.1 Brilho e cor | Ajustar brilho (ofuscamento, dor); contraste suficiente **sem brilho excessivo**; não depender só de cor |
| 3.2 Rastreamento (tracking) | Rolagem em uma só direção; reflow em coluna única; comprimento de linha configurável; hifenização liga/desliga |
| 3.3 Percepção | Aumentar só o texto; escolher fonte; mudar sublinhado, itálico, negrito, caixa; escalar **todos** os elementos, inclusive cursor |
| 3.4 Espaçamento | Entrelinha, letras, palavras, justificação, margens; espaçamento que agrupa o que é relacionado |
| 3.5 Identificação de elementos | Títulos, listas e parágrafos com estilos distintos |
| 3.6 Ponto de atenção e proximidade | O trecho em leitura continua visível ao ampliar ou reformatar; rótulos, controles e **feedback próximos** ao foco |
| 3.7 Configurações do usuário | Tudo continua visível quando as configurações mudam; respeitar SO e navegador |

A **perda de campo visual** não tem seção própria; aparece de forma implícita em
"point of regard" e "proximity" [15].

**Implicação para o app (inferência):** feedback de erro e resultado **junto do
controle** (não num toast no canto), coluna única, nada fixo cobrindo a área
ampliada, respeito ao tema do SO e opção de **tema escuro de baixo brilho**
além do alto contraste (3.1: contraste sem brilho excessivo).

---

## 7. Brasil: eMAG 3.1, ABNT NBR 17225:2025, LBI, Decreto 5.296

### 7.1 eMAG 3.1 [4]
- Versão 3.1, **abril de 2014**. **6 seções**: Marcação, Comportamento (DOM),
  Conteúdo/Informação, Apresentação/Design, Multimídia e Formulário.
- **45 recomendações**, **sem níveis A/AA/AAA** ("não estão divididas por níveis
  de prioridade e sim por área").
- Exemplos de recomendações citadas em `materiais-da-disciplina.md`: contraste
  4,5:1 (rec. 4.1), cor não como único meio (4.2), redimensionamento a 200% (4.3),
  foco com borda ≥ 2 px (4.4).
- **Barra de acessibilidade** padronizada. A v3.1 **removeu** A+/A- da barra
  (a ampliação fica com o navegador), mas a própria página do eMAG ainda mostra
  esses controles (inconsistência observada). Primeira folha de **alto
  contraste** padronizada.
- **Atalhos (accesskey):** 1 = conteúdo, 2 = menu principal, 3 = busca. O
  "4 = rodapé" aparece em sites gov.br, mas **não foi confirmado** no texto do
  eMAG (a confirmar).
- Validador: **ASES**. Status de manutenção e versão atual: (a confirmar).
- **Lacuna:** não foi confirmado se o eMAG foi atualizado ou substituído pela NBR
  17225 no governo federal em 2025–2026.

### 7.2 ABNT NBR 17225:2025 — Acessibilidade digital para web [16][17]
- **1ª edição de 11/03/2025**, elaborada pelo ABNT/CB-040 (CE-040:000.004).
  Consulta pública de 27/11 a 26/12/2024. Lançada em evento da ABNT no escritório
  do Google em São Paulo, com apoio do MDHC [17].
- Escopo: sites, **baseada na WCAG 2.2**, para necessidades situacionais,
  temporárias ou permanentes, em especial de pessoas com deficiência.
- Estrutura: 1 Escopo; 2 Referências; 3 Termos (3.1–3.58); 4 Conformidade;
  **5 Diretrizes (16 tópicos, 5.1–5.16)**; 6 Material de apoio. **Anexo A**:
  itens problemáticos (**CAPTCHA, reconhecimento facial**). **Anexo B**:
  desempenho funcional (visão, audição, mobilidade, cognição). **Anexo C**:
  checklist.
- **146 itens = 96 requisitos + 50 recomendações.**

| Tipo | Corresponde a | Consequência |
|---|---|---|
| Requisito (96) | WCAG 2.2 **A + AA** | Obrigatório para conformidade regular |
| Recomendação (50) | **AAA** + boas práticas | Cumpri-las dá "conformidade plena"; as não atendidas exigem justificativa |

- Cada item indica o critério WCAG ("C.S.") e o nível. O guia-wcag.com mostra os
  códigos da NBR ao lado de cada critério [3].
- **Pontos mais exigentes que a WCAG AA** (inferência a partir da classificação):
  **não bloquear o zoom do navegador** (req. 5.13.5) e **linha ≤ 80 caracteres**
  (req. 5.12.6, que na WCAG é AAA via 1.4.8).
- Obrigatoriedade legal: normas ABNT são, em princípio, voluntárias; a Agência
  Gov não diz se a NBR 17225 é legalmente obrigatória [17].

### 7.3 LBI — Lei 13.146/2015, art. 63 (caput) [18][20]
> "É obrigatória a acessibilidade nos sítios da internet mantidos por empresas com
> sede ou representação comercial no País ou por órgãos de governo, para uso da
> pessoa com deficiência, garantindo-lhe acesso às informações disponíveis,
> conforme as melhores práticas e diretrizes de acessibilidade adotadas
> internacionalmente."

Os parágrafos (§1º símbolo de acessibilidade; §2º telecentros e lan houses) não
foram verificados na fonte oficial (a confirmar).

### 7.4 Decreto 5.296/2004, art. 47 [19][20]
Tornou obrigatória, em até 12 meses (prazo depois prorrogado por mais 12), a
acessibilidade nos portais da **administração pública** para pessoas com
deficiência visual. É marco **histórico**, citado por Bach et al. (2009) [2].

**Implicação para o app:** dever legal → LBI art. 63; referência técnica mais
defensável → NBR 17225 (requisitos), que equivale a WCAG 2.2 AA. Barra própria
com A+/A- e botão de contraste (herança do eMAG) é **complemento**; o essencial é
respeitar zoom do navegador e configurações do SO.

---

## 8. Tecnologias assistivas e recursos do sistema operacional

### 8.1 Quem usa o quê (visão geral)
Pessoas com baixa visão combinam **ampliação** (lupa do SO, ZoomText), **temas
de alto contraste / forced-colors**, **escala de texto do SO** e, em visão muito
baixa, **leitor de tela**, às vezes com braille. O hardware inclui teclados
ampliados e, para escrita braille, a máquina Perkins.

| Tecnologia | O que se sabe | Verif. |
|---|---|---|
| **NVDA 2026.1** | Lançado em 06/05/2026; gratuito para Windows; mínimo Windows 10 (11 recomendado); sem Windows 8.1, 32 bits ou Windows 10 ARM; vozes SAPI 5 de 64 bits. Há também 2026.1.1 (só título visto) | [21] |
| JAWS, VoiceOver (iOS/macOS), TalkBack (Android) | Leitores de tela de referência (conhecimento geral) | versões e recursos 2026 (a confirmar) |
| ZoomText, Lupa do Windows, Zoom do macOS, Ampliação do Android/iOS | Ampliadores (conhecimento geral; lupas costumam ir de 2× a 16×) | (a confirmar) |
| Linhas (displays) braille | Mostram em celas braille o texto do leitor de tela; a entrada usa a mesma lógica de 6 pontos da Perkins (conhecimento geral) | (a confirmar) |

### 8.2 Perkins Brailler [5]
- Máquina de escrever braille mecânica, inventada em **1951**. **US$ 810,00**,
  corpo de metal, ajuste de margens, garantia de 1 ano, **4,8 kg** (10,6 lb).
- **Campainha 7 espaços antes do fim da linha** (feedback sonoro no lugar do visual).
- Papel até 11,5 × 14 pol (29,2 × 35,6 cm), recomendado 90 lb.
- Pontos no padrão NLS: altura **0,5 mm**, diâmetro **1,4 mm**, entre pontos
  **2,3 mm**, entre celas **6 mm**, entre linhas **10 mm**.
- **Teclas:** a página **não** informa a contagem. O arranjo de 6 teclas de pontos
  + espaço, retrocesso e avanço de linha (9 teclas) é o layout padrão conhecido
  (conhecimento geral, a confirmar na página do fabricante).
- Lição de IHC: feedback multimodal, mapeamento direto tecla↔ponto, robustez.

### 8.3 Teclados ampliados de alto contraste / braille
- **Especificação de compra pública do TRT-9** [22]: "teclado padrão **ABNT2**,
  **USB** plug and play, teclas ampliadas em **alto contraste (amarelo/preto)**,
  com identificação em **braille**", compatível com Windows/Linux, garantia
  ≥ 12 meses. Valor de referência **R$ 210,00/unidade** (5 un. = R$ 1.050,00).
  **Não traz o tamanho da letra.**
- Exemplo importado (X9 Large Print Backlit) [23]: letras grandes em negrito (sem
  multiplicador informado), 107 teclas, retroiluminação em 7 cores e 4 níveis,
  USB-A com fio.
- O anúncio do Mercado Livre trazido pelo aluno [6] **não pôde ser lido**. Não
  afirme especificações típicas ("letras 4× maiores") nem preços de varejo.

### 8.4 Preferências do SO e media queries (a confirmar no MDN [24])
| Preferência | Como respeitar no código |
|---|---|
| Temas de contraste do Windows | `@media (forced-colors: active)`: usar cores do sistema; não depender de `background-image` para informação; manter bordas visíveis |
| Pedido de mais contraste | `@media (prefers-contrast: more)`: aplicar tema de alto contraste |
| Reduzir movimento | `@media (prefers-reduced-motion: reduce)`: desligar animações não essenciais |
| Tema escuro | `@media (prefers-color-scheme: dark)` |
| Tamanho de fonte do SO (Android "Tamanho da fonte", que desde o Android 14 chega a 200% com escala não linear; Dynamic Type no iOS) | Unidades relativas (`rem`), layout que reflui; nunca `user-scalable=no` |

Nenhum desses recursos foi verificado em fonte primária nesta pesquisa (a confirmar).

**Implicação para o app (inferência):** funcionar com teclado físico (usuários
de teclado ampliado), ordem de foco lógica, nomes acessíveis (4.1.2), foco de
alto contraste, conteúdo novo anunciado por `aria-live` sem mover o foco quando a
explicação é gerada (4.1.3 Mensagens de status, AA; nível de conhecimento geral),
e testes com ampliação real, não só com zoom do navegador.

---

## 9. Ferramentas de teste e o limite da automação

### 9.1 Números de cobertura
| Estudo | Método | Resultado |
|---|---|---|
| **GOV.UK (fev/2017)** [25] | Página com **143 barreiras** em 19 categorias; 10 ferramentas (Tenon, WAVE, HTML CodeSniffer, aXe, AChecker, SortSite, Google ADT, EIII, Asqatasun, Nu HTML Checker) | Melhor ferramenta (Asqatasun) ≈ 41%; Google ADT ≈ 17%; todas juntas ≈ 71%; **42 barreiras (29%) não detectadas por nenhuma** |
| **Deque (10/03/2021)** [26] | > 2.000 auditorias, > 13.000 páginas, ~300.000 problemas | **57% das ocorrências** cobertas pelo axe. Métrica por volume de ocorrências, não por critérios; estudo do próprio fornecedor |
| **WebAIM Million 2026** [27] (via fonte secundária) | Home pages do top 1 milhão | **95,9%** com falhas detectáveis (94,8% em 2025); **56,1 erros/página** (+10,1%) |

**Top 6 falhas do WebAIM Million 2026 (~96% dos erros detectados)** [27]:

| Falha | % das home pages |
|---|---|
| Texto com baixo contraste (média de 34 ocorrências/página) | 83,9% |
| Imagem sem alt | 53,1% |
| Campo de formulário sem rótulo | 51,0% |
| Link vazio | 46,3% |
| Botão vazio | 30,6% |
| Idioma do documento ausente | 13,5% |

### 9.2 Ferramentas
- Verificadas nas fontes: **ASES** (avaliador do governo, citado no eMAG) [4];
  **axe/axe-core** e **WAVE** [25][26].
- Não verificadas em 2026 (a confirmar): Lighthouse (usa subconjunto do
  axe-core), Accessibility Insights, WebAIM Contrast Checker, Colour Contrast
  Analyser, Accessibility Scanner (Android), Accessibility Inspector (Xcode).
- Na skill: `scripts/contrast_check.py` (1.4.3/1.4.6/1.4.11) e
  `npx @axe-core/cli <url>`.
- **guia-wcag.com** [3]: referência rápida da WCAG 2.2 em PT (também EN, ES, FR),
  versão 8.5.1, atualizado em 02/09/2026, com opção de ver os códigos da NBR 17225
  e link para checklist ABNT. Avisa que os cards não substituem a leitura dos
  critérios completos.

### 9.3 Teste em camadas (inferência sustentada por [25][26][29])
1. Automático no desenvolvimento ou CI (axe/Lighthouse): pega contraste, alt e
   rótulos, as falhas mais comuns.
2. Manual: só teclado (ordem, foco visível, sem armadilha), zoom 200% e 400%
   (viewport 320 px), espaçamento de texto, `forced-colors`.
3. Leitor de tela (NVDA, TalkBack ou VoiceOver) nos fluxos completos.
4. **Teste com pessoas com baixa visão**, que revela o que a checagem não pega
   e **não determina conformidade** sozinho [29]. Detalhes em
   `metodos-de-avaliacao.md`.

Mensagem para o relatório: segundo os estudos acima, pelo menos ~29% das
barreiras (GOV.UK) ou ~43% das ocorrências (Deque) ficam fora da automação.

---

## 10. Requisitos de acessibilidade recomendados para o app

Lista numerada para virar critério de aceite em `requisitos.md`. Nível-alvo:
**WCAG 2.2 AA / NBR 17225 (requisitos)**, mais metas AAA marcadas com ★.

| # | Requisito | Critério |
|---|---|---|
| RA01 | Texto normal com contraste ≥ 4,5:1 e texto grande ≥ 3:1 em **todos** os temas (claro, escuro, alto contraste); ★ meta 7:1 no texto das explicações | 1.4.3 (AA), ★1.4.6 (AAA) |
| RA02 | Bordas de campos, ícones de ação, estados (selecionado, erro) e o indicador de foco com ≥ 3:1 | 1.4.11 (AA) |
| RA03 | Interesse selecionado, resposta certa ou errada e campo obrigatório nunca indicados só por cor (ícone + texto) | 1.4.1 (A) |
| RA04 | Texto ampliável a 200% sem perda; zoom nunca bloqueado (sem `user-scalable=no` / `maximum-scale=1`); unidades em `rem` | 1.4.4 (AA); NBR req. 5.13.5 |
| RA05 | A 320 CSS px (1280 px a 400%) nenhuma rolagem horizontal; a tabela de mapeamento analogia↔conceito vira lista empilhada | 1.4.10 (AA) |
| RA06 | Nada se perde com entrelinha 1,5, parágrafo 2×, letras 0,12×, palavras 0,16× | 1.4.12 (AA) |
| RA07 | Blocos de explicação com no máximo 80 caracteres por linha, alinhados à esquerda | NBR req. 5.12.6; 1.4.8 (AAA) |
| RA08 | Glossários e dicas em popover: fecham com Esc, aceitam o ponteiro sobre eles e persistem; preferir abrir por clique | 1.4.13 (AA) |
| RA09 | Foco visível em todos os controles (contorno ≥ 2 px, ≥ 3:1) e nunca coberto por header ou rodapé fixo | 2.4.7, 2.4.11 (AA); ★2.4.13 |
| RA10 | Alvos ≥ 24×24 CSS px; ★ meta 44×44 nos botões "sem analogia", "trocar universo", "avaliar" e "próximo" | 2.5.8 (AA); ★2.5.5 |
| RA11 | Todas as funções operáveis por teclado, em ordem lógica; exercícios de arrastar com alternativa de clique | 2.1.1, 2.4.3 (A); 2.5.7 (AA) |
| RA12 | Estrutura semântica: `h1`–`h3` na explicação (Conceito → Analogia → Mapeamento → Onde a analogia falha → Versão técnica), landmarks, `lang="pt-BR"` | 1.3.1, 3.1.1 (A) |
| RA13 | Botões com nome acessível e estado (ex.: `aria-pressed` no "modo analogia"); explicação gerada anunciada por região `aria-live` sem roubar o foco | 4.1.2 (A); 4.1.3 (AA) |
| RA14 | Imagens ou diagramas das analogias com texto alternativo que descreve a relação, não só a cena | 1.1.1 (A) |
| RA15 | Instruções sem referência só a posição ou forma ("toque no botão roxo à direita") | 1.3.3 (A) |
| RA16 | Login sem teste cognitivo: colar senha, gerenciador, passkey ou link mágico; sem CAPTCHA visual | 3.3.8 (AA); NBR Anexo A |
| RA17 | Interesses informados no onboarding não são pedidos de novo; ajuda sempre na mesma posição | 3.3.7, 3.2.6 (A) |
| RA18 | Quizzes sem limite de tempo ou com tempo ajustável e extensível | 2.2.1 (A) |
| RA19 | Animações (ex.: personagens, transições) pausáveis e desligadas com `prefers-reduced-motion` | 2.2.2 (A); boa prática |
| RA20 | Respeita `forced-colors`, `prefers-contrast` e o tamanho de fonte do SO; oferece tema escuro de baixo brilho e tema de alto contraste | Low Vision 3.1/3.7 [15]; boa prática (a confirmar no MDN) |
| RA21 | Explicação literal/técnica ("sem analogia") sempre a um toque, com resumo no topo | COGA 4.4.4, 4.4.8 [14]; 3.1.5 (AAA) |
| RA22 | Feedback de erro e de resultado ao lado do controle que o originou | Low Vision 3.6 [15]; 3.3.1 (A) |
| RA23 | Explicações longas divididas em segmentos com progresso visível e ritmo controlado pelo aluno | COGA 4.3.5, 4.2.4 [14] |
| RA24 | Validação: axe sem erros críticos + checklist manual (`assets/templates/checklist-baixa-visao.md`) + sessão com ao menos 1 pessoa com baixa visão usando sua própria TA | [25][26][29] |

Nota: os critérios 1.3.1, 2.1.1, 2.4.3, 3.1.1, 3.3.1 e 4.1.3 não foram
levantados nas notas de pesquisa. Os números e níveis vêm de conhecimento de
manual da WCAG 2.x (a confirmar no Understanding [10] ou no guia-wcag.com [3]).

**Por que assim:** RA01–RA10 cobrem o núcleo de baixa visão da seção 3. RA11–RA15
garantem compatibilidade com leitor de tela para visão muito baixa. RA16–RA23
reduzem carga cognitiva, que pesa mais para quem lê com ampliação. RA24 reconhece
o limite da automação.
