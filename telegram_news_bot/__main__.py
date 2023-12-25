"""Main file of program."""

from loguru import logger

from telegram_news_bot.config import settings
from telegram_news_bot.telegram.bot import bot

logger.add(
    "file.log",
    level=settings.log_level,
    colorize=False,
    backtrace=True,
    diagnose=True,
)


def main():
    """Start program."""
    logger.debug("Start program.")
    try:
        bot.infinity_polling()
    except Exception as e:
        logger.error(f"Something went wrong: {e}")


try:
    main()
except Exception as e:
    logger.error(f"Something went wrong: {e}")
