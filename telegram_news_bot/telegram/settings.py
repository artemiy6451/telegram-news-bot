from loguru import logger
from telebot import TeleBot
from telebot.types import Message
from telebot.util import quick_markup

from telegram_news_bot.config import settings
from telegram_news_bot.templates import render_template


def send_settings(bot: TeleBot, channel_id: int):
    """Send formated settings string."""
    logger.debug("Send formated settings string.")
    keyboard = quick_markup(
        {
            "1": {"callback_data": "change_list_of_parsers"},
            "Назад": {"callback_data": "back"},
        },
        row_width=2,
    )
    formated_message = render_template("settings.j2")
    bot.send_message(
        channel_id,
        formated_message,
        parse_mode="HTML",
        reply_markup=keyboard,
    )


def send_parsers_list_to_change(bot: TeleBot, channel_id: int):
    """Send all parsers with inline keyboard for choose witch parser toggle."""
    logger.debug("Send parsers list to change.")

    markup_data = {
        f"{index+1}": {"callback_data": f"select_parser_{index}"}
        for index, _ in enumerate(settings.avaliable_parsers_list)
    }
    markup_data = markup_data | {"Назад": {"callback_data": "back"}}

    keyboard = quick_markup(markup_data, row_width=2)
    formated_message = render_template(
        "select_parsers.j2",
        {
            "current_parsers_list": settings.current_parsers_list,
            "avaliable_parsers_list": settings.avaliable_parsers_list,
        },
    )
    bot.send_message(
        channel_id,
        formated_message,
        parse_mode="HTML",
        reply_markup=keyboard,
    )


def update_message_for_change_parsers_list(bot: TeleBot, message: Message):
    logger.debug("Update message for change parsers list.")
    formated_message = render_template(
        "select_parsers.j2",
        {
            "current_parsers_list": settings.current_parsers_list,
            "avaliable_parsers_list": settings.avaliable_parsers_list,
        },
    )
    markup_data = {
        f"{index+1}": {"callback_data": f"select_parser_{index}"}
        for index, _ in enumerate(settings.avaliable_parsers_list)
    }
    markup_data = markup_data | {"Назад": {"callback_data": "back"}}
    keyboard = quick_markup(markup_data, row_width=2)
    bot.edit_message_text(
        formated_message,
        message.chat.id,
        message.id,
        reply_markup=keyboard,
    )
