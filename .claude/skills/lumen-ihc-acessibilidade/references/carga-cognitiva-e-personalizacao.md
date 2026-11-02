# Carga cognitiva, aprendizagem multimídia e personalização por interesses

Fundamentação científica do coração do app: explicar conteúdo (ex.: redes de
computadores) pelo universo de interesse do aluno (jogo, anime, esporte).
Estado em **28/10/2026**. Os números [n] remetem a `bibliografia.md`.

**Marcadores:** **(a confirmar)** = referência clássica citada de memória ou dado
de fonte secundária; **PREPRINT** = não revisado por pares; **(inferência)** =
aplicação de Lumen, não afirmação da fonte.

## Sumário
1. Teoria da Carga Cognitiva (CLT, versão 2019)
2. Medir carga cognitiva
3. Aprendizagem multimídia (Mayer) e detalhes sedutores
4. Personalização por interesse: a evidência
5. Analogias: Gentner, Glynn (TWA) e onde a analogia falha
6. LLMs na aprendizagem (2023–2026)
7. Diretrizes de interação humano-IA (Amershi, PAIR)
8. Adaptativo × adaptável (Findlater & McGrenere)
9. UDL 3.0
10. Acessibilidade cognitiva: COGA × metáforas, TDAH, dislexia
11. Privacidade: LGPD e ANPD para dados de interesse
12. Diretrizes de design para a personalização do app

---

## 1. Teoria da Carga Cognitiva (CLT, versão 2019)

Referência-base: Sweller, van Merriënboer & Paas (2019), "20 Years Later",
*Educational Psychology Review* 31(2):261–292, DOI 10.1007/s10648-019-09465-5 [31].

| Conceito | O que diz a versão 2019 [31] |
|---|---|
| **Carga intrínseca** | Depende da complexidade da informação **e** do conhecimento prévio: "only can be changed by changing what needs to be learned or changing the expertise of the learner" |
| **Carga extrínseca** | Vem da forma de apresentação e do procedimento exigido; "is not determined by the intrinsic complexity of the information" |
| **Carga germana (redefinida)** | Deixa de ser um terceiro tipo que soma: são recursos de memória de trabalho **redistribuídos** das atividades extrínsecas para as intrínsecas. Intrínseca + extrínseca são os tipos que somam |
| **Interatividade de elementos** | Relativa ao aprendiz: o mesmo material é de baixa interatividade para o especialista e de alta para o novato. "Effective instructional procedures reduce element interactivity while ineffective ones increase element interactivity" |
| **Reversão de expertise** | Efeitos que ajudam novatos "first decrease in size, then disappear, and can eventually reverse" [31]. Seminal: Kalyuga, Ayres, Chandler & Sweller (2003) [32] (ordem de autores a confirmar) |

**Efeitos listados em 2019 relevantes ao app** [31]: *self-management*
(o aluno aprende a gerir a própria carga), **transient information** (áudio ou
animação que some em segundos aumenta a carga extrínseca), *guidance-fading*,
*self-explanation*, *isolated elements*, *collective working memory*, *human
movement*.

> Analogia para o aluno: a memória de trabalho é a mesa de estudo. A carga
> intrínseca é o tamanho do quebra-cabeça; a extrínseca é a bagunça em cima da
> mesa. A germana não é uma terceira pilha de coisas: é o tempo que sobra para
> montar o quebra-cabeça quando a bagunça sai.

**Implicação para o app (inferência):**
- A analogia temática só ajuda se **reduzir a interatividade de elementos**
  (ligar o conceito a esquemas que o aluno já tem). Se trouxer personagens e lore
  para processar, vira carga extrínseca.
- **Fading** por expertise: mais analogia para quem é novato no tópico, menos ou
  opcional para quem já domina. Detectar por pergunta de nível ou pré-teste curto.
- Explicação em áudio ou vídeo gerada por LLM precisa de controle de ritmo e de
  transcrição (efeito de informação transitória).

---

