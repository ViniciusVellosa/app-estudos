# Processo de design — pesquisa, personas, cenários, protótipos e requisitos

Referência para as etapas 1 a 3 (Entender → Desenhar) do app de estudos
personalizado por interesses, com foco em inclusão de pessoas com baixa visão.
Estado em **28/10/2026**. Os números [n] remetem a `bibliografia.md`.

**Marcadores:** **(a confirmar)** = conhecimento de manual ou dado não conferido
na fonte; **(fonte secundária)** = resumo, espelho ou matéria; **(manual)** =
orientação de livro-texto de IHC, rotulada assim porque as notas não trouxeram
fonte verificada; **(inferência)** = aplicação de Lumen.

## Sumário
1. Modelos de processo
2. Pesquisa com usuários
3. Personas
4. Cenários, PACT, jornadas e storyboards
5. Prototipação
6. Princípios de Krug
7. Requisitos com critérios de aceite de acessibilidade
8. Roteiro do projeto em 4 etapas

---

## 1. Modelos de processo

### 1.1 ISO 9241-210:2019 — Design centrado no humano [87]

| Princípios (cl. 5) | Atividades (cl. 7, iterativas) |
|---|---|
| (1) Design baseado em entendimento explícito de usuários, tarefas e ambientes | 1. Entender e especificar o contexto de uso |
| (2) Usuários envolvidos durante todo o design e desenvolvimento | 2. Especificar os requisitos do usuário |
| (3) Design guiado e refinado por avaliação centrada no usuário | 3. Produzir soluções de design |
| (4) Processo iterativo | 4. Avaliar os designs em relação aos requisitos |
| (5) O design trata a experiência do usuário como um todo | |
| (6) Equipe com habilidades e perspectivas multidisciplinares | |

A 2ª edição (2019) é revisão menor da de 2010: atualiza a Figura 1, **acrescenta
informação sobre acessibilidade em 7.1** e faz ajustes editoriais [87]. Só a
amostra da norma foi lida.

### 1.2 Double Diamond / Framework for Innovation (Design Council) [112]
- Lançado em 2004. Fases: **Discover** ("helps people understand, rather than simply
  assume, what the problem is"), **Define**, **Develop** (co-design com pessoas
  diversas), **Deliver** (testar em pequena escala, descartar o que não funciona).
  Não é linear.
- Princípios: "Put people first"; "Communicate visually and inclusively";
  "Collaborate and co-create"; "Iterate, iterate, iterate". Métodos em Explore,
  Shape e Build. A data de atualização de 2019 vem de fontes secundárias.

### 1.3 Rogers, Sharp & Preece — *Interaction Design*, 6ª ed. (Wiley, 2023) [113]
Ciclo de vida de manual (estabelecer requisitos ↔ projetar alternativas ↔
prototipar ↔ avaliar, com "descobrir requisitos" no centro). O diagrama **não foi
verificado na 6ª edição** e pode ter mudado entre edições (a confirmar).

### 1.4 Barbosa & Silva e engenharia semiótica
- Barbosa & Silva (2010), *Interação Humano-Computador*, Elsevier [114]: bibliografia
  básica da disciplina [1].
- **Versão ampliada:** Barbosa, Silva, Silveira, Gasparini, Darin & Barbosa (2021),
  *Interação Humano-Computador e Experiência do Usuário*, autopublicação no Leanpub,
  preço livre (mín. US$ 0,99, sugerido US$ 9,99), obra em andamento, atualizada em
  20/12/2025 [115][129]. Sumário não verificado; iniciais do último autor divergem
  entre fontes (a confirmar).
- **Engenharia semiótica** (de Souza, 2005) [92]: a interface é uma
  **metamensagem do designer ao usuário**; avaliação por **MIS** e **MAC** (ver
  `metodos-de-avaliacao.md` §5) (a confirmar no livro).
- Comunidade brasileira: anais do IHC na SOL/SBC e o glossário "IHCionário" [129].

### 1.5 Como amarrar os modelos no relatório (inferência)

