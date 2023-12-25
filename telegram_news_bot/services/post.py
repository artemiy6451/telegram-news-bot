"""File for post logic."""

import time

from loguru import logger
from telebot import TeleBot, traceback
from telebot.util import quick_markup

from telegram_news_bot.db import database_connection
from telegram_news_bot.habr.parser import Parser
from telegram_news_bot.schemas import Post
from telegram_news_bot.templates import render_template

markup = quick_markup(
    {
        "Delete": {"callback_data": "delete"},
    }
)


def get_parsed_posts_form_habr() -> list[Post]:
    """Get parsed articles from habr."""
    logger.debug("Get parsed articles from habr.")
    parser = Parser()
    articles = parser.parse()
    return articles


def add_post_to_database(post: Post):
    """Execute insert form `database_connection`."""
    logger.debug("Add post to database.")
    database_connection.insert_post(post)


def is_exist_post(post: Post) -> bool:
    """Check if post already in database."""
    logger.debug("Check is post exist.")
    result = database_connection.select_post(post)
    if result:
        return True
    return False


def send_posts(bot: TeleBot, chanel_id: int, posts: list[Post]):
    """Send all posts to telegram chanel."""
    for post in posts:
        try:
            if is_exist_post(post):
                continue
            formated_message = render_template("post.j2", post.model_dump())
            logger.debug("Send message.")
            bot.send_message(
                chanel_id,
                formated_message,
                parse_mode="HTML",
                reply_markup=markup,
            )
            add_post_to_database(post)
            time.sleep(2.2)
        except Exception:
            logger.error(f"Error: {traceback.format_exc()}")
