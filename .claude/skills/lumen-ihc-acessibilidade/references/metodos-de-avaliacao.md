# Métodos de avaliação — usabilidade, acessibilidade, carga e aprendizagem

Referência para a etapa 4 (Avaliar) do app de estudos personalizado por
interesses. Estado em **28/10/2026**. Os números [n] remetem a `bibliografia.md`.

**Marcadores:** **(a confirmar)** = não conferido na fonte primária;
**(fonte secundária)** = lido em slides, espelho ou resumo; **(inferência)** =
recomendação de Lumen.

## Sumário
1. O que é usabilidade (ISO 9241-11 / 9241-210)
2. Mapa dos métodos: analíticos × empíricos
3. Avaliação heurística (Nielsen + extensões)
4. Percurso cognitivo
5. Engenharia semiótica: MIS e MAC
6. Teste de usabilidade
7. SUS
8. Alternativas e complementos: UMUX-Lite, NASA-TLX, Paas, Leppink
9. Ganho de aprendizagem
10. Avaliação de acessibilidade
11. Ética: CEP, TCLE e LGPD
12. Plano de avaliação recomendado para o app

---

## 1. O que é usabilidade (ISO 9241-11 / 9241-210)

> "extent to which a system, product or service can be used by specified users
> to achieve specified goals with effectiveness, efficiency and satisfaction in a
> specified context of use" — ISO 9241-210:2019, item 3.13, mesma definição da
> ISO 9241-11:2018 [87][86].

| Componente | Métrica típica no teste |
|---|---|
| **Eficácia** | Taxa de sucesso na tarefa, erros graves |
| **Eficiência** | Tempo na tarefa, número de passos e erros |
| **Satisfação** | SEQ por tarefa, SUS ao final |

Os textos literais das definições de eficácia, eficiência e satisfação na ISO
9241-11 (norma paga) não foram lidos (a confirmar). Os 6 princípios e as 4
atividades da ISO 9241-210 estão em `processo-de-design.md`.

---

## 2. Mapa dos métodos: analíticos × empíricos

| Método | Tipo | Quem participa | Melhor para | Seção |
|---|---|---|---|---|
| Avaliação heurística | Analítico (inspeção) | 3–5 avaliadores | Limpar o protótipo antes do teste | 3 |
| Percurso cognitivo | Analítico | Equipe | Primeiro uso / onboarding | 4 |
| MIS | Analítico | Especialista | Comunicabilidade (designer → usuário) | 5 |
| Auditoria WCAG (WCAG-EM) | Analítico + ferramentas | Equipe | Conformidade | 10 |
| Teste de usabilidade (+ MAC) | Empírico | Usuários | Problemas reais, métricas | 6, 5 |
| SUS, SEQ, UMUX-Lite | Questionário | Usuários | Satisfação / percepção | 7, 8 |
| Paas, Leppink, NASA-TLX | Questionário | Usuários | Carga cognitiva / de trabalho | 8 |
| Pré/pós-teste | Empírico | Usuários | Aprendizagem | 9 |

Vocabulário da disciplina: métodos **analíticos** e **empíricos** (slides [1]).

---

## 3. Avaliação heurística (Nielsen + extensões)

### 3.1 As 10 heurísticas de Nielsen
Texto lido no espelho principles.design, que reproduz a NN/g [81] (página da NN/g
não acessada; redação mais recente a confirmar).

| # | Heurística | Essência |
|---|---|---|
| H1 | Visibilidade do status do sistema | Manter o usuário informado com feedback em tempo razoável |
| H2 | Correspondência com o mundo real | Falar a língua do usuário; convenções do mundo real |
| H3 | Controle e liberdade | "Saída de emergência" clara; desfazer e refazer |
| H4 | Consistência e padrões | Mesmas palavras e ações significam o mesmo; seguir a plataforma |
| H5 | Prevenção de erros | Evitar o problema é melhor que boa mensagem de erro |
| H6 | Reconhecer em vez de lembrar | Minimizar a carga de memória com opções visíveis |
| H7 | Flexibilidade e eficiência | Aceleradores para experientes; personalizar ações frequentes |
| H8 | Design estético e minimalista | Sem informação irrelevante ou raramente necessária |
| H9 | Reconhecer, diagnosticar e recuperar erros | Linguagem simples, problema preciso, solução sugerida |
| H10 | Ajuda e documentação | Fácil de buscar, focada na tarefa, concisa |

