"""File with settings for project."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from telebot.types import Path


class Settings(BaseSettings):
    """Class for import all env from `.env` file."""

    base_dir: Path = Path(__file__).resolve().parent
    database_path: Path = base_dir / "../database.db"
    model_config = SettingsConfigDict(env_file=".env")

    page_count_to_check: int = 5
    log_level: str = "INFO"
    telegram_api: str = ""
    template_dir: str = "templates"
    channel_id: int = 0


settings = Settings()
