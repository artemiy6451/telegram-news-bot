"""File for telegram bot logic."""

import time

import telebot
from loguru import logger
from telebot.types import CallbackQuery, Message

from telegram_news_bot.config import settings
from telegram_news_bot.db import database_connection
from telegram_news_bot.schemas import Post
from telegram_news_bot.services.post import get_parsed_posts_form_habr, send_posts
from telegram_news_bot.templates import render_template

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
        try:
            bot.delete_message(call.message.chat.id, call.message.id)
        except telebot.apihelper.ApiTelegramException:
            if call.message.text is None:
                logger.error(f"Can not delete message {call}")
                return
            post = database_connection.select_post(
                Post(
                    name="",
                    url=call.message.text.split("\n")[-1],
                    time_to_read="",
                )
            )
            print(post)
            breakpoint()
            if post is None:
                logger.error(f"Can not delete message {call}")
                return
            post = Post(
                name=post[0][1],
                time_to_read=post[0][2],
                url=post[0][3],
            ).model_dump()
            error_message = "Can not delete post."
            post["update_message"] = error_message
            print(post)
            rendered_message = render_template(
                "update_post.j2",
                post,
            )
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                text=rendered_message,
                parse_mode="HTML",
            )