## 2. Medir carga cognitiva

| Instrumento | Formato | O que mede | Fonte |
|---|---|---|---|
| **Escala de Paas (1992)** | 1 item, 9 pontos, de "muito, muito baixo" a "muito, muito alto" esforço mental; teste-reteste r = 0,90 | Carga global; "sensitive to small differences", mas não separa os tipos | [33][31] |
| **Leppink et al. (2013)** | 10 itens, escala de 0 a 10: **IL itens 1–3**, **EL itens 4–6**, **GL itens 7–10** | Separa intrínseca, extrínseca e germana | [34] |
| **NASA-TLX** (Hart & Staveland, 1988) | 6 subescalas (exigência mental, física, temporal; desempenho; esforço; frustração) com ponderação por pares; **Raw TLX** sem ponderação | Carga de trabalho da tarefa | [35][36] |
| Tarefa secundária, fisiológicas (EEG, rastreamento ocular) | — | Intrusivas, pouco separam tipos de carga | [31] |

**Leppink et al. (2013)** [34]: validado com n = 56 (PCA), 171 (CFA), 136 + 148
(validação cruzada) e 58 (experimento). Itens-exemplo: IL "The topic/topics
covered in the activity was/were very complex"; EL "The instructions and/or
explanations during the activity were very unclear"; GL "The activity really
enhanced my understanding of the topic(s) covered". Sweller et al. (2019) aceitam
que IL e EL "can be differentiated" com ele, mas pedem mais evidência [31].
Sweller et al. **não** discutem o NASA-TLX [31].

**Implicação para o app (inferência):** o instrumento de Leppink testa a hipótese
central: "a analogia temática **reduz** a carga intrínseca percebida sem
**aumentar** a extrínseca". A escala de Paas serve como medida rápida após cada
explicação. O NASA-TLX combina mais com a usabilidade da interface. Não existe
tradução validada para o português dessas escalas nas notas (a confirmar); ver
`metodos-de-avaliacao.md`.

**Lacuna:** não foram encontrados estudos que meçam com Leppink especificamente
explicações analógicas personalizadas por interesse.

---

## 3. Aprendizagem multimídia (Mayer) e detalhes sedutores

### 3.1 Os 15 princípios (Mayer, 2020, *Multimedia Learning*, 3ª ed.) [37]

| Princípio | Regra | Uso no app |
|---|---|---|
| **Coerência** | Excluir material estranho | Podar lore sem correspondência no conceito |
| **Sinalização** | Destacar a organização do essencial | Rotular "em redes, isso se chama *roteador*" |
| Redundância | Gráfico + narração > gráfico + narração + texto | Não ler em voz alta o texto que já está na tela junto com o diagrama |
| Contiguidade espacial | Palavra e imagem correspondentes juntas | Rótulos dentro do diagrama |
| Contiguidade temporal | Apresentadas simultaneamente | — |
| **Segmentação** | Segmentos com ritmo do aprendiz | Explicação em blocos com "próximo" |
| **Pré-treino** | Nomes e características dos conceitos-chave antes | Termos técnicos (pacote, IP, roteador) antes da analogia |
| Modalidade | Gráfico + narração > gráfico + texto | Opção de áudio, mantendo o texto (dislexia, baixa visão) |
| Multimídia | Palavras + imagens > só palavras | Diagrama da analogia com alt text |
| **Personalização** | Estilo conversacional > formal | Tom "você" nas explicações |
| Voz | Voz humana amigável > voz de máquina | — |
| Imagem | Imagem do orador não necessariamente ajuda | Avatar não é necessário |
| Incorporação | Instrutor com gestos > sem | — |
| Imersão | 3D não é necessariamente melhor que 2D | — |
| **Atividade generativa** | Guiar atividades generativas ajuda | "Crie sua analogia", autoexplicação |

O documento consultado não traz tamanhos de efeito por princípio [37].

