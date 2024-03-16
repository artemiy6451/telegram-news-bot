"""File for telegram bot logic."""

import time

import telebot
from loguru import logger
from telebot.types import CallbackQuery, Message

from telegram_news_bot.config import settings
from telegram_news_bot.telegram.post import get_parsed_posts_from_all_sites, send_posts
from telegram_news_bot.telegram.settings import (
    send_parsers_list_to_change,
    send_settings,
    update_message_for_change_parsers_list,
)
from telegram_news_bot.utils import RegexEqual

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


@bot.channel_post_handler(commands=["settings"])
def send_settings_post(message: Message):
    """Send settings post."""
    logger.debug("Send settings post.")
    bot.delete_message(message.chat.id, message.id)
    send_settings(bot, message.chat.id)


@bot.callback_query_handler(lambda query: query.data == "back")
def return_to_main_menu(query: CallbackQuery):
    bot.delete_message(query.message.chat.id, query.message.id)


@bot.callback_query_handler(lambda query: query.data != "back")
def process_callback_data(query: CallbackQuery):
    """Process all callback data."""
    logger.debug(f"{query.data=}")
    match RegexEqual(query.data):
        case "change_list_of_parsers":
            send_parsers_list_to_change(bot, query.message.chat.id)
        case r"^select_parser_\d+$":
            parser_id = int(query.data.split("_")[-1])
            settings.selected_parsers_list.append(
                settings.avaliable_parsers_list[parser_id]
            )
            settings.avaliable_parsers_list.pop(parser_id)
            update_message_for_change_parsers_list(bot=bot, message=query.message)
            logger.debug(f"{settings.selected_parsers_list}")
