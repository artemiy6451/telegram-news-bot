from loguru import logger
from telebot.util import quick_markup

from telegram_news_bot.config import settings
from telegram_news_bot.db import database_connection
from telegram_news_bot.schemas import Post


def add_parser_to_selected_parsers(query):
    """Add parser to `settings.selected_parsers_list`"""
    parser_id = int(query.data.split("_")[-1])
    settings.selected_parsers_list.append(settings.avaliable_parsers_list[parser_id])
    settings.avaliable_parsers_list.pop(parser_id)


def get_parsed_posts_from_all_sites() -> list[Post]:
    """Get parsed articles from all sites in `selected_parsers_list`."""
    logger.debug("Get parsed articles from all sites in list.")
    posts: list[Post] = []
    for parser in settings.selected_parsers_list:
        posts = parser.parser_obj().parse(parser.tags)
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


def create_keyboard_markup_for_add_parsers():
    logger.debug("Create keyboard markup for add parsers.")
    markup_data = {
        f"{index+1}": {"callback_data": f"add_parser_{index}"}
        for index, _ in enumerate(settings.avaliable_parsers_list)
    }
    markup_data = markup_data | {"Назад": {"callback_data": "back"}}
    keyboard = quick_markup(markup_data, row_width=2)

    return keyboard
