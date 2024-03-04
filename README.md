# Telegram news bot
Это телеграм бот, для оправки новых сообщений с постами из habr и medium.

# Todo:

### Проект
- Добавить github actoins
- Написать тесты(только после рефакторинга)
- Исправить баг, когда в названии есть ковычки(из за них невозможно добавить пост в базу данных)
- Полученный данные из запросов graphql парсить в pydantic схемы.

### Рефакторинг

# Как запустить?

### Сначала надо создать базу данных используя sqlite3:
```shell
mkdir data
cat database.sql | sqlite3 database.db 
mv database.db data/
```

## Без использования Docker

### Для запуска проекта используется poetry и python3.11
```shell
pip install poetry
```

##### Установка зависимостей
```shell
poerty install
```
##### Настройка переменных окружения
```shell
cp .env.template .env
```

##### Запуск приложения
```shell
poetry run python -m telegram_news_bot
```

## Используя Docker

### Создание Docker образа
```shell
docker build -t telegram_news_bot .
```

##### Настройка переменных окружения
```shell
cp .env.template .env
```

##### Запуск приложения
```shell
docker run -it --rm --name telegram-news-bot-dockered --env-file=.env telegram_news_bot:latest 
```

## Используя Docker compose

##### Настройка переменных окружения
```shell
cp .env.template .env
```

## Запуск приложения
```shell
docker compose up --build -d
```
