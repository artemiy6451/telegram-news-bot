"""File for work with database."""

import sqlite3
import traceback

from loguru import logger

from telegram_news_bot.config import settings
from telegram_news_bot.schemas import Post
from telegram_news_bot.templates import render_template


class DataBase:
    """Class for interact with database."""

    def __init__(self) -> None:
        """Connect to database."""
        self.connection = sqlite3.connect(
            settings.database_path, check_same_thread=False
        )
        self.cursor = self.connection.cursor()

    def insert_post(self, post: Post) -> None:
        """Insert post to databsae."""
        insert_sql = render_template("database/insert_post.j2", post.model_dump())
        try:
            self.cursor.execute(insert_sql)
            self.connection.commit()
        except sqlite3.OperationalError as e:
            logger.error(f"Operational error: {e}\nSQL: {insert_sql}")
        except Exception:
            logger.error(f"Error while insert to database: {traceback.format_exc()}")

    def select_post(self, post: Post) -> list | None:
        """Select post form database."""
        select_sql = render_template("database/select_post.j2", post.model_dump())
        try:
            self.cursor.execute(select_sql)
            return self.cursor.fetchall()
        except sqlite3.OperationalError as e:
            logger.error(f"Operational error: {e}\nSQL: {select_sql}")
        except Exception:
            logger.error(f"Error while insert to database: {traceback.format_exc()}")


database_connection = DataBase()