| Disciplina (slides [1]) | Double Diamond | ISO 9241-210 | Entregas do app |
|---|---|---|---|
| **Entender** | Discover | Entender o contexto de uso | Entrevistas, questionário |
| | Define | Especificar requisitos | Análise temática, personas, PACT, cenários-problema, requisitos com critérios WCAG |
| **Desenhar** | Develop | Produzir soluções | Esboços, papel, wireframes, Wizard of Oz, alta fidelidade |
| **Avaliar** | Deliver | Avaliar | Heurística, teste com SUS, auditoria |

Citar a ISO 9241-210 junto com a acessibilidade (7.1) mostra que acessibilidade é
parte do processo, não fase final. Citar Barbosa et al. (2021) ao lado de Barbosa
& Silva (2010) mostra bibliografia atualizada.

---

## 2. Pesquisa com usuários

### 2.1 Roteiro de entrevista (NN/g, Rosala, 2021) [97]
1. Escrever primeiro as **perguntas de pesquisa**.
2. Brainstorm de todas as perguntas possíveis.
3. Transformar perguntas fechadas em abertas ("Descreva um dia típico" em vez de
   "Você trabalha em equipe?").
4. Conferir se cada pergunta de pesquisa está coberta.
5. Ordenar logicamente (cronologia ou jornada): aquecimento no início, reflexão no fim.
6. Preparar perguntas de acompanhamento e de sondagem.
7. **Pilotar** o roteiro.