Nielsen publicou uma releitura no Substack ("The 10 Usability Heuristics
Reimagined"), não lida (a confirmar).

### 3.2 Severidade (0–4) [82]

| Nota | Significado |
|---|---|
| 0 | Não é problema de usabilidade |
| 1 | Cosmético: corrigir só se sobrar tempo |
| 2 | Menor: baixa prioridade |
| 3 | Maior: importante, alta prioridade |
| 4 | Catástrofe: corrigir antes de lançar |

Fatores: **frequência, impacto e persistência**.

### 3.3 Processo [83] (fonte secundária)
- **3 a 5 avaliadores independentes**. Um encontra ≈ **35%** dos problemas; cinco,
  ≈ **75%**; acima de ~5, retornos decrescentes (Nielsen, 1994; a confirmar no original).
- Fases: (1) treinamento (domínio e cenários); (2) avaliação individual em **≥ 2
  passadas** (fluxo geral, depois elementos); (3) severidade individual e depois
  consolidada; (4) debriefing.
- Planilha pronta: `assets/templates/avaliacao-heuristica.md`.

### 3.4 Conjuntos complementares
| Conjunto | Itens | Uso no app |
|---|---|---|
| **8 Regras de Ouro de Shneiderman** [84] | Consistência; usabilidade universal; feedback informativo; diálogos com fechamento; prevenir erros; reversão fácil; usuário no controle; reduzir carga de memória de curto prazo | "Usabilidade universal" amarra a acessibilidade |
| **Norman (2013)** [85] | Princípios do cap. 1: affordances, signifiers, mapping, feedback, conceptual models; constraints (físicas, culturais, semânticas, lógicas) no cap. 4 | Signifiers dos botões de analogia; modelo conceitual "explicação técnica + camada de analogia" |
| **Amershi et al. (2019), 18 diretrizes** [61] | Ver `carga-cognitiva-e-personalizacao.md` §7 | Mais críticas: G1, G2, G9, G10, G11 |
| **COGA, 8 objetivos** [14] | Ver `acessibilidade.md` §6.1 | Objetivos 5 (foco) e 6 (memória) como heurísticas extras. A seção 5 do COGA recomenda envolver pessoas com deficiências cognitivas |

Não existe conjunto de heurísticas para IA generativa amplamente validado além de
Amershi et al. (lacuna).

**Implicação para o app:** a planilha usa H1–H10 + A1 (baixa visão) + C1 (carga
cognitiva) + IA1 (transparência da IA). Os mesmos 3–5 avaliadores percorrem as
tarefas T1–T5 do teste.

---

## 4. Percurso cognitivo (cognitive walkthrough)

Wharton, Rieman, Lewis & Polson (1994) [91] (fonte secundária). Para cada passo
da tarefa:
1. O usuário tentará atingir o efeito que o passo produz?
2. Perceberá que a ação correta está disponível?
3. Entenderá que essa ação leva ao efeito desejado?
4. Receberá feedback adequado de que acertou?

A versão "streamlined" de Spencer (CHI 2000) usa 2 perguntas, cujo texto exato
não foi confirmado (a confirmar).

**Implicação para o app:** percorra o **onboarding de interesses** (T1) e o
primeiro pedido de explicação (T2) com as 4 perguntas, de preferência no papel de
uma persona com baixa visão a 400% de zoom.

---

## 5. Engenharia semiótica: MIS e MAC

A interface é uma **metamensagem do designer ao usuário** (de Souza, 2005 [92];
conceito descrito em Barbosa & Silva, 2010 [114]; a confirmar).

### 5.1 MIS — Método de Inspeção Semiótica [93]
Passos: (1) signos **metalinguísticos** (ajuda, dicas); (2) signos **estáticos**
(botões, menus, textos); (3) signos **dinâmicos** (interação entre estados);
(4) comparação das 3 metamensagens reconstruídas; (5) avaliação global da
comunicabilidade. Dispensa usuários; pode complementar ou substituir a heurística.

### 5.2 MAC — Método de Avaliação de Comunicabilidade [94]
Passos: tarefas predefinidas → gravação de tela + notas → entrevista opcional →
**etiquetagem** → **interpretação** → **perfil semiótico**.

| Etiqueta | Significado | Classe |
|---|---|---|
| Cadê? | Procura uma função que sabe existir | Navegação |
| E agora? | Não sabe o que fazer em seguida | Navegação |
| O que é isto? | Tenta entender um elemento | Atribuição de significado |
| Epa! | Faz algo sem querer e desfaz logo | Navegação/significado |
| Onde estou? | Age no contexto errado | Navegação/significado |
| Assim não dá. | Abandona um subplano inteiro | Navegação/significado |
| Por que não funciona? | Repete uma ação que falha | Significado |
| Ué, o que houve? | Não percebe o feedback | Significado |
| Para mim está bom... | Acha que concluiu, mas não concluiu | Significado |
| Desisto. | Abandona a tarefa | Falha na execução |
| Vai de outro jeito. | Não percebe a solução principal e usa caminho mais complexo | Incompreensão da affordance |
| Não, obrigado. | Conhece a solução principal, mas prefere outra | Recusa da affordance |
| Socorro! | Recorre à ajuda | Qualquer problema |

A ligação das etiquetas às falhas "completa / temporária / parcial" de Barbosa &
Silva (2010) não foi confirmada (a confirmar).

**Implicação para o app:** reaproveite as gravações do teste de usabilidade para
etiquetar com o MAC. Isso economiza sessões e conversa com a bibliografia da
disciplina (engenharia semiótica). "Ué, o que houve?" é a etiqueta a observar
quando a explicação do LLM é gerada sem anúncio para quem usa ampliação.

---

## 6. Teste de usabilidade

### 6.1 Quantos participantes

| Posição | Dado |
|---|---|
| **Nielsen & Landauer (1993)** [88] | Problemas encontrados = `N · (1 − (1 − L)^n)`, L ≈ 31%. **5 usuários ≈ 85%**. Melhor: 15 usuários em 3 rodadas de 5, com redesign entre elas. 2 grupos distintos → 3–4 por grupo; 3+ grupos → ≥ 3 por grupo; nunca 1 |
| **Faulkner (2003)** [89] | Com 5 usuários, média de 85%, mas variação de quase 100% até **55%**. Com 10: média 95%, mínimo 82% |
| **Uso correto (inferência)** | 5 por rodada vale para **descobrir problemas** (formativo) em público homogêneo. Para **estimar métricas** (somativo) são precisas dezenas. O relatório deve dizer qual é o objetivo |

### 6.2 Protocolo (inferência baseada em [29][90])
1. TCLE (seção 11).
2. Questionário de perfil curto.
3. Tarefa de prática.
4. 4–6 tarefas realistas com **critério de sucesso definido antes**.
5. **Think-aloud concorrente**, teste **moderado**. O W3C recomenda think-aloud
   com alta interação do facilitador em testes com pessoas com deficiência [29].
6. **SEQ** após cada tarefa.
7. **SUS** ao final.
8. Entrevista curta (debrief).

Roteiro pronto: `assets/templates/protocolo-teste-usabilidade.md`.

Observações (inferência): o think-aloud concorrente altera o tempo; se o tempo
for métrica central, use think-aloud retrospectivo com gravação ou sessões
separadas. O teste remoto não moderado é barato, mas perde as sondagens; com n
pequeno, o moderado é mais seguro. Não há referência primária verificada
comparando concorrente e retrospectivo (lacuna).

### 6.3 Métricas por tarefa

| Métrica | Como registrar | Como resumir (inferência / prática de UX) |
|---|---|---|
| Sucesso | 1 / 0,5 (parcial) / 0, por critério definido antes | Taxa com **IC de Wilson ajustado** |
| Tempo | Do "pode começar" ao critério de sucesso | **Média geométrica** em amostras pequenas |
| Erros | Contagem + descrição | Por tarefa e por tipo |
| **SEQ** | "No geral, quão difícil ou fácil foi completar esta tarefa?", 7 pontos | Média; perguntar "por quê?" se < 5 |
| Etiquetas MAC | Durante a análise da gravação | Frequência por tarefa |

**SEQ** [90]: pergunta original "Overall, how difficult or easy was the task to
complete?", 7 pontos com extremos rotulados, logo após a tarefa. Média histórica
≈ **5,3–5,6** (> 400 tarefas, > 10.000 usuários; atualização de mai/2019).
Correlação com tempo e sucesso r ≈ 0,5. Em ≈ 14% dos casos quem **falhou** avaliou
a tarefa como extremamente fácil, por isso observe o comportamento, não só a nota.
A tradução para o português usada no protocolo é da skill, não validada (a confirmar).

O benchmark de ≈ 78% de taxa de conclusão citado pela MeasuringU não foi
confirmado (a confirmar).

---

## 7. SUS (System Usability Scale)

### 7.1 Origem e itens
Brooke (1996), "quick and dirty", baseado em dados de 20 pessoas, com 10 itens
escolhidos de 50 [70][71]. Respondeu por 43% do uso de questionários pós-teste
num estudo industrial [71].

| # | Original [70] | PT-BR — Lourenço, Carmona & Lopes (2022) [77] |
|---|---|---|
| 1 | I think that I would like to use this system frequently. | Eu acho que gostaria de usar esse sistema frequentemente. |
| 2 | I found the system unnecessarily complex. | Eu achei esse sistema desnecessariamente complexo. |
| 3 | I thought the system was easy to use. | Eu achei esse sistema fácil de usar. |
| 4 | I think that I would need the support of a technical person to be able to use this system. | Eu achei que precisaria de ajuda de uma pessoa técnica para ser capaz de usar esse sistema. |
| 5 | I found the various functions in this system well-integrated. | Eu achei que as várias funções desse sistema foram bem integradas. |
| 6 | I thought there was too much inconsistency in this system. | Eu acho que o sistema apresenta muita inconsistência. |
| 7 | I would imagine that most people would learn to use this system very quickly. | Eu imagino que a maioria das pessoas pode aprender a usar esse sistema rapidamente.* |
| 8 | I found the system very cumbersome to use. | Eu achei esse sistema muito pesado para usar. |
| 9 | I felt very confident using the system. | Eu me senti muito seguro usando o sistema. |
| 10 | I needed to learn a lot of things before I could get going with this system. | Eu precisei aprender muitas coisas antes que pudesse utilizar esse sistema. |

\* Item 7: a Tabela 1 do artigo omite "muito"; o texto de Resultados diz "muito
rapidamente". Escolha uma forma, use-a com todos e declare a escolha.

**Versão PT-BR:** *Aquichan* 22(2):e2228, 2022, **DOI 10.5294/aqui.2022.22.2.8**.
Pré-teste com n = 100 universitários (61 de Enfermagem, 39 de Análise de Sistemas,
17–45 anos, média 22,68), avaliando o WhatsApp; **α de Cronbach = 0,76**. Escala de
5 pontos, de 1 = discordo totalmente a 5 = concordo totalmente. A redação exata das
âncoras em português não aparece no texto lido (a confirmar) [77].

Finstad (2006) [79]: não nativos tiveram dificuldade com "cumbersome" (item 8);
sugeriu "awkward". Na versão PT-BR, "muito pesado" pode merecer atenção no
pré-teste (inferência).

Modelo pronto: `assets/templates/sus-ptbr.md`.

### 7.2 Pontuação [71]
```
SUS = 2,5 × [ Σ ímpares (x − 1) + Σ pares (5 − x) ]   → 0 a 100
```
O escore **não é percentual**: 70 é perto da média (≈ percentil 50), não "70%" [80].
Script: `python3 scripts/sus_calculator.py respostas.csv`.

### 7.3 Interpretação
- **Média 68 = percentil 50**, normas com > 10.000 respostas de centenas de
  produtos [75]. Atribuir o 68 a Sauro (2011) não foi verificado no texto primário
  (a confirmar).
- **Escala curva Sauro-Lewis (2016; 241 estudos industriais)** [75][71]:

| Nota | Faixa SUS | Percentil |
|---|---|---|
| A+ | 84,1–100 | 96–100 |
| A | 80,8–84,0 | 90–95 |
| A− | 78,9–80,7 | 85–89 |
| B+ | 77,2–78,8 | 80–84 |
| B | 74,1–77,1 | 70–79 |
| B− | 72,6–74,0 | 65–69 |
| C+ | 71,1–72,5 | 60–64 |
| C | 65,0–71,0 | 41–59 |
| C− | 62,7–64,9 | 35–40 |
| D | 51,7–62,6 | 15–34 |
| F | 0–51,6 | 0–14 |

68 é o centro do C; 80 é A−; "80 é uma meta industrial comum" [71].

- **Adjetivos de Bangor, Kortum & Miller (2009)** [73]: 11º item de 7 pontos;
  n = 959; r = 0,822 com o SUS.

| Adjetivo | n | Média SUS | DP |
|---|---|---|---|
| Worst Imaginable (pior imaginável) | 4 | 12,5 | 13,1 |
| Awful (horrível) | 22 | 20,3 | 11,3 |
| Poor (ruim) | 72 | 35,7 | 12,6 |
| OK | 211 | 50,9 | 13,8 |
| Good (bom) | 345 | 71,4 | 11,6 |
| Excellent (excelente) | 289 | 85,5 | 10,4 |
| Best Imaginable (melhor imaginável) | 16 | 90,9 | 13,4 |

São **médias** por adjetivo, não cortes. "OK" é problemático; a MeasuringU sugere
"Fair" para ~51–62 [75].

- **Aceitabilidade** (Bangor et al., 2008) [74][75]: aceitável > ~70; marginal 50–70;
  inaceitável < 50. Escala absoluta de Bangor (2009): F < 60, D 60–69, C 70–79,
  B 80–89, A ≥ 90 [71]. Não confunda com a curva Sauro-Lewis.
- **Benchmarks por item** [71] (166 estudos, 11.855 questionários): item 3 ≈ 3,67
  para SUS 68 e ≥ 4,24 para SUS 80; item 9 = 4,25 para SUS 80.
- **NPS** [75]: promotores ≈ 81, neutros ≈ 70, detratores ≤ 53 (R² = 42%).

### 7.4 Confiabilidade e estrutura
- α ≈ 0,90 ou mais no original [71]; r = 0,806 com item de "user-friendliness" [71].
  Sensível a diferenças entre interfaces e ao sucesso na tarefa [71].
- **Lewis & Sauro (2017)** [72]: 9.156 questionários de 112 estudos. A divisão
  Usability (todos menos 4 e 10) × Learnability (4 e 10) de 2009 não se replicou;
  o melhor ajuste foi tom positivo/negativo (CFI = 0,958, RMSEA ≈ 0,088). O SUS é
  "bidimensional, mas não de forma interessante ou útil". **Reporte só o escore
  global.**

> Nota sobre o script: `sus_calculator.py` ainda imprime as subescalas
> Usabilidade/Aprendizibilidade. Siga Lewis & Sauro (2017): não as use como
> resultado principal.

### 7.5 Tamanho de amostra e intervalo de confiança [76]
`n = (s · t / d)²`, com d = margem desejada e t ≈ 2 para 95%.

| DP (s) | n para ±5 pontos |
|---|---|
| 16,8 (software de negócios) | ≈ 46 |
| 17,6 (software de consumo) | ≈ 50 |
| 20 | 64 |
| 21,4 (média das fontes) | ≈ 74 |
| 22,5 | 81 |

Infle o DP em 5–10% se for incerto. DP do SUS varia de ≈ 16,8 a 22,5 [76].

- Tullis & Stetson (2004) [80]: com ~6 usuários nenhum questionário foi preciso; o
  SUS ficou no meio do grupo. O dado de "12–14 participantes" frequentemente citado
  não foi confirmado (a confirmar).
- **Implicação para o app (inferência):** com n ≈ 10–20, a margem fica em ≈ ±9 a
  ±13 pontos (s ≈ 20). Apresente o SUS como **indicador complementar**, com média,
  IC 95%, nota na curva e percentil. Para afirmar "acima de 68" com rigor seria
  preciso n ≈ 50 ou mais.

### 7.6 Cuidados
- A alternância de tom (itens positivos e negativos) gera erros: confira
  inversões aparentes (ex.: 5 no item 3 e 5 no item 2) [inferência].
- O SUS mostra **quanto**, não **por quê**: combine com think-aloud, taxa de
  sucesso e heurística.

---

## 8. Alternativas e complementos

### 8.1 UMUX-Lite [78]
- 2 itens: "[This system's] capabilities meet my requirements." e "[This system]
  is easy to use." Original de 7 pontos; a MeasuringU usa variante de 5.
- Conversão para escala SUS (versão de 7 pontos):
  `SUS ≈ 0,65 × [(Item1 + Item2 − 2) × (100/12)] + 22,9`.
- r = 0,83 com o SUS; r = 0,72 com NPS; α = 0,86 (SUS 0,91). Borsci et al. (2015)
  confirmaram a regressão com erro ≈ 1%.
- A conversão para a variante de 5 pontos não é publicada (a confirmar). Não há
  tradução PT-BR validada nas notas.

**Uso no app (inferência):** UMUX-Lite cabe **dentro do app**, depois de várias
sessões; o SUS fica no teste formal.

### 8.2 NASA-TLX e Raw TLX [35][36]
- 6 subescalas (exigência mental, física, temporal; desempenho; esforço;
  frustração), cada uma de 0 a 100 em passos de 5 (21 valores); ponderação com 15
  comparações pareadas.
- **Raw TLX**: sem ponderação, média ou soma. Em 29 estudos foi mais, menos ou
  igualmente sensível que o ponderado: "you can take your pick" [36]. Mais simples
  para amostras pequenas (inferência).
- Tradução PT-BR validada não verificada (a confirmar).

### 8.3 Escala de Paas [33]
1 item, 9 pontos, de "very, very low mental effort" (1) a "very, very high mental
effort" (9); teste-reteste r = 0,90. Enunciado exato e tradução validada: a confirmar.

### 8.4 Leppink et al. (2013) [34]
10 itens, 0–10: IL (1–3), EL (4–6), GL (7–10). Separa intrínseca de extrínseca e
testa a hipótese central do app. Detalhes em `carga-cognitiva-e-personalizacao.md` §2.

---

## 9. Ganho de aprendizagem

- **Ganho normalizado de Hake (1998)** [69], *American Journal of Physics*
  66(1):64–74. Limiares: **baixo < 0,3; médio 0,3–0,7; alto > 0,7**.
- Fórmula usual: `g = (pós − pré) / (100 − pré)`, com notas em %. É a forma comum
  na literatura, mas **não estava escrita na página verificada** (a confirmar no
  texto primário).

**Desenho sugerido (inferência):** pré-teste de 5–10 questões → sessão com o app →
Paas após cada explicação (ou Raw TLX ao final) → SUS → pós-teste em **forma
paralela** (para evitar efeito de memória), **sem acesso ao app** e com pelo menos
uma questão de **transferência** fora do universo temático (Bastani [53]; Lin et
al. [42]). Sem grupo controle, o ganho não pode ser atribuído causalmente ao app:
declare isso. Uma comparação possível dentro do sujeito é "explicação analógica ×
neutra" em tópicos diferentes, com ordem contrabalançada.

---

## 10. Avaliação de acessibilidade

### 10.1 WCAG-EM 2.0 [28]
**W3C Group Note de 23/07/2026** (Draft de 05/02/2026; substitui o WCAG-EM 1.0 de
2014). Alvo: WCAG 2, com exemplos em WCAG 2.2.

| Passo | Conteúdo |
|---|---|
| 1. Definir o escopo | Produto, nível de conformidade, baseline de suporte de acessibilidade, requisitos adicionais |
| 2. Explorar o produto | Visões comuns, funcionalidades essenciais, tipos de amostra, tecnologias |
| 3. Selecionar amostra | **Amostra estruturada + amostra aleatória (10% da estruturada)** + processos completos (fluxo padrão e ramos críticos) |
| 4. Avaliar | Amostras, processos completos; comparar estruturada × aleatória |
| 5. Reportar | Resultados obrigatórios; opcional: detalhes, declaração, escore agregado, EARL |

Avaliar o produto inteiro é preferível quando viável. Por avaliar amostra, o método
sozinho não permite declarar conformidade do site inteiro [28].

### 10.2 Testes manuais (prática consolidada; protocolos detalhados como o "Easy Checks" do W3C não foram lidos — a confirmar)

| Teste | Como | Critérios |
|---|---|---|
| Só teclado | Tab/Shift+Tab/Enter/Espaço/Esc em todos os fluxos: ordem lógica, foco visível, sem armadilha, foco não coberto | 2.1.1, 2.4.3, 2.4.7, 2.4.11 |
| Zoom 200% | Ctrl + no navegador; fonte do SO a 200% | 1.4.4 |
| Reflow 400% | Janela de 1280 px a 400% = 320 CSS px; sem rolagem horizontal [30] | 1.4.10 |
| Espaçamento | Bookmarklet de text spacing | 1.4.12 |
| Contraste | `contrast_check.py` em todos os pares de token e estados | 1.4.3, 1.4.11 |
| Leitor de tela | NVDA (Windows), TalkBack (Android), VoiceOver (iOS/macOS) nos fluxos completos: títulos, nomes, estados, anúncio da explicação gerada | 1.3.1, 4.1.2, 4.1.3 |
| Temas do SO | `forced-colors` e `prefers-contrast` ligados | boa prática |

Checklist pronto: `assets/templates/checklist-baixa-visao.md`. Limites da automação
(GOV.UK, Deque, WebAIM): `acessibilidade.md` §9.

### 10.3 Envolvendo usuários com deficiência (W3C WAI, 30/04/2024) [29]
- Revelam problemas que a checagem de conformidade não pega.
- "Alguns" participantes, sem número fixo; experiência com TA compatível com o
  público-alvo.
- **Não generalizar** de 1 pessoa para toda uma deficiência; não tratar estudo
  pequeno como estatisticamente significativo.
- Relatório declara escopo, métodos e perfil dos participantes.
- **O teste com usuários não determina conformidade**; combine com avaliação WCAG.
- Corrija barreiras óbvias **antes** das sessões; avaliações informais contínuas
  valem mais que um único teste formal no fim.
- Think-aloud com alta interação do facilitador.

**Implicação para o app (inferência):** cada participante com baixa visão usa **o
próprio dispositivo e a própria TA** (lupa, zoom, contraste, leitor de tela), já
configurados como no dia a dia. Relate as sessões como achados **qualitativos**.
Recrutamento respeitoso: `processo-de-design.md` §2.5.

---

## 11. Ética: CEP, TCLE e LGPD

### 11.1 Precisa de CEP?
- **Res. CNS 510/2016** [95], art. 1º, parágrafo único: não passam pelo CEP, entre
  outros, I) pesquisa de opinião pública com participantes não identificados;
  V) bancos agregados sem identificação; VI) revisão de literatura; **VIII)
  atividade exclusivamente de educação, ensino ou treinamento, sem finalidade de
  pesquisa científica**.
