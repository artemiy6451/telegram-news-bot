"""File for post logic."""

import time

from loguru import logger
from telebot import TeleBot, telebot, traceback

from telegram_news_bot.config import settings
from telegram_news_bot.schemas import Post
from telegram_news_bot.telegram.utils import (
    add_post_to_database,
    get_parsed_posts_from_all_sites,
    is_exist_post,
)
from telegram_news_bot.templates import render_template


def send_post_transactional(bot: TeleBot, chanel_id: int, post: Post):
    try:
        formated_message = render_template("telegram/send_post.j2", post.model_dump())
        bot.send_message(
            chanel_id,
            formated_message,
            parse_mode="HTML",
        )
        post.name = post.name.replace('"', "").replace("'", "").replace("’", "")
        add_post_to_database(post)
    except Exception:
        logger.error(f"Error: {traceback.format_exc()}\nPost: {post.model_dump()}")


def send_posts(bot: TeleBot, chanel_id: int, posts: list[Post]):
    """Send all posts to telegram chanel."""
    logger.debug("Send all posts to telegram chanel.")
    for post in posts:
        if is_exist_post(post):
            continue
        send_post_transactional(bot, chanel_id, post)
        time.sleep(settings.time_for_send_post)
    logger.debug("All post sended.")


def send_automatic_posts(bot: telebot.TeleBot):
    """Automaticly send posts to channel."""
    logger.debug("Start automatic send posts.")
    while True:
        send_posts(bot, settings.channel_id, get_parsed_posts_from_all_sites())
        time.sleep(settings.update_time_for_parser_in_seconds)