**Atenção terminológica:** o "princípio da personalização" de Mayer trata do
**estilo conversacional**, não de personalização por interesse. No relatório,
distinga **personalização linguística** (Mayer) de **personalização de
contexto/interesse** (Walkington; Cordova & Lepper) [37].

### 3.2 Detalhes sedutores: o principal risco do app

| Estudo | Achado |
|---|---|
| Garner, Gillingham & White (1989) [39] | Origem do conceito; adultos (mais memória de trabalho) são menos afetados que crianças (via fonte secundária) |
| **Harp & Mayer (1998)** [38] | Os detalhes desviam ao "activating an inappropriate base of prior knowledge". No **início** prejudicaram mais; no **fim**, resultado semelhante à lição sem eles. Sem os detalhes, ~3× mais chance de lembrar o que é estruturalmente importante (via fonte secundária; a confirmar) |
| **Rey (2012)** [40] | 39 efeitos; recordação g = −0,27 a −0,95; transferência g = −0,65 a −0,83; mais forte com detalhes visuais (a confirmar) |
| **Sundararajan & Adesope (2020)** [41] | 68 efeitos de 58 estudos, **g = −0,33** (pequeno a moderado). Pior com detalhes estáticos, texto + imagem, papel, **sem controle de ritmo** e detalhes **frequentes** ou no mesmo formato do conteúdo central. Relatado g = −0,70 para detalhes **no fim**, o que parece contradizer Harp & Mayer (resumo secundário; a confirmar) |

"Information that is interesting but irrelevant can be detrimental to learning"
(comunicado da WSU sobre [41]).

**Detalhe sedutor × contexto personalizado (inferência):** a diferença é a
**relevância estrutural**. O detalhe sedutor é interessante e irrelevante para o
modelo mental-alvo. O contexto personalizado de Walkington mantém a estrutura e
troca só a "cobertura". A analogia de Gentner mapeia relações. **Regra: todo
elemento do universo temático na explicação corresponde a um elemento do conceito.**

**Mitigações (moderadores de [41], inferência):** controle de ritmo; poucas
referências temáticas; nada de imagens temáticas decorativas; sinalização
explícita do termo técnico; termos técnicos antes da analogia (pré-treino).

---

## 4. Personalização por interesse: a evidência

### 4.1 Meta-análise de Lin, Lin, Zhang & Ginns (2024) [42]
*Educational Psychology Review* 36, art. 88, DOI 10.1007/s10648-024-09933-7.
34 publicações.

| Desfecho | k (tamanhos de efeito) | n | g |
|---|---|---|---|
| Interesse | 26 | 5.335 | **0,55** |
| Carga cognitiva | 8 | 1.228 | **0,54** (direção de redução inferida; a confirmar no texto completo) |
| Retenção | 46 | 5.991 | **0,48** |
| **Transferência** | **6** | **375** | **0,36** |

Moderadores não extraídos (a confirmar).

### 4.2 Estudos-chave

| Estudo | Desenho | Achado |
|---|---|---|
| **Anand & Ross (1987)** [43] | RCT, 48 alunos de 5º–6º ano, divisão de frações por CAI | Médias em teste de 11 questões: personalizado 5,95; concreto 3,58; abstrato 2,28; sem CAI 1,12. WWC: "meets standards without reservations" |
| **Cordova & Lepper (1996)** [44] | Jogo de aritmética, crianças | Contextualização, personalização e **escolha** aumentaram motivação, engajamento e aprendizagem (a confirmar) |
| **Walkington (2013)** [45] | 145 alunos de Álgebra I, Cognitive Tutor, randomizado; interesses: esportes, música, filmes, TV, games, arte, computadores, comida, lojas | Personalizado mais rápido e mais preciso; ganho maior ao escrever expressões simbólicas e entre alunos com dificuldade; vantagem mantida na unidade sem personalização. Imprensa: baixo desempenho 58% × 25%; "scaffold rather than a crutch" (fonte jornalística; a confirmar) |
| **Walkington & Bernacki (2018/2019)** [46] | ITS de álgebra; personalização **profunda** (experiências quantitativas reais do aluno) × **superficial** (troca de tema) | Benefício **só quando a profundidade combinava** com o engajamento do aluno com o interesse; menos *gaming the system*; mais profundidade → mais afeto positivo. Profundidade é "a critical feature" |
| **Bernacki & Walkington (2018)** [47] | 150 alunos do ensino médio, 4 unidades num ITS | A personalização aumentou o **interesse situacional desencadeado**, que previu acerto e eficiência; efeito total na nota de prova e no interesse individual em matemática |
| Høgheim & Reber (2015) [48] | Ensino fundamental II | Ganho maior em alunos com baixo interesse inicial (a confirmar) |