- **Ofício Circular nº 17/2022/CONEP (05/07/2022)** [96]: **TCCs, monografias e
  similares NÃO se enquadram no inciso VIII**. Se uma atividade de ensino tiver
  resultados incorporados a uma pesquisa, a submissão passa a ser obrigatória.
  Mesmo com dispensa, a instituição pode exigir análise ética.

| Situação | Caminho (inferência a partir de [95][96]) |
|---|---|
| Teste só como exercício da disciplina, sem publicação nem uso em TCC | Pode caber no inciso VIII. **Confirme com o professor** |
| Os dados vão para TCC, artigo ou apresentação em evento | Submeter ao CEP (Plataforma Brasil) **antes** da coleta |
| SUS anônimo e aberto (sem nome, e-mail ou IP) | Aproxima-se do inciso I |
| SUS respondido depois de sessão gravada | Identificável → CEP |

Esse é o risco mais comum para equipes de alunos: começar como exercício e depois
querer usar no TCC. O texto da Res. CNS 674/2022 não foi verificado (a confirmar).

### 11.2 Conteúdo do TCLE / registro de consentimento [95]
- Consentimento "livre de simulação, fraude, erro ou intimidação" (art. 2º); o
  registro pode ser escrito, sonoro, em imagem ou digital (arts. 2º e 15), sempre em
  linguagem clara.
