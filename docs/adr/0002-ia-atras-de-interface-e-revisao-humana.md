# ADR 0002 — IA atrás de uma interface, com validação e revisão humana

- **Status:** aceita
- **Data:** AAAA-MM-DD

## Contexto
Analogias geradas por IA podem soar certas e estar erradas (caso real: uma
analogia com Pokémon descrevia o protocolo pare-e-espere em vez do TCP). A
pesquisa de IHC indica que detalhes irrelevantes atrapalham a aprendizagem e
que IA sem salvaguardas pode prejudicar o aprendizado.

## Decisão
1. Cada conceito tem um **texto-base revisado** (`content/concepts/`), que é a
   única fonte de verdade técnica.
2. O gerador (`ExplanationGenerator`) tem duas implementações: `curated`
   (explicações escritas à mão) e `llm`.
3. A saída da IA passa por schema (Pydantic) e por validadores
   determinísticos (`validators/grounding.py`); falhou duas vezes → explicação
   padrão.
4. Explicações geradas nascem como rascunho; só aparecem para o aluno depois
   de aprovadas (`python -m app.review`), a menos que `SERVE_ONLY_APPROVED=false`.

## Consequências
- (+) O teste de usabilidade pode acontecer antes da integração com IA.
- (+) Erro técnico conhecido vira teste automatizado de regressão.
- (−) Revisão humana dá trabalho; por isso as explicações aprovadas ficam em cache.
