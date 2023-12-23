"""Main file of program."""

import sys

from loguru import logger

from telegram_news_bot.config import settings
from telegram_news_bot.telegram.bot import bot

log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS zz}</green>"
    " | <level>{level: <8}</level> | <yellow>Line {line: >4}"
    "({file}):</yellow> <b>{message}</b>"
)
logger.add(
    sys.stdout,
    level=settings.log_level,
    format=log_format,
    colorize=True,
    backtrace=True,
    diagnose=True,
)
logger.add(
    "file.log",
    level=settings.log_level,
    format=log_format,
    colorize=False,
    backtrace=True,
    diagnose=True,
)


def main():
    """Start program."""
    logger.debug("Start program.")
    bot.infinity_polling()


try:
    main()
except Exception as e:
    logger.debug(f"Something went wrong: {e}")