- **Art. 17, o registro contém:** justificativa; objetivos; procedimentos; riscos e
  medidas de proteção; sigilo; acesso aos resultados; ressarcimento; contatos do
  pesquisador e do CEP; liberdade de recusar ou retirar o consentimento sem
  penalidade.
- Art. 9º: direito a **ressarcimento** de despesas e **indenização** por danos.
  Art. 21: risco **mínimo, baixo, moderado ou elevado**.
- **Acessível:** TCLE em HTML ou DOCX bem estruturado, compatível com leitor de
  tela e zoom; oferecer leitura em voz alta; registro de consentimento em áudio é
  admitido (art. 15) [103][95].

### 11.3 LGPD na pesquisa acadêmica [68]
- Art. 4º, II, "b": não se aplica a fins **exclusivamente** acadêmicos, **mas os
  arts. 7º e 11 continuam valendo** (interpretação restritiva; guia ANPD v1.0,
  jun/2023, lido via resumo institucional).
- "Órgão de pesquisa" (art. 5º, XVIII) é órgão público ou pessoa jurídica **sem fins
  lucrativos**. Com essa qualificação, os arts. 7º, IV, e 11, II, "c" permitem
  tratar dados sem consentimento, com anonimização "sempre que possível". A natureza
  jurídica da UNIARA não foi verificada (a confirmar); se houver dúvida, use
  **consentimento** como base.
