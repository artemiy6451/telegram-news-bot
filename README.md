# Telegram news bot
---
Это телеграм бот, для оправки новых сообщений с постами из habr и medium.

# Todo:

### Проект
---
- Добавить github actoins
- Написать тесты(только после рефакторинга)
- Сделать так чтобы работал абстрактный класс с парсерами.

### Рефакторинг
---

# Как запустить?
---
## Сначала надо создать базу данных используя sqlite3:
```shell
cat database.sql | sqlite3 database.db 
```
## Для запуска проекта используется poetry и python3.12

#### Установка зависимостей
```shell
poerty install
```
#### Настройка переменных окружения
```shell
cp .env.template .env
```

#### Запуск приложения
```shell
poetry run python -m telegram_news_bot
```
