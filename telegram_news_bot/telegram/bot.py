"""File for telegram bot logic."""

from time import sleep

import telebot
from loguru import logger
from telebot.types import CallbackQuery, Message
from telebot.util import quick_markup

from telegram_news_bot.config import settings
from telegram_news_bot.habr.parser import Parser
from telegram_news_bot.templates import render_template

logger.info("Start telegram bot.")
bot = telebot.TeleBot(settings.telegram_api)

markup = quick_markup(
    {
        "Delete": {"callback_data": "delete"},
    }
)


@bot.channel_post_handler(commands=["start"])
def send_message(message: Message):
    """Send message to channel."""
    logger.debug("Send message.")
    bot.delete_message(message.chat.id, message.id)
    parser = Parser()
    articles = parser.parse()

    for article in articles:
        data = {
            "name": article.name,
            "author": article.author,
            "date": str(article.published.date()),
            "difficulty": str(article.difficulty),
            "time_to_read": article.time_to_read,
            "description": article.description,
            "tags": str(article.tags),
            "labels": article.labels,
            "url": article.url,
        }
        formated_message = render_template("post.j2", data)
        print(formated_message)
        bot.send_message(
            message.chat.id,
            formated_message,
            parse_mode="Markdown",
            reply_markup=markup,
        )
        break
        sleep(1)


@bot.callback_query_handler(func=lambda call: True)
def delete_post(call: CallbackQuery):
    """Delete post form wall using inline keyboard."""
    logger.debug("Delete message.")
    if call.data == "delete":
        bot.delete_message(call.message.chat.id, call.message.id)
