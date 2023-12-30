"""File for telegram bot logic."""

import time

import telebot
from loguru import logger
from telebot.types import CallbackQuery, Message

from telegram_news_bot.config import settings
from telegram_news_bot.services.post import get_parsed_posts_form_habr, send_posts

logger.info("Start telegram bot.")
bot = telebot.TeleBot(settings.telegram_api)


@bot.channel_post_handler(commands=["start"])
def send_manually_posts(message: Message):
    """Send posts to channel by click /start."""
    print(message.chat.id)
    bot.delete_message(message.chat.id, message.id)
    send_posts(bot, message.chat.id, get_parsed_posts_form_habr())


def send_automatic_posts(bot: telebot.TeleBot, channel_id: int, update_time: int):
    """Automaticly send posts to channel."""
    logger.debug("Start automatic send posts.")
    while True:
        send_posts(bot, channel_id, get_parsed_posts_form_habr())
        time.sleep(update_time)


@bot.callback_query_handler(func=lambda call: True)
def delete_post(call: CallbackQuery):
    """Delete post form wall using inline keyboard."""
    logger.debug("Delete message.")
    if call.data == "delete":
        bot.delete_message(call.message.chat.id, call.message.id)
