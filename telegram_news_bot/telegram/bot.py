"""File for telegram bot logic."""

import time

import telebot
from loguru import logger
from telebot.types import Message

from telegram_news_bot.config import settings
from telegram_news_bot.services.post import get_parsed_posts_from_all_sites, send_posts

logger.info("Start telegram bot.")
bot = telebot.TeleBot(settings.telegram_api)


@bot.channel_post_handler(commands=["start"])
def send_manually_posts(message: Message):
    """Send posts to channel by /start."""
    logger.debug("Send posts to channel by /start.")
    bot.delete_message(message.chat.id, message.id)
    send_posts(bot, message.chat.id, get_parsed_posts_from_all_sites())


def send_automatic_posts(bot: telebot.TeleBot):
    """Automaticly send posts to channel."""
    logger.debug("Start automatic send posts.")
    while True:
        send_posts(bot, settings.channel_id, get_parsed_posts_from_all_sites())
        time.sleep(settings.update_time_for_parser_in_seconds)