Tipos: aquecimento; abertas baseadas em histórias ("Conte sobre a última vez
que…"); acompanhamento ("Quando foi isso?"); sondagem ("Por que isso é importante
para você?"). O roteiro é flexível, mas improvisar aumenta o risco de perguntas
indutoras [97]. Modelo: `assets/templates/roteiro-entrevista.md`.

Exemplo para o app (inferência). Indutora: "Você não acha que um modo de alto
contraste ajudaria?" Neutra: "Conte a última vez que você estudou por um PDF no
celular. O que aconteceu?"

### 2.2 Quantas entrevistas

| Estudo | Achado |
|---|---|
| Guest, Bunce & Johnson (2006) [98] | Em 60 entrevistas, saturação nas primeiras **12**; metatemas já na 6ª. A saturação orienta pouco o tamanho da amostra antes da coleta |
| **Hennink & Kaiser (2022)** [99], revisão sistemática (23 artigos) | Entrevistas: maioria saturou entre **9 e 17** (média ~12–13; faixa 5–24). Grupos focais: **4 a 8** (média ~5–6). Ajustar a objetivos e homogeneidade; não virar "número genérico" |
| Hennink, Kaiser & Marconi (2017) [100] | **Saturação de códigos** ("ouvimos tudo?") em **9**; **saturação de significado** ("entendemos tudo?") em **16–24** |

**Implicação para o app (inferência):** meta de **8 a 12 entrevistas**, com 3 a 5
estudantes com baixa visão incluídos de propósito. Se usar análise temática
reflexiva, justifique a amostra por **profundidade e poder de informação**, não
por "saturação".

### 2.3 Questionários (manual — lacuna nas notas)
As notas **não** trouxeram fonte verificada sobre desenho de questionários. As
orientações abaixo são de manual de métodos de pesquisa em IHC (ex.: Lazar, Feng
& Hochheiser, *Research Methods in HCI*, 2ª ed., 2017 [122], a confirmar):
- Questionário complementa a entrevista: dá **amplitude** (quantos), não
  **profundidade** (por quê). Use para perfil, hábitos e preferências.
- Uma ideia por pergunta (evite "duplo cano": "o app é rápido e bonito?").
- Linguagem neutra, sem induzir; escala Likert com âncoras rotuladas e opção "não
  sei / prefiro não responder".
- Viés de aquiescência: alterne algumas formulações, mas sem confundir.
- Perguntas sensíveis (deficiência) no fim, **opcionais**, com explicação do porquê.
- Pilotar com 2–3 pessoas; medir o tempo (meta: ≤ 10 min).
- Amostra de conveniência não permite generalizar: declare isso.

Modelo: `assets/templates/questionario.md`.

### 2.4 Análise: temática reflexiva e diagrama de afinidade
- **Braun & Clarke** (formulação recente; fonte secundária [101]): (1)
  familiarização; (2) codificação; (3) temas iniciais; (4) desenvolvimento e revisão;
  (5) refinamento, definição e nomeação; (6) redação. **Recursivas**, não lineares.
- Na TA reflexiva, evite alegar "saturação" e medir concordância entre codificadores
  (kappa) [101]. "Our assumptions always influence our research — it's not a
  question of whether they influence but how" (resenha do livro [101]). Temas não
  "emergem": são construídos pelo pesquisador (Morriss, 2024 [102]).
- **Diagrama de afinidade** (manual, a confirmar): cada observação ou citação vira
  um post-it (P03: "desisto quando preciso dar zoom e perco a linha") → agrupar por
  semelhança → nomear grupos → agrupar grupos em temas. Funciona bem em Miro ou
  FigJam. Para manter acessível à equipe, exporte também como lista em texto.
- Cadeia de saída: **tema → insight → requisito**.

### 2.5 Recrutar e incluir pessoas com deficiência com respeito [103]
- **Mais tempo** para recrutar; parcerias com organizações da comunidade ou de
  defesa de direitos (no Brasil, por exemplo, associações de pessoas com deficiência
  visual e o núcleo de acessibilidade da universidade — exemplo de inferência).
- **Diversidade dentro da deficiência visual** (cegueira, baixa visão, daltonismo) e
  das TAs.
- **Remuneração justa**, com consideração extra a usuários de TA; reembolsar
  transporte.
- **Materiais acessíveis**: formulários, TCLE e instruções; prefira documentos
  digitais; cuidado com PDFs.
- Sessões remotas: teste antes a acessibilidade da ferramenta de vídeo; ofereça
  entrevista **individual**; peça feedback ao fim.
- Linguagem: "pessoa com deficiência visual", "pessoa com baixa visão". Pergunte a
  **todos** se precisam de ajuste, sem presumir.
- **"Nada sobre nós sem nós"** (origem atribuída a J. Charlton, 1998 [130], a
  confirmar): envolver estudantes com baixa visão na pesquisa, no co-design e nos
  testes, não só na validação final. Apoio normativo: princípio (2) da ISO 9241-210.
- Tornar o próprio material de pesquisa acessível já testa a proposta inclusiva
  (inferência).

### 2.6 Outros métodos (manual, não verificados nas notas)
- **Investigação contextual** (Beyer & Holtzblatt, *Contextual Design*, 1998/2017
  [123], a confirmar): modelo mestre-aprendiz; princípios de contexto, parceria,
  interpretação e foco. Ex.: observar o aluno estudando com o próprio ampliador.
- **Estudo de diário** (NN/g, não lido): autorrelato longitudinal por intervalo,
  sinal ou evento. Ex.: uma semana registrando "momentos em que desisti de uma
  explicação".

---

## 3. Personas

### 3.1 Origens e tipos
- **Cooper** (*The Inmates Are Running the Asylum*, 1999; *About Face*, 4ª ed.,
  2014) [105] (a confirmar).
- **Pruitt & Grudin (2003)** [104]: estenderam a técnica de Cooper em 3 anos de uso
  na Microsoft; personas "can engage team members very effectively", transmitem
  dados qualitativos e quantitativos e complementam outros métodos.
- **Três tipos (NN/g, Laubheimer, 2020)** [106]:

| Tipo | Base | Custo | Limite |
|---|---|---|---|
| **Proto-persona** | Oficina de 2–4 h, sem pesquisa nova; 3–6 personas | Baixo | **Hipótese**; pode reforçar suposições erradas |
| **Qualitativa** (melhor custo-benefício) | 5–30 entrevistas codificadas em temas | Médio | Não mostra que fração da base cada persona representa |
| Estatística | Qualitativo + survey com 500+ (mínimo ~100) + clusterização | Alto | Cara; muitas vezes parecida com a qualitativa |

**Implicação para o app:** personas **qualitativas**, a partir das entrevistas.
Se a equipe começar com proto-personas, rotule-as como hipóteses e valide-as na
pesquisa.

### 3.2 Inclusão sem estereótipo
- **Microsoft Inclusive Design** [107]: "Recognize exclusion", "Solve for one, extend
  to many", "Learn from diversity". **Espectro de personas**: permanente, temporária,
  situacional (um braço / braço quebrado / segurando um bebê). Nos EUA, 26 mil
  pessoas/ano perdem membros superiores, mas o grupo passa de 20 milhões incluindo
  limitações temporárias e situacionais. Exclusão situacional: "distracted driving,
  loud environments, or simply having an overwhelming day".
- **W3C WAI, Stories of Web Users** [108]: inclui **Elias** (baixa visão, tremor,
  perda leve de memória de curto prazo; ajudado por texto ajustável e layout
  consistente), **Marta** (surdocega; ampliação, legendas, transcrições),
  **Lakshmi** (cega; leitor de tela), **Stefan** (estudante com dislexia e TDAH),
  **Dhruv** (estudante idoso, surdo), **Lexie** (daltonismo). As histórias
  "represent the experiences of some people with disabilities".
- **GOV.UK accessibility personas** (2019) [109]: Pawel (Asperger), Simone
  (dislexia), **Ashleigh (parcialmente cega, usa leitor de tela)**, Christopher
  (artrite, controle por voz), Ron, Claudia. Cada membro "veste" uma persona por
  50 min e compartilha achados por 10 min. **Ressalva explícita: "not a substitute
  for testing with real users"**; simulação nunca representa uma deficiência.
- Críticas a personas: Marsden & Haag (2016), estereótipos e política [121] (conteúdo
  a confirmar).

**Implicação para o app (inferência):**

| Persona | Papel |
|---|---|
| Primária: estudante com **baixa visão** (zoom 200–400%, alto contraste, lê PDFs de aula, fã de um universo específico) | Garante o foco da Parte 1 |
| Secundária: estudante sem deficiência, com pouco tempo e dificuldade em redes | Testa a personalização em geral |
| Espectro "ler conteúdo denso": baixa visão (permanente), olhos cansados ou pós-cirurgia (temporária), celular sob o sol ou no ônibus (situacional) | Mostra benefício ampliado |

Baseie a persona em **comportamentos, objetivos e estratégias de contorno**
observados, não no diagnóstico. Inclua o que a pessoa **consegue** fazer e suas
TAs; evite "fotos de sofrimento". Acrescente o campo **"universo de interesse e
profundidade"** (fã casual × profundo), que alimenta a personalização (Walkington
& Bernacki [46]). Modelo: `assets/templates/persona.md`.

