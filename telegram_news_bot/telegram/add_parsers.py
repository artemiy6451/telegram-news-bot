from loguru import logger
from telebot import TeleBot
from telebot.types import Message

from telegram_news_bot.config import settings
from telegram_news_bot.telegram.utils import create_keyboard_markup_for_add_parsers
from telegram_news_bot.templates import render_template


def send_parsers_list_to_add(bot: TeleBot, channel_id: int):
    """Send all parsers with inline keyboard for choose witch parser toggle."""
    logger.debug("Send parsers list to change.")

    formated_message = render_template(
        "telegram/add_parsers.j2",
        {
            "selected_parsers_list": settings.selected_parsers_list,
            "avaliable_parsers_list": settings.avaliable_parsers_list,
        },
    )
    bot.send_message(
        channel_id,
        formated_message,
        parse_mode="HTML",
        reply_markup=create_keyboard_markup_for_add_parsers(),
    )


def update_message_for_add_parsers_list(bot: TeleBot, message: Message):
    logger.debug("Update message for change parsers list.")

    formated_message = render_template(
        "telegram/add_parsers.j2",
        {
            "selected_parsers_list": settings.selected_parsers_list,
            "avaliable_parsers_list": settings.avaliable_parsers_list,
        },
    )
    bot.edit_message_text(
        formated_message,
        message.chat.id,
        message.id,
        reply_markup=create_keyboard_markup_for_add_parsers(),
    )
