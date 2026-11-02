"""Revisão humana das explicações geradas por IA (linha de comando).

    uv run python -m app.review list            # rascunhos e itens marcados como errados
    uv run python -m app.review show 12         # mostra uma explicação
    uv run python -m app.review approve 12      # aprova (passa a ser servida)
    uv run python -m app.review reject 12       # reprova

Em Docker: docker compose exec api python -m app.review list
"""
import json
import sys

from sqlalchemy import select

from app.db import Explanation, SessionLocal, init_db


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 1
    init_db()
    cmd, *rest = argv
    with SessionLocal() as db:
        if cmd == "list":
            rows = db.scalars(
                select(Explanation).where(Explanation.status.in_(["draft", "under_review"]))
            ).all()
            for r in rows:
                print(f"{r.id:>4}  {r.status:<13} {r.concept_slug} / {r.interest_label} ({r.provider})")
            if not rows:
                print("Nada para revisar.")
            return 0
        if cmd in {"show", "approve", "reject"} and rest:
            row = db.get(Explanation, int(rest[0]))
            if row is None:
                print("Não encontrada.")
                return 1
            if cmd == "show":
                print(json.dumps(row.payload, ensure_ascii=False, indent=2))
                return 0
            row.status = "approved" if cmd == "approve" else "rejected"
            db.commit()
            print(f"{row.id} → {row.status}")
            return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