Complemento possível: *Jobs-to-be-done* — "Quando [situação], quero [motivação],
para que [resultado]" (não verificado nas notas; a confirmar).

---

## 4. Cenários, PACT, jornadas e storyboards

### 4.1 PACT (Benyon) [110]
Pessoas, Atividades, Contextos, Tecnologias; o cenário ideal fica na interseção
(slides [1]). Livro em português: Benyon, *Interação Humano-Computador*, Pearson,
2011, ISBN 978-85-7936-109-8 (tradução de *Designing Interactive Systems*; edição
do original a confirmar; o original está na 3ª ed., ISBN 9781447920113). A descrição
detalhada do PACT vem de conhecimento de manual (a confirmar).

| | App de estudos (inferência) |
|---|---|
| **P** | Universitários, inclusive com baixa visão (ampliação, alto contraste, leitor de tela parcial); interesses e profundidade de fã variados |
| **A** | Entender um conceito (TCP/IP), revisar antes da prova, fazer quiz; frequência alta perto de provas; pressão de tempo |
| **C** | Físico (ônibus, biblioteca, sol), social (grupo de estudo), organizacional (AVA, PDFs dos professores) |
| **T** | Celular Android/iOS com zoom do sistema, tema escuro, fonte grande; notebook com ampliador ou NVDA; LLM no back-end |

