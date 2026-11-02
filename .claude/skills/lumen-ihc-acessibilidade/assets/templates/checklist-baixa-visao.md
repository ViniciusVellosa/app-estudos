# Checklist de acessibilidade para baixa visão — protótipo e código

Marque: ✅ passa · ❌ falha · ➖ não se aplica. Registre evidência (print, medida).

## Percepção visual
| # | Verificação | Critério | Como testar | Resultado |
|---|---|---|---|---|
| 1 | Texto normal com contraste ≥ 4,5:1 (meta do projeto: ≥ 7:1) | 1.4.3 (AA) / 1.4.6 (AAA) | `contrast_check.py` em todos os pares de token | |
| 2 | Texto grande (≥ 24px, ou ≥ 18,66px negrito) ≥ 3:1 | 1.4.3 (AA) | idem | |
| 3 | Bordas de campos, ícones, botões e estados ≥ 3:1 | 1.4.11 (AA) | idem, com `--componente` | |
| 4 | Informação nunca só por cor (erro, correto, obrigatório, link) | 1.4.1 (A) | ver em escala de cinza | |
| 5 | Nada de texto em imagem (exceto logo) | 1.4.5 (AA) | inspeção | |
| 6 | Tema de alto contraste / respeita `forced-colors` e `prefers-contrast` | boa prática / e-MAG cap. 4 | ativar no SO | |

## Ampliação e layout
| # | Verificação | Critério | Como testar | Resultado |
|---|---|---|---|---|
| 7 | Zoom de 200% sem perda de conteúdo/função | 1.4.4 (AA) | Ctrl + no navegador | |
| 8 | A 400% (ou 320px de largura) não há rolagem horizontal | 1.4.10 (AA) | DevTools 320px | |
| 9 | Espaçamento ajustado (linha 1,5; parágrafo 2×; letra 0,12; palavra 0,16) sem cortar texto | 1.4.12 (AA) | bookmarklet de text spacing | |
| 10 | Zoom não bloqueado (sem `user-scalable=no`/`maximum-scale=1`) | 1.4.4 | inspecionar meta viewport | |
| 11 | Fonte do sistema (Android/iOS) aumenta o texto do app | 1.4.4 | configurações do SO | |
| 12 | Tooltips/popovers persistem, podem ser fechados e não cobrem conteúdo | 1.4.13 (AA) | passar mouse e Tab | |

## Navegação e foco
| # | Verificação | Critério | Como testar | Resultado |
|---|---|---|---|---|
| 13 | Foco sempre visível, contorno ≥ 2px com contraste ≥ 3:1 | 2.4.7 (AA), 2.4.13 (AAA) | navegar com Tab | |
| 14 | Foco não fica escondido por cabeçalho/rodapé fixo | 2.4.11 (AA) | Tab com zoom 200% | |
| 15 | Alvos de toque ≥ 24×24px (meta: 44×44px) | 2.5.8 (AA) / 2.5.5 (AAA) | medir no Figma/DevTools | |
| 16 | Ordem de foco lógica; tudo operável por teclado | 2.4.3, 2.1.1 (A) | só teclado | |
| 17 | Instruções não dependem de posição/forma ("botão à direita") | 1.3.3 (A) | revisão de texto | |

## Leitor de tela (baixíssima visão e cegueira)
| # | Verificação | Critério | Como testar | Resultado |
|---|---|---|---|---|
| 18 | Títulos `h1`–`h6` hierárquicos e regiões (`main`, `nav`) | 1.3.1 (A) | NVDA/VoiceOver: lista de títulos | |
| 19 | Imagens e ilustrações das analogias têm texto alternativo útil | 1.1.1 (A) | leitor de tela | |
| 20 | Botões e controles têm nome, função e estado | 4.1.2 (A) | leitor de tela | |
| 21 | Mensagens (ex.: "explicação gerada") anunciadas sem mover foco | 4.1.3 (AA) | `aria-live` | |
| 22 | Idioma da página declarado (`lang="pt-BR"`) | 3.1.1 (A) | inspeção | |

## Carga cognitiva (afeta todos, crítica com ampliação)
| # | Verificação | Critério | Resultado |
|---|---|---|---|
| 23 | Ajuda no mesmo lugar em todas as telas | 3.2.6 (A) | |
| 24 | Não pede de novo dado já informado | 3.3.7 (A) | |
| 25 | Login sem teste cognitivo (permite colar senha, gerenciador) | 3.3.8 (AA) | |
| 26 | Sem limite de tempo nas atividades (ou ajustável) | 2.2.1 (A) | |
| 27 | Animações podem ser pausadas; respeita `prefers-reduced-motion` | 2.2.2 (A), 2.3.3 (AAA) | |

> Ferramentas automáticas (axe, WAVE, Lighthouse, ASES) cobrem só parte destes
> itens. Os itens 7–9, 13–14, 17 e 19–21 exigem verificação manual.
