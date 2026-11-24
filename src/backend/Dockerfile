FROM python:3.12-slim

# - PYTHONDONTWRITEBYTECODE: pas de fichiers .pyc dans l'image
# - PYTHONUNBUFFERED: logs envoyes directement (visibles dans `docker logs`)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

# On copie d'abord SEULEMENT les dependances : tant que requirements.txt
# ne change pas, Docker reutilise ce layer en cache (build plus rapide).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Puis le reste du code (app/, migrations/, alembic.ini, data/, entrypoint...).
COPY . .

# Securite line-endings : si le script a ete sauve en CRLF (Windows),
# on retire les \r sinon le shebang casse dans le conteneur Linux.
RUN sed -i 's/\r$//' docker-entrypoint.sh && chmod +x docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
