#!/usr/bin/env sh
set -e

# 1) Appliquer les migrations Alembic (cree les 5 tables si besoin).
#    La DB est deja prete grace au healthcheck + depends_on du compose.
echo ">> alembic upgrade head"
alembic upgrade head

# 2) Bootstrap idempotent : admin + import CSV + 1er modele entraine.
#    Relançable sans risque (il saute ce qui existe deja).
echo ">> seed (admin / import / train)"
python -m app.seed

# 3) Lancer l'API. `exec` remplace le shell par uvicorn -> les signaux
#    (Ctrl+C, docker stop) sont bien transmis au process Python.
echo ">> uvicorn"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
