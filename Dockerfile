FROM python:3.11
RUN set -ex && \
    apt-get update && apt-get install -y sqlite3
RUN pip install poetry
WORKDIR /app
COPY . /app
RUN poetry lock
RUN poetry install

CMD ["poetry", "run", "python", "-m", "telegram_news_bot"]
