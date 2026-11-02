# Materiais da disciplina de IHC (UNIARA) — fichamento

Materiais que o aluno trouxe para a disciplina de Interação Humano-Computador.
Use-os como ponto de partida e vocabulário comum com o professor; complemente
com as referências atualizadas desta biblioteca quando estiverem defasados.

## 1. Slides "Interação Humano-Computador — Semana 1: Fundamentos de Design e a Mudança de Paradigma" (Designing_for_Humans.pdf, 2025)

Ideias centrais da aula, em ordem:

- **O desafio**: a máquina executa a lógica perfeitamente, mas o humano tem
  limitações cognitivas, emocionais e de contexto. "O verdadeiro desafio não é
  fazer o sistema funcionar, é fazer o sistema trabalhar para o humano."
- **O que é IHC**: disciplina que facilita a comunicação entre o humano e os
  sistemas computacionais, aplicando **usabilidade, acessibilidade e
  comunicabilidade**. É a tradução entre o **modelo mental** do usuário
  (cognição, percepção, intenção) e o **modelo do sistema** (código, banco de
  dados, saída).
- **Evolução da interação** (sempre reduzindo carga cognitiva): linha de
  comando (memorizar sintaxe) → manipulação direta/GUI (reconhecer em vez de
  lembrar) → toque/mobile (o dedo substitui o mouse) → ambientes virtuais e
  computação ubíqua (interfaces "invisíveis").
- **Matriz do design**: UI (como isso se parece? layout, tipografia, cores,
  hierarquia), IxD (como isso responde? comandos, estilos interativos,
  feedback), UX (como o usuário se sente? jornada, arquitetura de informação,
  pesquisa).
- **Modelo de cognição**: Percepção → Processamento (alinhar interface ao
  modelo mental; alto risco de sobrecarga) → Ação (mouse, toque, voz). "O
  cérebro não é um disco rígido infinito": atenção e memória de trabalho são
  limitadas.
- **Framework PACT (David Benyon)**: Pessoas, Atividades, Contextos,
  Tecnologias; o cenário de uso ideal está na interseção.
- **Processo de design de IHC** (ciclo contínuo): 1. Entender (necessidades e
  requisitos) → 2. Desenhar (cenários e prototipação) → 3. Avaliar
  (usabilidade e acessibilidade, métodos analíticos e empíricos).
- **Princípios**: "Não me faça pensar" (Steve Krug); Visibilidade, Feedback,
  Consistência.
- **Do abstrato ao concreto**: princípios de IHC (teoria) → diretrizes de
  acessibilidade (ponte testável, ex.: WCAG) → padrões W3C (código, validação,
  semântica). "Princípios guiam a mente do designer; padrões W3C guiam o código
  do engenheiro."
- **Plano do semestre**: Fundamentos → Processo (cenários, prototipação,
  design de interação) → Avaliação e validação (usabilidade, acessibilidade,
  W3C) → Projeto final.
- **Bibliografia básica da disciplina**: Rogers, Sharp & Preece (*Design de
  Interação*); Barbosa & Silva (*Interação Humano-Computador*, engenharia
  semiótica); David Benyon (*Interação Humano-Computador*, PACT); Steve Krug
  (*Não me faça pensar*).
- Fechamento: "O código perfeito é inútil se o usuário falhar." Próxima aula:
  fatores humanos e engenharia semiótica.

**Como usar no projeto**: amarre cada entrega ao vocabulário da aula (PACT nas
personas e cenários; Entender → Desenhar → Avaliar como espinha do relatório;
Visibilidade/Feedback/Consistência na avaliação heurística).

## 2. Artigo Bach, Ferreira, Silveira & Nunes (2009) — "Diretrizes de Acessibilidade: Uma Abordagem Comparativa entre WCAG e e-MAG"

V Simpósio Brasileiro de Sistemas de Informação (SBSI), UNIRIO/UFRJ.
(Os arquivos `2009-sbsi-catharine.pdf` e `diretrizes de acessibilidade .pdf`
são o mesmo artigo.)

- Compara **WCAG 1.0** (W3C/WAI, 1999; 14 diretrizes com pontos de verificação
  e prioridades 1, 2, 3 → conformidade A, AA, AAA) com o **e-MAG 2.0** (2005;
  8 diretrizes, visões Técnica e do Cidadão, mesmos três níveis).
- Contexto legal: Leis 10.048 e 10.098/2000; Decreto 5.296/2004 (prazo para
  acessibilizar sites públicos).
