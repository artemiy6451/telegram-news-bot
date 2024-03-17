from loguru import logger
from telebot import TeleBot
from telebot.util import quick_markup

from telegram_news_bot.templates import render_template


def send_settings(bot: TeleBot, channel_id: int):
    """Send formated settings string."""
    logger.debug("Send formated settings string.")
    keyboard = quick_markup(
        {
            "1": {"callback_data": "add_parsers_to_selected_list"},
            "2": {"callback_data": "add_tags_for_parsers"},
            "Закрыть": {"callback_data": "exit"},
        },
        row_width=2,
    )
    formated_message = render_template("telegram/settings.j2")
    bot.send_message(
        channel_id,
        formated_message,
        parse_mode="HTML",
        reply_markup=keyboard,
    )