- Boas práticas: consentimento específico; minimização (faixa etária em vez de data
  de nascimento); códigos P01, P02…; gravações em drive institucional com acesso
  restrito; prazo de descarte no TCLE; não usar transcrição que treine modelos com
  os dados; **informação sobre deficiência é dado sensível** (art. 11).

---

## 12. Plano de avaliação recomendado para o app

| Fase | O quê | Quem / n | Instrumentos | Saída |
|---|---|---|---|---|
| 0. Ética | Verificar com o professor: exercício ou TCC? Se TCC → CEP antes de tudo. Preparar TCLE acessível | Equipe | Res. 510/2016, Ofício 17/2022 [95][96] | TCLE, aprovação ou dispensa documentada |
| 1. Inspeção | **Avaliação heurística** (H1–H10 + A1, C1, IA1) e **percurso cognitivo** do onboarding | 3–5 avaliadores independentes, ≥ 2 passadas | `avaliacao-heuristica.md`, severidade 0–4 | Lista consolidada com severidade média |
| 2. Auditoria | Automático (axe/Lighthouse) + checklist manual (teclado, 200%, 400%/320 px, espaçamento, leitor de tela) | Equipe | `checklist-baixa-visao.md`, `contrast_check.py`, WCAG-EM simplificado | Barreiras óbvias identificadas |
| 3. Correções | Corrigir severidade 3–4 e todas as barreiras de acessibilidade óbvias **antes** das sessões [29] | Equipe | — | Protótipo v2 + registro de mudanças |
| 4. Teste moderado | 5 tarefas (T1–T5), think-aloud, SEQ após cada uma, SUS ao final, Leppink após T2–T3, debrief | **5–8 participantes**, incluindo **≥ 1 pessoa com baixa visão** usando a própria TA (ideal: 2–3) | `protocolo-teste-usabilidade.md`, `sus-ptbr.md` | Gravações, notas, CSVs |
| 5. (Opcional) Aprendizagem | Pré-teste → sessão → pós-teste sem o app com questão de transferência | Mesmos participantes | Hake [69] | Ganho normalizado (sem atribuição causal) |
| 6. Análise | Sucesso (IC de Wilson), tempo (média geométrica), erros, SEQ por tarefa; SUS global com IC 95%, curva e percentil; Leppink IL × EL; etiquetagem MAC das gravações; problemas priorizados por severidade | Equipe | `sus_calculator.py` | `resultados.md` |
| 7. Iteração | Redesign e, se houver tempo, segunda rodada curta | 3–5 participantes | — | `melhorias.md` com rastreabilidade |

**Como reportar (inferência):**
- Declare o objetivo **formativo** (achar problemas) e o n.
- SUS como indicador complementar: "SUS médio = X (IC 95% Y–Z; nota C+ na curva
  Sauro-Lewis; n = 7)", sem subescalas [72].
- Achados de participantes com baixa visão relatados como **qualitativos**, sem
  generalizar para "pessoas com baixa visão" [29].
- Diga que ferramentas automáticas pegam só parte dos problemas [25][26].
- Rastreabilidade: problema → heurística/critério → mudança no protótipo.

**Por que assim:** a inspeção barata vem primeiro para que o tempo com usuários
reais (o recurso mais escasso, especialmente com baixa visão) seja gasto com
problemas que só eles revelam. SEQ, SUS e Leppink cobrem tarefa, produto e
aprendizagem, e o think-aloud explica o porquê de cada número.
