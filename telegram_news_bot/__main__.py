"""Main file of program."""

import threading
from typing import Callable

from loguru import logger

from telegram_news_bot import parsers
from telegram_news_bot.config import settings
from telegram_news_bot.parser import ParserSchema
from telegram_news_bot.telegram.commands import bot as telegram_bot
from telegram_news_bot.telegram.start import send_automatic_posts

logger.add(
    settings.data_dir / "telegram_news_bot.log",
    level=settings.log_level,
    colorize=False,
    backtrace=True,
    diagnose=True,
    rotation="2 MB",
    compression="zip",
)

all_parsers_list: list[ParserSchema] = [
    ParserSchema(
        name="habr",
        verbose_name="Хабр",
        parser_obj=parsers.habr.HabrParser,
        tags=["develop"],
    ),
    ParserSchema(
        name="medium",
        verbose_name="Медиум",
        parser_obj=parsers.medium.MediumParser,
        tags=["programming"],
    ),
]

settings.avaliable_parsers_list = all_parsers_list

if settings.test_mode:
    events: list[tuple[Callable, tuple]] = [
        (telegram_bot.infinity_polling, ()),
    ]
    settings.selected_parsers_list = [
        ParserSchema(
            name="habr",
            verbose_name="Хабр",
            parser_obj=parsers.habr.HabrParser,
            tags=["develop"],
        ),
    ]
else:
    events: list[tuple[Callable, tuple]] = [
        (telegram_bot.infinity_polling, ()),
        (
            send_automatic_posts,
            (telegram_bot,),
        ),
    ]


threads = []


def main():
    """Start program."""
    logger.debug("Start program.")
    for event, args in events:
        threads.append(threading.Thread(target=event, args=args))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


try:
    main()
except Exception as e:
    logger.error(f"Something went wrong: {e}")
except KeyboardInterrupt:
    logger.info("Shutdown program.")