Dimensões de design da personalização na literatura: **profundidade**,
**granularidade (grain size)**, **autoria/propriedade** e **quem personaliza** [46]
(texto relacionado não aberto; a confirmar).

### 4.3 Modelo de 4 fases do interesse (Hidi & Renninger, 2006) [49]
1. Interesse situacional **desencadeado**
2. Interesse situacional **mantido**
3. Interesse individual **emergente**
4. Interesse individual **bem desenvolvido**

**Implicação para o app (inferência):**
- O app usa um interesse de fase 4 (o hobby) para **desencadear** a fase 1 em
  redes. Para chegar às fases 2–4 em redes, a analogia precisa ser retirada aos
  poucos, até o conteúdo valer por si.
- Perguntar não só "qual seu jogo?" mas "**quanto** você conhece ou joga?":
  personalização profunda para fãs profundos (ex.: latência em partidas online
  para explicar RTT), superficial para fãs casuais [46].
- A evidência mais fraca é justamente a de **transferência** (k = 6), a que mais
  importa em engenharia. A avaliação deve medi-la (aplicar o conceito fora do
  universo temático), não só satisfação.
- O efeito maior em alunos com dificuldade [45] sugere priorizar esse público.

**Lacunas:** nenhuma meta-análise específica de computação/redes nem com
universitários de engenharia.

---

## 5. Analogias: Gentner, Glynn (TWA) e onde a analogia falha

- **Gentner (1983), structure-mapping** [50]: o núcleo da analogia é mapear
  **relações**, não atributos. **Sistematicidade**: preferem-se sistemas de
  relações interligadas (sistema solar ↔ átomo).
- **Duit (1991)** [52]: distingue analogias de transferência de **atributos**
  (água e eletricidade "fluem") das de transferência de **relações**; recomenda
  analogias **geradas pelos alunos** como diagnóstico de concepções prévias.
- **Modelo TWA de Glynn (1991)** [51], seis passos:

| # | Passo TWA | Bloco no template do app (inferência) |
|---|---|---|
| 1 | Introduzir o conceito-alvo | "O que é" (termos técnicos: pré-treino) |
| 2 | Evocar o análogo | Cena do universo do aluno |
| 3 | Identificar características relevantes | — |
| 4 | Mapear similaridades | **Tabela elemento ↔ elemento** (ex.: "mensageiro entre vilas ↔ pacote") |
| 5 | **Indicar onde a analogia falha** | Seção obrigatória "Onde a analogia quebra" |
| 6 | Tirar conclusões | Versão só com termos técnicos + pergunta de transferência fora do universo |

**Por que a seção "onde falha" é obrigatória:** sem ela o aluno transfere
atributos que não valem para o alvo e cria concepções alternativas. Não há
quantificação desse risco nas notas, nem estudo sobre analogias **geradas por LLM**
(lacuna).

**Implicação para o app (inferência):** o template TWA também funciona como
sinalização (Mayer) e trava contra detalhes sedutores, porque força cada elemento
temático a ter correspondente. Pela sistematicidade, o LLM deve escolher dentro
do universo do aluno a **estrutura** mais parecida (economia do jogo ↔ controle de
congestionamento; troca de mensagens entre personagens ↔ camadas), não só a
ambientação. Uma função "crie sua própria analogia" é atividade generativa e
diagnóstico [52].

