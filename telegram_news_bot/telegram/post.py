"""File for post logic."""

import time

from loguru import logger
from telebot import TeleBot, traceback

from telegram_news_bot.config import settings
from telegram_news_bot.db import database_connection
from telegram_news_bot.schemas import Post
from telegram_news_bot.templates import render_template


def get_parsed_posts_from_all_sites() -> list[Post]:
    """Get parsed articles from all sites(habr and medium)."""
    logger.debug("Get parsed articles from all sites in list.")
    posts: list[Post] = []
    for parser in settings.current_parsers_list:
        posts = parser.parser_obj().parse()
    return posts


def add_post_to_database(post: Post):
    """Execute insert form `database_connection`."""
    logger.debug("Add post to database.")
    database_connection.insert_post(post)


def is_exist_post(post: Post) -> bool:
    """Check if post already in database."""
    logger.debug(f"Check is post with name {post.name} exist.")
    result = database_connection.select_post(post)
    if result:
        logger.debug("Post in database.")
        return True
    logger.debug("Post not in database.")
    return False


def send_posts(bot: TeleBot, chanel_id: int, posts: list[Post]):
    """Send all posts to telegram chanel."""
    logger.debug("Send all posts to telegram chanel.")
    for post in posts:
        try:
            if is_exist_post(post):
                continue
            formated_message = render_template("send_post.j2", post.model_dump())
            logger.debug("Send message.")
            bot.send_message(
                chanel_id,
                formated_message,
                parse_mode="HTML",
            )
            post.name = post.name.replace('"', "").replace("'", "").replace("’", "")
            add_post_to_database(post)
            time.sleep(settings.time_for_send_post)
        except Exception:
            logger.error(f"Error: {traceback.format_exc()}\nPost: {post.model_dump()}")
    logger.debug("All post sended.")
