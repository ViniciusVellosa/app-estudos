# Estrutura sugerida do repositório do projeto

```
projeto-ihc/
├── README.md                    # visão geral, equipe, como navegar
├── 1-pesquisa/
│   ├── plano-de-pesquisa.md     # objetivos, perguntas, método, recrutamento, ética
│   ├── roteiro-entrevista.md
│   ├── questionario.md          # e link do formulário publicado
│   ├── tcle.md                  # termo de consentimento
│   ├── dados/                   # transcrições e respostas ANONIMIZADAS (P01, P02…)
│   └── sintese.md               # diagrama de afinidade / análise temática → achados
├── 2-personas-cenarios/
│   ├── personas.md              # 2–3 personas (incluir 1 com baixa visão)
│   ├── pact.md                  # análise PACT
│   ├── cenarios.md              # cenários de problema e de atividade/interação
│   ├── jornada.md               # mapa de jornada (opcional)
│   └── requisitos.md            # histórias de usuário + critérios de aceite (inclui WCAG)
├── 3-prototipo/
│   ├── baixa-fidelidade/        # fotos/scan de papel ou wireframes
│   ├── alta-fidelidade/         # link Figma e/ou código (HTML/React)
│   ├── design-tokens.json       # cores, tipografia, espaçamentos (com contraste validado)
│   └── decisoes-de-design.md    # cada decisão → achado/persona/critério
├── 4-avaliacao/
│   ├── avaliacao-heuristica.md  # planilha consolidada + severidade
│   ├── auditoria-wcag.md        # automática + manual (teclado, zoom, leitor de tela)
│   ├── protocolo-teste.md       # tarefas, métricas, roteiro do moderador
│   ├── sus-respostas.csv
│   ├── resultados.md            # SUS, taxa de sucesso, tempo, erros, problemas
│   └── melhorias.md             # o que mudou no protótipo após a avaliação
└── relatorio-final.md
```

Rastreabilidade (mostrar no relatório): **achado da pesquisa → persona/cenário
→ requisito/critério → elemento do protótipo → tarefa do teste → resultado**.