- Método: (a) pesquisa bibliográfica; (b) avaliação automática de 351 URLs
  públicas com o avaliador daSilva em três momentos (nov/2005, mar/2006,
  mar/2007); (c) questionário com 87 organizações; (d) comparação detalhada.
- Resultados: só 22% das organizações estavam adaptadas, 31% em adaptação, 47%
  não adaptadas; 22% desconheciam o decreto; 48% não sabiam que o prazo tinha
  acabado; só 42% conheciam o e-MAG. As recomendações dos dois modelos têm
  poucas diferenças, mas a prioridade de itens equivalentes às vezes difere.
  O e-MAG tinha apenas um validador automático (daSilva), enquanto o WAI
  recomenda ao menos dois.
- Conclusão: quem segue a WCAG atende também ao e-MAG; um padrão único evita
  treinar equipes em dois modelos.

**Atenção — o artigo está defasado**: hoje vigoram a **WCAG 2.2** (princípios
POUR, critérios de sucesso com níveis A/AA/AAA) e o **e-MAG 3.1** (2014), que
**abandonou os níveis A/AA/AAA** e organiza 45 recomendações por seção
(Marcação, Comportamento, Conteúdo/Informação, Apresentação/Design,
Multimídia, Formulário). O validador atual do governo é o ASES. Use o artigo
como contexto histórico e metodológico (é um bom exemplo de avaliação
automática + questionário), não como fonte do estado atual das normas.

## 3. Links trazidos pelo aluno

- **Guia WCAG (guia-wcag.com)** — guia de consulta rápida da WCAG 2.2 em
  português (versão 8.5.1, atualizado em 02/09/2026), com filtros por nível,
  automatização e área responsável, e mapeamento de cada critério para os itens
  da **ABNT NBR 17225**. Melhor ponto de entrada em português para consultar
  um critério específico.
- **e-MAG (emag.governoeletronico.gov.br)** — Modelo de Acessibilidade em
  Governo Eletrônico, versão 3.1 (abril/2014). Contraste mínimo de 4,5:1
  (rec. 4.1), redimensionamento a 200% sem perda (4.3), foco visível com borda
  de pelo menos 2px (4.4), cor não como único meio (4.2), barra de
  acessibilidade com atalhos e alto contraste (cap. 4). Processo em 3 passos:
  padrões web → recomendações → avaliação (automática com ASES, manual e com
  usuários reais).
  - Curiosidade didática: o par de cores que o e-MAG usa como exemplo de
    "4,5:1" (#0000A2 sobre #939393) calcula 4,49:1 pela fórmula da WCAG, ou
    seja, falha por pouco. Sempre meça com ferramenta (veja
    `scripts/contrast_check.py`) em vez de confiar em exemplo.
- **Perkins Brailler (brailler.perkins.org)** — máquina de escrever braille
  mecânica mais usada no mundo desde 1951 (US$ 810 no site). A página da
  Perkins **não informa a contagem de teclas**: o arranjo de 6 teclas de pontos
  (uma por ponto da cela braille) + espaço, retrocesso e avanço de linha é o
  layout padrão da Perkins (conhecimento geral, a confirmar na página do
  fabricante). Campainha que toca 7 espaços antes do fim da linha
  (feedback sonoro no lugar do visual); papel até 11,5 × 14 pol; pesa 4,8 kg;
  pontos seguem o padrão da NLS (altura 0,5 mm, diâmetro 1,4 mm, espaçamento
  2,3 mm, 6 mm entre celas, 10 mm entre linhas).
  - Lição de IHC: feedback multimodal (tátil + sonoro), mapeamento direto
    tecla↔ponto, robustez. A lógica de 6 teclas é a mesma da entrada braille
    em telas sensíveis ao toque (iOS/Android) e em linhas braille.
- **Teclado ampliado adaptado em braille (anúncio do Mercado Livre)** — o
  anúncio não pôde ser aberto pela ferramenta (URL longa demais). O que se
  sabe sobre a categoria está em `acessibilidade.md` (seção de tecnologias
  assistivas); não afirme especificações desse modelo específico sem
  confirmação do aluno.
  - Especificação de referência (compra pública do TRT-9,
    https://www.trt9.jus.br/portal/arquivos/9026477): "teclado padrão ABNT2,
    USB plug and play, teclas ampliadas em alto contraste (amarelo/preto), com
    identificação em braille", compatível com Windows/Linux, garantia de pelo
    menos 12 meses; valor de referência R$ 210,00 por unidade. A especificação
    **não** informa o tamanho das letras.