---

## 6. LLMs na aprendizagem (2023–2026)

| Estudo | Status | Achado-chave |
|---|---|---|
| **Bastani et al. (2025)** *PNAS* 122(26) e2422633122 [53] | Revisado | ~1.000 alunos do ensino médio (Turquia). Na prática: +48% (GPT Base) e +127% (GPT Tutor). **Sem acesso depois: Base 17% pior** que quem nunca usou ("as a crutch"). Salvaguardas do Tutor "largely" mitigaram |
| **Fan et al.** *BJET*, DOI 10.1111/bjet.13544 [54] | Revisado | RCT, 117 universitários, escrita. ChatGPT: **maior melhora na nota da redação**, mas ganho de conhecimento e transferência **não diferiram**; alerta de "metacognitive laziness" |
| **Kestin et al. (2025)** *Sci. Reports* 15:17458 [56] | Revisado | Física em Harvard, ensaio cruzado (N = 142 IA, 174 sala). Pós-teste mediano 4,5 × 3,5 (pré 2,75); 0,63 DP (0,73–1,3 DP na regressão quantílica); 49 × 60 min. Design: prompt para **gerir carga cognitiva**, **andaime sequencial**, **soluções de especialistas no prompt** |
| Lehmann, Cornelius & Sting [55] | **PREPRINT** | Sem efeito geral. Uso **substitutivo** (o LLM resolve) → menos compreensão; **complementar** (pedir explicação) → melhor compreensão. O LLM **ampliou a diferença** entre alunos de baixo e de alto conhecimento prévio |
| PAIGE, Do et al. [57] | **PREPRINT** | n = 180; podcast personalizado melhor em Filosofia (7,30 × 5,85 × 5,95), efeito global misto em Psicologia (inconsistência interna nos números), nulo em Governo dos EUA |
| PAGE, Lim et al. [58] | **PREPRINT** | Materiais adaptados a curso e interesses num ITS por um semestre: "significantly improved learning outcomes" (n e efeitos não informados) |
| Walkington et al. (2026) [59] | **PREPRINT** | 7 professores, GPT-4o, 143 problemas, ~512–521 alunos do 7º ano. Professores usaram **categorias amplas**; alunos pediam **referências específicas**. 139 de 415 prompts foram para corrigir **realismo**. Notas médias ~2,5/5; sem controle |
| EDUMATH, Christ et al. [60] | **PREPRINT** | > 11 mil problemas gerados; customizados tiveram desempenho semelhante aos humanos e foram preferidos |

**Lacunas:** nenhuma avaliação causal independente do Khanmigo; nenhum estudo
revisado sobre analogias de cultura pop geradas por LLM em computação; sem taxas
de alucinação em explicações educacionais.

**Implicação para o app (inferência):**
- Ser **complementar** (explicar), não **substitutivo** (resolver exercícios):
  andaime, autoexplicação, nada de entregar resposta pronta.
- Ancorar a parte técnica em conteúdo **curado** (RAG ou gabarito de especialista),
  como Kestin et al.
- Dois tipos de alucinação: **técnica** (fato de redes errado) e **de lore**
  (fato errado sobre o anime, que destrói a credibilidade com o fã). Botão "isso
  está errado" (Amershi G9).
- Coletar interesses em nível de **obra, personagem ou mecânica**, não só categoria.
- Na avaliação, medir desempenho **sem o app** (pós-teste sem apoio), que é onde
  o dano aparece em Bastani.

---

## 7. Diretrizes de interação humano-IA (Amershi, PAIR)

**Amershi et al. (CHI 2019)**, DOI 10.1145/3290605.3300233 [61]. Dados do estudo
de validação não verificados (a confirmar).

