"""File for telegram bot logic."""

import telebot
from loguru import logger
from telebot.types import CallbackQuery, Message

from telegram_news_bot.config import settings
from telegram_news_bot.telegram.add_parsers import (
    send_parsers_list_to_add,
    update_message_for_add_parsers_list,
)
from telegram_news_bot.telegram.add_tags import (
    add_new_tag_to_selected_tags,
    add_tag_for_parser,
    choose_parser_for_add_tags,
    update_message_for_add_tag,
)
from telegram_news_bot.telegram.settings import send_settings
from telegram_news_bot.telegram.start import send_posts
from telegram_news_bot.telegram.utils import (
    add_parser_to_selected_parsers,
    get_parsed_posts_from_all_sites,
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


@bot.channel_post_handler(commands=["settings"])
def send_settings_post(message: Message):
    """Send settings post."""
    logger.debug("Send settings post.")
    bot.delete_message(message.chat.id, message.id)
    send_settings(bot, message.chat.id)


@bot.callback_query_handler(lambda query: query.data in ("back", "exit"))
def return_to_main_menu(query: CallbackQuery):
    bot.delete_message(query.message.chat.id, query.message.id)
    settings.waiting_for = {}
    if query.data == "back":
        send_settings(bot, query.message.chat.id)


@bot.channel_post_handler(
    content_types=["text"],
    func=lambda _: settings.waiting_for,
)
def process_text(message: Message):
    """Process text from channel."""
    logger.debug(f"Process text: {message.text=}\n{settings.waiting_for=}")
    match settings.waiting_for:
        case d if d.get("tag"):
            add_new_tag_to_selected_tags(message.text)
            update_message_for_add_tag(bot, message.chat.id)
    bot.delete_message(message.chat.id, message.id)


@bot.callback_query_handler(lambda query: query.data != "back")
def process_callback_data(query: CallbackQuery):
    """Process all callback data."""
    logger.debug(f"Process callback data: {query.data=}")
    match RegexEqual(query.data):
        case "add_parsers_to_selected_list":
            send_parsers_list_to_add(bot, query.message.chat.id)
        case r"^add_parser_\d+$":
            add_parser_to_selected_parsers(query)
            update_message_for_add_parsers_list(bot=bot, message=query.message)
            logger.debug(f"{settings.selected_parsers_list}")
        case r"^add_tags_for_parsers$":
            choose_parser_for_add_tags(bot, query.message.chat.id)
        case r"^add_tag_for_parser_\d+$":
            add_tag_for_parser(query, bot, query.message.chat.id)
        case _:
            logger.warning(f"{query.data=}")
