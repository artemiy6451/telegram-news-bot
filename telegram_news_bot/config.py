"""File with settings for project."""

import os

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict
from telebot.types import Path

from telegram_news_bot.parser import Parser


class Settings(BaseSettings):
    """Class for import all env from `.env` file."""

    base_dir: Path = Path(__file__).resolve().parent.parent
    template_dir: Path = base_dir / "telegram_news_bot" / "templates"
    data_dir: Path = base_dir / "data"
    database_path: Path = data_dir / "database.db"
    model_config = SettingsConfigDict(env_file=".env")

    test_mode: bool = False
    log_level: str = "INFO"
    update_time_for_parser_in_seconds: int = 3600
    time_for_send_post: int = 5
    time_for_connect_to_server: int = 1
    page_count_to_check: int = 5
    channel_id: int = 0
    telegram_api: str = ""
    current_parsers_list: list[Parser] = []
    avaliable_parsers_list: list[Parser] = []

    habr_url: str = "https://habr.com/ru/articles/page{}"
    medium_url: str = "https://medium.com/_/graphql"

    medium_tags: list[str] = ["programming"]


settings = Settings()

if settings.test_mode and not os.path.exists(settings.data_dir):
    os.mkdir(settings.data_dir)

if settings.test_mode:
    logger.debug(f"{settings.model_dump()}")