Modelo: `assets/templates/cenario-pact.md`.

### 4.2 Design baseado em cenários (Rosson & Carroll, 2002) [111]
Sequência (conhecimento de manual da obra, a confirmar):
1. **Cenário-problema**: a situação atual. Ex.: "Ana, com baixa visão, tenta
   entender TCP/IP num PDF de slides a 300% de zoom no ônibus, perde a linha e
   desiste."
2. **Cenário de atividade**: o que a nova solução faz, sem interface.
3. **Cenário de informação**: como o conteúdo é apresentado (texto que reflui,
   contraste, tabela de mapeamento).
4. **Cenário de interação**: gestos, voz, foco.

**Análise de claims:** em cada etapa, registre "característica → **+** vantagem /
**−** desvantagem". Ex.: "Analogia com o universo do aluno → + interesse
situacional [47]; − risco de detalhe sedutor e de metáfora para quem prefere
linguagem literal [41][14]".

Contextos situacionais (luz, mobilidade, cansaço) devem estar explícitos nos
cenários de baixa visão.

### 4.3 Mapa de jornada e storyboard (manual, não verificados)
- **Mapa de jornada** (NN/g, Gibbons 2018 [126], a confirmar): fases × ações,
  pensamentos, emoções e oportunidades. Para o app, acrescente uma raia de
  **barreiras de acessibilidade** e uma de **estratégias de contorno** (inferência).
- **Storyboard** (Truong, Hayes & Abowd 2006 [127], a confirmar): quadros com
  personagem, contexto e passagem de tempo. Descreva cada quadro em texto, para que
  o storyboard também seja acessível a quem não enxerga a imagem.

---

## 5. Prototipação

### 5.1 O que um protótipo prototipa (Houde & Hill, 1997) [116]
"Any representation of a design idea, regardless of medium". Três dimensões:

| Dimensão | Pergunta | Exemplo no app |
|---|---|---|
| **Role** (papel) | Que papel o artefato tem na vida do usuário? | O aluno usaria analogias antes da prova? (papel + Wizard of Oz) |
| **Look and feel** | O que se vê, ouve e sente? | Tema de alto contraste, tipografia a 400% |
| **Implementation** | Como funciona? | Latência real de um LLM gerando a analogia |

Protótipos de **integração** ficam no centro do triângulo e são os mais caros.
"Prototypes are not self-explanatory: looks can be deceiving" [116].

### 5.2 Fidelidade (inferência + manual)
- Fidelidade não é uma escala única: McCurdy et al. (2006) [124] propõem várias
  dimensões e defendem protótipos de **fidelidade mista** (a confirmar). Ex.: alta
  fidelidade de contraste e tipografia com baixa fidelidade de dados.
- **Papel** (Snyder, 2003 [125], a confirmar): rápido, barato, convida à crítica. Para
  co-design com baixa visão: papel grande, marcadores grossos de alto contraste,
  componentes recortáveis e o facilitador descrevendo em voz alta (inferência).
- **Wireframes** de média fidelidade: anote hierarquia de títulos e ordem de foco
  desde já.

### 5.3 Wizard of Oz para simular a personalização por LLM [117]
A interface "appears to be autonomous but is (fully or partially) controlled by a
human". Papéis: facilitador, **mágico**, usuário.

| Passo | No app (inferência) |
|---|---|
| 1. Criar o protótipo com componentes fáceis de atualizar | Tela "Explicação" com áreas de texto editáveis |
| 2. Escolher respostas fechadas, abertas ou híbridas | **Híbridas**: banco curado de explicações TWA para 3–4 universos comuns + escrita ao vivo para universos inesperados |
| 3. Protocolo com diretrizes de tom | Template TWA obrigatório (conceito, cena, mapeamento, onde falha, versão técnica) |
| 4. Treinar o mágico | Ensaio com cronômetro: tempo realista de "geração" |
| 5. Pilotar | 1 colega antes dos participantes |

Armadilhas: respostas inviáveis tecnicamente (consulte quem vai implementar),
variação alta no modo aberto, participante que desconfia do humano. **Ética:**
debriefing quando houver engano; inclua isso no TCLE [117]. Indicado para
chatbots, recomendações e IA generativa, antes de investir na construção.

