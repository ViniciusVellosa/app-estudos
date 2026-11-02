# Requisitos

Formato: história de usuário + critérios de aceite (Dado/Quando/Então) +
rastreio até a pesquisa e o teste. Prioridade MoSCoW (Must/Should/Could/Won't).
Requisitos de acessibilidade e personalização vêm do Lumen (códigos RA e DP).

## Funcionais
| ID | História | Prioridade | Rastreio | Teste automatizado |
|---|---|---|---|---|
| RF01 | Como aluno, quero começar sem criar conta com nome e e-mail, para não perder tempo nem expor dados | Must | achado A_ → persona _ | `test_api.py::test_health` + e2e |
| RF02 | Como aluno, quero informar meus interesses e o quanto conheço deles | Must | | `test_interest_requires_consent` |
| RF03 | Como aluno, quero a explicação de um conceito usando meu interesse, em passos curtos | Must | | e2e `fluxo-principal` |
| RF04 | Como aluno, quero ver a explicação sem analogia com um toque | Must | DP do Lumen | e2e |
| RF05 | Como aluno, quero avisar que uma explicação está errada ou confusa | Should | | `test_wrong_feedback_...` |
| RF06 | Como aluno com baixa visão, quero aumentar o texto e usar alto contraste no app | Must | persona com baixa visão | e2e `texto ampliado...` |
| RF07 | Como aluno, quero ver e apagar meus dados | Must | LGPD art. 18 | `test_delete_me_erases_everything` |

### Exemplo de critérios de aceite (RF03)
```gherkin
Cenário: explicação personalizada revisada
  Dado que aceitei o termo e informei o interesse "futebol"
  Quando peço a explicação de "Entrega confiável no TCP"
  Então vejo os passos: conceito, cena, quem é quem, onde a comparação falha,
        explicação técnica e uma pergunta para testar
  E a mensagem "Explicação pronta." é anunciada pelo leitor de tela (WCAG 4.1.3)

Cenário: sem explicação revisada para o interesse
  Dado que informei o interesse "xadrez"
  Quando peço a explicação de "Entrega confiável no TCP"
  Então vejo a explicação padrão e um aviso explicando o motivo
```

## Não funcionais (ISO/IEC 25010:2023)
| ID | Característica | Requisito | Verificação |
|---|---|---|---|
| RNF01 | Capacidade de interação (inclusividade) | WCAG 2.2 AA; sem rolagem lateral a 320px com texto 2x | axe + e2e + checklist manual do Lumen |
| RNF02 | Segurança | Chave da IA só no back-end; banco sem porta exposta; sessão por token com hash | revisão de código |
| RNF03 | Confiabilidade | Falha ou recusa da IA → explicação padrão | `test_llm_*` |
| RNF04 | Correção do conteúdo | Toda afirmação técnica vem de texto-base revisado | validadores + revisão |
| RNF05 | Privacidade (LGPD) | Minimização, consentimento, exportação e exclusão | testes de API |
| RNF06 | Flexibilidade | Sobe com `docker compose up`; troca de provedor de IA por variável | CI |
