"""Main file of program."""

import threading

from loguru import logger

from telegram_news_bot.config import settings
from telegram_news_bot.telegram.bot import bot as telegram_bot
from telegram_news_bot.telegram.bot import send_automatic_posts

logger.add(
    "file.log",
    level=settings.log_level,
    colorize=False,
    backtrace=True,
    diagnose=True,
)

if settings.test_mode:
    events = [
        [telegram_bot.infinity_polling, ()],
    ]
else:
    events = [
        [telegram_bot.infinity_polling, ()],
        [
            send_automatic_posts,
            (
                telegram_bot,
                settings.channel_id,
                settings.update_time_for_parser_in_seconds,
            ),
        ],
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