Pesquisa recente aplica WoZ à integração de IA (NexOz; arXiv 2510.06872), não lida
na íntegra (a confirmar).

### 5.4 Alta fidelidade no Figma com acessibilidade
- **Kits de anotação** [118][128]: GitHub Annotation Toolkit (Primer; fork do kit
  da CVS Health; CC-BY 4.0): anotações de fluxo, interações (teclado, toque),
  cabeçalhos e landmarks, formulários, **ordem de foco e de leitura**, idioma,
  feedback e live regions; suporta iOS e Android. Alternativas: A11y Annotation
  Kit (Atlassian), Microsoft "Include". O ThoughtWorks Radar recomenda "accessibility
  annotations in designs".
- Plugin "Accessibility Persona Lens", inspirado nas personas do GOV.UK.
- Plugins Stark, Able e Contrast, e o suporte do Figma a *variables/modes* para
  temas e tokens: **não verificados** (a confirmar na Figma Community).
- Prática (inferência): modos claro / escuro / alto contraste; tokens de cor
  validados com `scripts/contrast_check.py --palette`; frames de 320 px de largura
  para simular 400%; tipografia testada a 200%; alvos ≥ 24×24 (meta 44×44).

### 5.5 Ferramentas de IA (cautela)
- **Figma Make**: beta em maio de 2025 (Config 2025), disponível para todos em
  24/07/2025; depende do tipo de assento e consome créditos de IA. A matéria **não
  menciona acessibilidade** [119]. A Intopia publicou sobre acessibilidade em
  protótipos gerados por IA (não lido).
- Estado em out/2026 do Figma Make e concorrentes (v0, Lovable, Google Stitch):
  não verificado.
- **Regra (inferência):** use para explorar alternativas; todo resultado passa por
  verificação manual (contraste, rótulos, ordem de foco). Não há evidência de que
  gerem saídas acessíveis por padrão.

---

## 6. Princípios de Krug (*Don't Make Me Think, Revisited*, 3ª ed., 2014) [120]
Via resumo secundário:
- **1ª lei:** a página deve ser autoevidente; cada pergunta desnecessária aumenta a
  carga cognitiva.
- **2ª lei:** o número de cliques importa menos que cada clique ser uma escolha
  inequívoca e sem esforço.
- **3ª lei:** "omit needless words" (corte metade, depois metade do que sobrou).
- Fatos: escaneamos em vez de ler; *satisficing*; "muddle through".
- **Trunk test:** largado numa página interna, o usuário responde sem hesitar: que
  site é este? Em que página estou? Quais as seções principais? Onde estou nelas?
  Como busco?

**Implicação para o app (inferência):** aplicar o trunk test **a 400% de zoom e no
celular**. Com ampliação, a pessoa vê só um recorte, então título da página e
"onde estou" precisam aparecer no ponto de entrada da área visível. A 3ª lei vale
para as explicações geradas: limite de tamanho por segmento.

---

## 7. Requisitos com critérios de aceite de acessibilidade

Fontes sobre user stories (Cohn, GOV.UK Service Manual) não foram pesquisadas.
Os números WCAG abaixo foram **conferidos em `acessibilidade.md`**, que se baseia
nas notas de acessibilidade [7][16][30].

**Modelo (Gherkin):**
> **US-07.** Como estudante com baixa visão, quero ampliar a explicação sem perder
> conteúdo, para estudar no celular sem rolagem horizontal.
>
> - **Dado** zoom de 200%, **quando** abro uma explicação, **então** nenhum texto
>   ou botão é cortado — `1.4.4 Redimensionar texto (AA)`.
> - **Dada** largura de 320 CSS px (1280 px a 400%), **então** não há rolagem
>   horizontal e a tabela de mapeamento vira lista — `1.4.10 Realinhar (AA)`.
> - **Dado** espaçamento de texto aumentado (linha 1,5; parágrafo 2×; letras 0,12;
>   palavras 0,16), **então** nada se sobrepõe — `1.4.12 (AA)`.
> - Texto ≥ 4,5:1 e componentes/foco ≥ 3:1 — `1.4.3 (AA)`, `1.4.11 (AA)`.
> - Foco visível e não coberto por barra fixa — `2.4.7 (AA)`, `2.4.11 (AA)`.
> - Botões "sem analogia" e "trocar universo" ≥ 24×24 CSS px — `2.5.8 (AA)`.
> - Botões com nome acessível e estado — `4.1.2 Nome, função, valor (A)`.