| Fase | Diretriz | Aplicação no app (inferência) |
|---|---|---|
| Início | G1 Deixar claro o que o sistema faz | Onboarding: "uso seus interesses para criar analogias" |
| | G2 Deixar claro quão bem ele faz | "Analogias simplificam; confira a versão técnica" |
| Durante | G3 Momento conforme o contexto | Não sugerir trocar o universo no meio de um quiz |
| | G4 Informação contextualmente relevante | Analogia ligada ao tópico atual |
| | G5 Normas sociais relevantes | Tom respeitoso, não infantilizado |
| | G6 Mitigar vieses sociais | Não inferir interesses por gênero ou idade |
| Quando erra | G7 Invocação eficiente | Botão "explicar com meu interesse" |
| | G8 Dispensa eficiente | "Explicar sem analogia" |
| | G9 Correção eficiente | "Trocar universo"; "a referência está errada" |
| | G10 Limitar o escopo na dúvida | Sem universo adequado → explicação neutra |
| | G11 Explicar por que fez | "Explicado com base em: *One Piece* (você marcou como favorito)" |
| Ao longo do tempo | G12 Lembrar interações recentes | Retomar a última explicação |
| | G13 Aprender com o comportamento | Sugerir menos analogia quando acerta muito |
| | G14 Atualizar e adaptar com cautela | Sugerir, não impor |
| | G15 Feedback granular | "A analogia ajudou?" e "a referência ao anime está errada?" |
| | G16 Comunicar consequências | "Ao apagar este interesse, as próximas explicações…" |
| | G17 Controles globais | Interruptor geral de personalização; gerenciar interesses |
| | G18 Notificar mudanças | Avisar quando o perfil de interesses mudar |

**Google PAIR, People + AI Guidebook** [62]: lançado em 2019, atualizado em
2021, em revisão para IA generativa desde nov/2023. Capítulos: User Needs +
Defining Success; Mental Models; Explainability + Trust; Data Collection +
Evaluation; Feedback + Control; Errors + Graceful Failure. Perguntas abertas
para genAI: como ajudar a decidir se reescrever um texto gerado; como desenhar
com segurança diante de "hallucinations". O conteúdo detalhado dos padrões não
foi extraído (a confirmar).

**Bolha de filtro (inferência):** explicar sempre pelo mesmo universo pode
atrapalhar a abstração, porque a transferência pede variação de contexto. Varie
os universos de vez em quando ou feche com a versão neutra.

---

## 8. Adaptativo × adaptável (Findlater & McGrenere, CHI 2004) [63]

| Tipo | Quem controla | Resultado (menus, n = 27) |
|---|---|---|
| Estático | Ninguém | Significativamente mais rápido que o adaptativo |
| **Adaptativo** | O sistema | O mais lento; 30% de preferência |
| **Adaptável** | O usuário | Mais rápido que o adaptativo (quando não apresentado primeiro); quem customizou igualou o estático (300,72 × 301,76); **55% de preferência**; 16 de 27 o julgaram o mais eficiente |

Ressalva: é um estudo de **menus**, não de aprendizagem. A transposição é por
analogia.

**Implicação para o app:** **adaptação mista**. O aluno escolhe o universo e o
nível de analogia (nenhum, leve, profundo); o sistema pode **sugerir** mudanças
(ex.: reduzir analogia quando acerta muito), sem impor (G14, G17).

---

## 9. UDL 3.0 (CAST, julho de 2024) [64]

- Processo iniciado em 2020; versão 1.0 de 2008. **3 princípios** (Engajamento,
  Representação, Ação e Expressão), **9 diretrizes**, **36 considerações**.
- Mudanças: abordagem baseada em ativos; identidade como dimensão de
  variabilidade; barreiras individuais, institucionais e sistêmicas; linguagem
  centrada no aprendiz.
- Considerações relevantes: **Diretriz 7 "Welcoming Interests & Identities"**;
  7.2 "Optimize relevance, value, and authenticity"; **7.3 "Nurture joy and
  play"**; **7.4 "Address biases, threats, and distractions"**; 8.4 "Foster
  belonging and community"; 1.3 diversidade de perspectivas e identidades;
  2.4 vieses na linguagem e nos símbolos.
