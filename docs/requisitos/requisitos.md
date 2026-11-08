# Requisitos

Formato: história de usuário + critérios de aceite (Dado/Quando/Então) +
rastreio até a pesquisa e o teste. Os achados referem-se à seção 4 de
`etapa-1-pesquisa/sintese.docx`; as personas e os cenários, à pasta `etapa-2-personas-cenarios/`. Prioridade MoSCoW (Must/Should/Could/Won't).
Requisitos de acessibilidade e personalização vêm do Lumen (códigos RA e DP).

## Funcionais
| ID | História | Prioridade | Rastreio | Teste automatizado |
|---|---|---|---|---|
| RF01 | Como aluno, quero começar sem criar conta com nome e e-mail, para não perder tempo nem expor dados | Must | LGPD art. 6º, III (minimização) → todas as personas · [hipótese da equipe] | `test_api.py::test_health` + e2e |
| RF02 | Como aluno, quero dizer no chat, com minhas palavras, o universo que conheço (D7) | Must | Achado 4 (itens 7 e 8; média 4,8) → Rafael, Caio | `test_interest_requires_consent` |
| RF03 | Como aluno, quero escrever no chat o assunto que quero entender e receber a explicação usando meu universo, em passos curtos (D7) | Must | Achado 2 (item 6: abstração 4 de 5) e achado 6 (item 14) → Ana, Rafael · Cenários 1 e 2 | e2e `fluxo-principal` |
| RF04 | Como aluno, quero que a explicação comece com a analogia e que um botão mostre a versão técnica (sem analogia), e volte, sem perder o ponto em que eu estava | Must | Achado 3 (item 11: maior média, 4,0; R01) → Rafael, Caio · DP05 · Cenários 2 e 3 · DD03 | e2e `T3`; unidade `passos.test.ts` |
| RF05 | Como aluno, quero avisar que uma explicação está errada ou confusa | Should | Achado 4 (item 12: 3 de 5) → Rafael · DP10 · Cenário 2 | `test_wrong_feedback_...` |
| RF06 | Como aluno com baixa visão, quero aumentar o texto e usar alto contraste no app | Must | Achado 5 (item 13: 4 de 5 ajustam a leitura) → Ana [da literatura], Rafael · Cenário 1 | e2e `texto ampliado...` |
| RF07 | Como aluno, quero ver e apagar meus dados | Must | LGPD art. 18 → todas as personas | `test_delete_me_erases_everything` |
| RF08 | Como aluno que prefere linguagem técnica, quero definir a explicação sem analogia como padrão | Won't (nesta versão) | Achado 3 (R01: item 9 = 1; item 11 = 5) → Caio · Cenário 3. Substituído pela decisão D2: o app sempre começa pela analogia; decisão da equipe: Caio é atendido pelo botão de alternar do RF04. Observar no teste de usabilidade se o perfil cético aceita o clique extra | — |
| RF09 | Como aluno, quero trocar de universo sem sair da explicação, para comparar analogias ou corrigir uma escolha ruim | Must | Decisão D4 · Achado 4 (universos variados) → Rafael · divergência 3 da seção 6 dos Cenários · DD04 | `test_api.py::test_troca_de_universo_guarda_uma_explicacao_por_interesse` + e2e |
| RF10 | Como aluno, quero conversar com o app numa interface de chat, recebendo a explicação em mensagens curtas, uma etapa por vez | Must | Decisão D3 · PACT conclusão 1 (blocos curtos e retomáveis) · Achado 6 (item 14: cansaço com texto longo, 4 de 5) → Ana, Rafael · divergência 1 da seção 6 dos Cenários · DD02 | e2e `T2` + `acessibilidade-chat.spec.ts` (sem API: uma etapa por mensagem é apresentação) |
| RF11 | Como aluno, quero digitar perguntas livremente no chat e receber resposta somente dentro do conceito que estou estudando | Must | Decisão D5 · RNF04 (correção do conteúdo) · Achado 4 (item 12: 3 de 5 perderiam a confiança diante de um erro) → todas as personas · DD05, DD06 | `test_questions.py` (20 testes) + e2e |

### Exemplo de critérios de aceite (RF03)
```gherkin
Cenário: explicação personalizada verificada
  Dado que aceitei o termo e informei o interesse "futebol"
  Quando peço a explicação de "Entrega confiável no TCP"
  Então vejo os passos: conceito, cena, quem é quem, onde a comparação falha,
        explicação técnica e uma pergunta para testar
  E a mensagem "Explicação pronta." é anunciada pelo leitor de tela (WCAG 4.1.3)

Cenário: explicação reprovada na verificação
  Dado que informei o interesse "xadrez"
  Quando peço a explicação de "Entrega confiável no TCP"
  Então vejo a explicação padrão e um aviso explicando o motivo
```

## Não funcionais (ISO/IEC 25010:2023)
| ID | Característica | Requisito | Verificação |
|---|---|---|---|
| RNF01 | Capacidade de interação (inclusividade) | WCAG 2.2 AA; sem rolagem lateral a 320px com texto 2x | axe + `acessibilidade-chat.spec.ts` (região viva, foco, alvo 24×24, reflow) + checklist manual do Lumen |
| RNF02 | Segurança | Chave da IA só no back-end; banco sem porta exposta; sessão por token com hash | revisão de código |
| RNF03 | Confiabilidade | Falha ou recusa da IA → explicação padrão | `test_llm_*` |
| RNF04 | Correção do conteúdo | Nenhuma resposta é exibida sem passar pela autoverificação da IA (D6) e pelos validadores automáticos; reprovada → nova tentativa ou explicação padrão | `test_grounding.py` + `test_verification.py` (12 testes, incluindo o contrato de que a checagem não vê o rascunho) + taxa de erro medida no teste de usabilidade |
| RNF05 | Privacidade (LGPD) | Minimização, consentimento, exportação e exclusão | testes de API |
| RNF06 | Flexibilidade | Sobe com `docker compose up`; troca de provedor de IA por variável | CI |
| RNF07 | Capacidade de interação (adaptabilidade) | Aplicação web responsiva: a mesma interface funciona no celular (a partir de 320px) e no computador, sem app nativo | e2e nos dois projetos do Playwright, `celular` e `desktop` |

## Decisões de projeto (07/11/2026, antes da Etapa 3)

| ID | Decisão | Requisitos afetados |
|---|---|---|
| D1 | O app é uma aplicação **web responsiva**, para celular e computador | RNF07, RNF01 |
| D2 | A explicação **começa sempre com a analogia**; um botão alterna para a versão técnica | RF04 (alterado), RF08 (adiado) |
| D3 | A interface segue o modelo de **chat das sessões de IA** | RF10 (novo) |
| D4 | É possível **trocar de universo de dentro da explicação** | RF09 (novo) |
| D5 | O chat **aceita texto livre, mas responde só dentro do conceito** escolhido; fora dele, recusa com educação e oferece opções | RF11 (novo), RNF04 |
| D6 | Não há revisão humana: a **própria IA verifica a resposta antes de exibi-la** (autoverificação), seguida dos validadores automáticos | RNF04, RF03, RF11 |
| D7 | **Tudo dentro do chat**: o aluno escreve o assunto e o universo com as próprias palavras; o assunto é reconhecido na biblioteca de conteúdos (com material de referência) e, fora dela, o app diz que ainda não tem material e sugere o que tem | RF02, RF03, RF10, RNF04 |

### Cuidados de acessibilidade para a interface de chat (Lumen)
- Histórico de mensagens com `role="log"` (anúncio educado ao leitor de tela); anunciar a mensagem pronta, não cada pedaço do texto enquanto é gerado (WCAG 4.1.3).
- Não mover o foco nem rolar a tela sozinho enquanto a pessoa lê; oferecer um botão "ir para a última mensagem".
- Mensagens refluem a 400% de zoom, sem rolagem lateral (WCAG 1.4.10); campo de digitação com rótulo visível e envio pelo teclado (WCAG 2.1.1, 3.3.2).
- Botões de ação em cada explicação ("Ver versão técnica", "Trocar universo", "Está errada") com alvo de no mínimo 24×24 px (WCAG 2.5.8).
- Uma etapa por mensagem, com "Próximo passo", resolve a divergência dos seis passos numa única tela.
- A aparência de chat não implica conversa livre com a IA: as respostas ficam presas ao conceito escolhido e passam pela autoverificação (RNF04, D5, D6).

### Critérios de aceite (RF11)
```gherkin
Cenário: pergunta dentro do conceito
  Dado que estou estudando "Entrega confiável no TCP" com o universo "anime"
  Quando digito "o que acontece se o ACK se perder?"
  Então recebo uma resposta sobre esse conceito que passou pela autoverificação

Cenário: pergunta fora do conceito
  Dado que estou estudando "Entrega confiável no TCP"
  Quando digito "me explica o que é DNS" ou "quem ganhou o jogo ontem?"
  Então o app informa que só responde sobre o conceito atual
  E oferece os botões "Escolher outro conceito" e "Continuar este"
  E nenhuma resposta é gerada fora do texto-base

Cenário: pergunta que o texto-base não cobre
  Dado que a pergunta é sobre o conceito, mas o texto-base não traz a resposta
  Então o app diz que não conseguiu verificar essa informação, em vez de inventar
```

### Autoverificação da resposta (D6)
Termo técnico: **autoverificação** ou **autocrítica** (*self-verification*), feita no momento da resposta. Não confundir com aprendizado autossupervisionado (*self-supervised learning*), que é uma forma de treinar modelos.

Fluxo, baseado no Chain-of-Verification (Dhuliawala et al., 2024):
1. **Rascunho:** a IA gera a explicação (analogia e versão técnica) ou a resposta da pergunta.
2. **Perguntas de checagem:** a IA lista as afirmações técnicas do rascunho e cria uma pergunta de verificação para cada uma (ex.: "o TCP retransmite quando o ACK não chega?").
3. **Respostas independentes:** responde cada pergunta numa chamada separada, **sem ver o rascunho**, para não repetir o próprio erro.
4. **Veredito:** compara as respostas com o rascunho e também confere se a analogia não contradiz a versão técnica e se os fatos do universo (personagens, regras do jogo) estão corretos. Saída estruturada: `aprovada` ou `reprovada` + motivos.
5. **Validadores automáticos** (`validators/grounding.py`) continuam valendo depois disso.
6. **Reprovada:** uma nova tentativa com os motivos; se falhar de novo, explicação padrão com aviso. Nunca exibir resposta reprovada.

Limite conhecido: um modelo verificando a si mesmo reduz erros, mas não os elimina; sem informação externa, a autocorreção pode até piorar o resultado (Huang et al., 2024). Mitigações:
- usar como referência uma fonte técnica fixa por conceito (ex.: trecho do livro ou dos slides da disciplina) na etapa 3;
- manter o botão "Está errada" (RF05) e registrar os casos;
- medir no teste de usabilidade quantas explicações tinham erro.

Referências: DHULIAWALA, S. et al. Chain-of-Verification Reduces Hallucination in Large Language Models. Findings of ACL, 2024. HUANG, J. et al. Large Language Models Cannot Self-Correct Reasoning Yet. ICLR, 2024.