**Outras histórias típicas (inferência):**
- "Como aluno, quero ver a explicação sem analogia, para conferir o conteúdo técnico"
  → critério: alternância a um toque, estado anunciado (`4.1.2`) — COGA 4.4.4 [14].
- "Como aluno, quero saber por que a explicação usou *One Piece*" → rótulo G11 [61].
- "Como aluno, quero fazer o quiz sem cronômetro" → `2.2.1 (A)`.

Lista completa de requisitos RA01–RA24: `acessibilidade.md` §10. Diretrizes de
personalização DP01–DP18: `carga-cognitiva-e-personalizacao.md` §12.

**Rastreabilidade:** tema da análise → insight → requisito/história → elemento do
protótipo → tarefa do teste → resultado (ver `assets/estrutura-projeto.md`).

---

## 8. Roteiro do projeto em 4 etapas

| Etapa | Atividades | Entregas concretas (pastas de `estrutura-projeto.md`) | Critério de "pronto" |
|---|---|---|---|
| **1. Pesquisa com usuários** (Entender / Discover) | Perguntas de pesquisa; verificar ética com o professor (CEP se for usar no TCC); recrutar com antecedência; **8–12 entrevistas** (3–5 com baixa visão); questionário online acessível; análise temática ou diagrama de afinidade | `plano-de-pesquisa.md`, `roteiro-entrevista.md`, `questionario.md` + link, `tcle.md`, `dados/` anonimizados (P01…), `sintese.md` com 4–6 temas e insights | Cada insight tem citação de participante; materiais testados com leitor de tela e zoom 200% |
| **2. Personas e cenários** (Define) | 2–3 personas qualitativas (1 com baixa visão) + espectro; PACT; cenários-problema → atividade → interação com claims; jornada com raia de barreiras; requisitos | `personas.md`, `pact.md`, `cenarios.md`, `jornada.md`, `requisitos.md` (histórias + critérios WCAG + DP da personalização) | Toda persona e todo requisito apontam para um tema da etapa 1 |
| **3. Prototipação** (Desenhar / Develop) | Esboços → papel (co-design) → wireframes anotados → **Wizard of Oz** da explicação personalizada → alta fidelidade no Figma (temas, tokens validados, frames de 320 px, kit de anotação) e/ou HTML/React | `baixa-fidelidade/`, `alta-fidelidade/` (link Figma/código), `design-tokens.json` validado, `decisoes-de-design.md` (decisão → achado/persona/critério) | Paleta passa em `contrast_check.py`; protótipo navegável nas tarefas T1–T5; anotações de foco e títulos |
| **4. Avaliação** (Avaliar / Deliver) | Heurística (3–5 avaliadores) → auditoria WCAG → correções → teste moderado com **5–8 participantes** (≥ 1 com baixa visão, própria TA), SEQ, SUS, Leppink → análise → melhorias | `avaliacao-heuristica.md`, `auditoria-wcag.md`, `protocolo-teste.md`, `sus-respostas.csv`, `resultados.md`, `melhorias.md`, `relatorio-final.md` | SUS com IC 95%; problemas priorizados por severidade; cada melhoria rastreada até um achado |

Detalhes da etapa 4: `metodos-de-avaliacao.md` §12.

**Por que assim:** segue a ISO 9241-210 (usuários envolvidos em todo o processo,
avaliação que refina o design, iteração) e o ciclo Entender → Desenhar → Avaliar da
disciplina. A rastreabilidade é o que transforma artefatos soltos em um projeto de IHC.