- Sem tradução oficial para o português encontrada.

**Implicação para o app:** 7.2 e 7.3 justificam explicar pelo interesse; 7.4
("distractions") é o contrapeso, alinhado aos detalhes sedutores. O princípio de
Representação sustenta oferecer a mesma explicação em **três versões
alternáveis**: técnica, analógica e diagrama.

---

## 10. Acessibilidade cognitiva: COGA × metáforas, TDAH, dislexia

- **COGA** (W3C Note, 29/04/2021) [14]: oito objetivos (ver `acessibilidade.md`
  §6.1). Padrões aplicáveis: palavras claras (4.4.1), **linguagem literal (4.4.4),
  que evita metáforas**, texto sucinto (4.4.5), resumos (4.4.8), mídia em blocos
  (4.3.5), uma instrução por vez (4.4.9), espaço em branco (4.4.10), indicador de
  progresso (4.2.4), limitar interrupções (4.6.1), evitar excesso (4.6.3), apoio à
  simplificação (4.9.3), controle sobre o que se move (4.9.1).
- **Tensão COGA × analogias (inferência):** para algumas pessoas com dificuldades
  cognitivas ou de linguagem (possivelmente também pessoas autistas que preferem
  linguagem literal), a analogia **aumenta** a carga. Saída: personalização
  opcional e reversível, explicação literal a um toque e tabela de mapeamento,
  que torna a metáfora explícita.
- **TDAH, Dai, Wufue & Zhang (2025)** [65]: RCT, 80 crianças de 6–12 anos, 8
  semanas; feedback imediato, pontos, níveis, dificuldade adaptativa. Tempo de
  reação ~550 → 440 ms (× 550 → 537); matemática 46,0 → 71,2 (× 46,2 → 50,8);
  ganhos mantidos na semana 16. **Evidência fraca**: sem cegamento, controle neutro,
  app dos próprios autores, referências aparentemente incorretas.
- **Dislexia, Rello & Baeza-Yates** [66]: fonte maior (~18 pt ou mais) melhora a
  legibilidade e o espaçamento pesa menos (de memória; **a confirmar**).
- **Limite da evidência:** nenhum estudo sobre personalização por interesse
  especificamente em estudantes com TDAH ou dislexia; nenhuma fonte brasileira
  revisada sobre acessibilidade cognitiva em apps educacionais com IA.

**Implicação para o app (inferência):** TDAH → segmentos curtos, progresso
visível, feedback imediato, pouca decoração (Garner et al. sugerem efeito maior de
detalhes sedutores com memória de trabalho menor; extrapolação). Dislexia →
controle de fonte e espaçamento, texto-para-fala com destaque sincronizado,
texto sempre disponível para reler.

---

## 11. Privacidade: LGPD e ANPD para dados de interesse

- Interesses e desempenho são **dados pessoais** sob a LGPD [68].
- Interesses (anime, futebol) **não** estão no rol de dados sensíveis do art. 5º,
  II, mas podem **revelar** convicção religiosa, opinião política ou orientação
  sexual. Essa leitura é inferência, não confirmada por fonte jurídica (a confirmar).
- **Menores:** Enunciado CD/ANPD nº 1/2023 (24/05/2023): qualquer base legal dos
  arts. 7º ou 11, "desde que observado e prevalecente o seu melhor interesse"; o
  art. 14, §1º, exige consentimento específico e em destaque de um dos pais
  quando a base for o consentimento; documentar a avaliação do melhor interesse
  [67] (fonte secundária; ler o enunciado oficial).

**Implicação para o app (inferência):** minimização (só o necessário para gerar a
analogia); apagar interesses a qualquer momento; não usar interesses para
publicidade; **pseudonimizar** o que vai para o provedor do LLM; se houver menores
de 18, documentar o melhor interesse. Para a pesquisa com usuários, ver ética em
`metodos-de-avaliacao.md`.

