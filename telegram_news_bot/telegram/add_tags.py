from telebot import TeleBot
from telebot.types import CallbackQuery
from telebot.util import quick_markup

from telegram_news_bot.config import settings
from telegram_news_bot.templates import render_template


def choose_parser_for_add_tags(bot: TeleBot, channel_id: int):
    formated_message = render_template(
        "telegram/choose_parser_for_add_tags.j2",
        {
            "selected_parsers_list": settings.selected_parsers_list,
        },
    )
    markup_data = {
        f"{index+1}": {"callback_data": f"add_tag_for_parser_{index}"}
        for index, _ in enumerate(settings.selected_parsers_list)
    }
    markup_data = markup_data | {"Назад": {"callback_data": "back"}}
    keyboard = quick_markup(markup_data, row_width=2)
    bot.send_message(
        channel_id,
        formated_message,
        parse_mode="HTML",
        reply_markup=keyboard,
    )


def add_tag_for_parser(query: CallbackQuery, bot: TeleBot, channel_id: int):
    parser_id = int(query.data.split("_")[-1])
    parser = settings.selected_parsers_list[parser_id]
    formated_message = render_template(
        "telegram/add_tags_for_parser.j2",
        {
            "parser": parser,
        },
    )
    markup_data = {"Назад": {"callback_data": "back"}}
    keyboard = quick_markup(markup_data, row_width=2)
    bot.send_message(
        channel_id,
        formated_message,
        parse_mode="HTML",
        reply_markup=keyboard,
    )
    settings.waiting_for["tag"] = parser


def update_message_for_add_tag(bot: TeleBot, channel_id: int):
    parser = settings.waiting_for.get("tag")
    formated_message = render_template(
        "telegram/add_tags_for_parser.j2",
        {
            "parser": parser,
        },
    )
    markup_data = {"Назад": {"callback_data": "back"}}
    keyboard = quick_markup(markup_data, row_width=2)
    bot.send_message(
        channel_id,
        formated_message,
        parse_mode="HTML",
        reply_markup=keyboard,
    )


def add_new_tag_to_selected_tags(tag: str | None):
    parser = settings.waiting_for.get("tag")
    if parser is None:
        return
    if tag is None:
        return
    parser.tags.append(tag)
