FROM python:3.11
RUN set -ex && \
    apt-get update && apt-get install -y sqlite3
RUN pip install poetry
WORKDIR /app
COPY . /app
RUN poetry lock
RUN poetry install
RUN set -ex && cat database.sql | sqlite3 database.db 
ENV NUM_THREADS=2
CMD ["poetry", "run", "python", "-m", "telegram_news_bot"]
