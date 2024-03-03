"""File with settings for project."""

import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from telebot.types import Path


class Settings(BaseSettings):
    """Class for import all env from `.env` file."""

    base_dir: Path = Path(__file__).resolve().parent
    template_dir: Path = base_dir / "../templates"
    database_path: Path = base_dir / "../database.db"
    model_config = SettingsConfigDict(env_file=".env")

    test_mode: bool = False
    data_dir: Path = base_dir / "../data"
    log_level: str = "INFO"
    update_time_for_parser_in_seconds: int = 3600
    time_for_send_post: int = 5
    time_for_connect_to_server: int = 1
    page_count_to_check: int = 5
    channel_id: int = 0
    telegram_api: str = ""

    habr_url: str = "https://habr.com/ru/articles/page{}"
    medium_url: str = "https://medium.com/_/graphql"

    medium_tags: list[str] = ["programming"]


settings = Settings()

if settings.test_mode and not os.path.exists(settings.data_dir):
    os.mkdir(settings.data_dir)