---

## 12. Diretrizes de design para a personalização do app

| # | Diretriz | Justificativa |
|---|---|---|
| DP01 | **Toda explicação segue o template TWA:** conceito → cena do universo → tabela de mapeamento → **onde a analogia quebra** → versão técnica → pergunta de transferência fora do universo | Glynn [51]; Gentner [50]; sinalização de Mayer [37] |
| DP02 | **Regra da correspondência:** elemento temático sem correspondente no conceito é cortado; nada de imagens temáticas decorativas | Coerência [37]; detalhes sedutores g = −0,33 [41], mais fortes com imagens [40] |
| DP03 | **Termos técnicos antes da analogia** (ou intercalados e sinalizados: "em redes, isso se chama…") | Pré-treino e sinalização [37]; Harp & Mayer sobre detalhes no início [38] |
| DP04 | **Personalização adaptável:** o aluno escolhe universo e nível (nenhum / leve / profundo); o sistema só sugere | Findlater & McGrenere [63]; Amershi G14, G17 [61]; COGA objetivo 8 [14] |
| DP05 | **Explicação literal sempre a um toque** e alternância técnica / analógica / diagrama | COGA 4.4.4 [14]; UDL Representação [64]; Amershi G8 [61] |
| DP06 | **Profundidade combinada ao engajamento:** perguntar quanto o aluno conhece o universo e usar mecânicas reais só para fãs profundos | Walkington & Bernacki [46] |
| DP07 | **Interesses em nível de obra, personagem ou mecânica**, não só categoria | Walkington et al. 2026, PREPRINT [59] |
| DP08 | **Fading:** reduzir a analogia conforme o domínio cresce (sugestão após acertos) | Reversão de expertise [31][32]; Hidi & Renninger [49] |
| DP09 | **Transparência:** rótulo "explicado com base em X porque você marcou…" | Amershi G1, G2, G11 [61]; PAIR [62] |
| DP10 | **Correção granular:** "a analogia ajudou?", "a referência está errada", "trocar universo" | Amershi G9, G15 [61]; erros de realismo [59] |
| DP11 | **Complementar, não substitutivo:** explica e faz andaime; não entrega respostas de exercícios; pede autoexplicação | Bastani [53]; Lehmann (PREPRINT) [55]; Kestin [56] |
| DP12 | **Base técnica curada** (gabarito ou RAG) para o conteúdo de redes | Kestin [56] |
| DP13 | **Segmentação com ritmo do aluno**, progresso visível; áudio com transcrição e controle | Segmentação [37]; informação transitória [31]; COGA 4.3.5 [14] |
| DP14 | **Variar universos** de vez em quando e fechar com a versão neutra | Bolha de filtro e transferência (inferência); transferência tem k = 6 [42] |
| DP15 | **Medir o que importa:** Leppink (IL × EL), Paas por explicação, pós-teste **sem o app** com questão de transferência | Leppink [34]; Paas [33]; Bastani [53]; Lin et al. [42] |
| DP16 | **Privacidade por padrão:** coletar o mínimo, permitir apagar, pseudonimizar antes do LLM, nada de publicidade | LGPD/ANPD [67][68] |
| DP17 | **Atividade generativa opcional:** "crie sua própria analogia" | Mayer, atividade generativa [37]; Duit [52] |
| DP18 | **Sem vieses na sugestão de universos** (nada de inferir por gênero) e tom não infantilizado | Amershi G5, G6 [61]; UDL 7.4 e 2.4 [64] |

**Por que assim:** a evidência diz que interesse ajuda (g = 0,48–0,55 em
retenção e interesse [42]), mas o mesmo mecanismo vira detalhe sedutor se a
analogia decorar em vez de estruturar. DP01–DP03 garantem estrutura, DP04–DP10
devolvem controle ao aluno, DP11–DP12 evitam dependência e alucinação, e
DP13–DP18 cuidam de acessibilidade cognitiva, medição e privacidade.
