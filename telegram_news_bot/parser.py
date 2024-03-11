"""File with template of parsers class."""

from abc import ABC, abstractmethod
from typing import Any

from bs4 import ResultSet
from pydantic import BaseModel

from telegram_news_bot.schemas import Post


class AbstarctParser(ABC):
    """Abstract class for parsers."""

    @abstractmethod
    def __init__(self) -> None:
        """Init parser."""
        raise NotImplementedError

    @abstractmethod
    def parse(self) -> list[Post]:
        """Parse all articles."""
        raise NotImplementedError

    @abstractmethod
    def _transform_articles(self) -> list[Post]:
        """Transform raw articles to post."""
        raise NotImplementedError

    @abstractmethod
    def _parse_raw_articles(self) -> ResultSet:
        """Parse raw articles from one page."""
        raise NotImplementedError

    @abstractmethod
    def _parse_name(self) -> str:
        """Parse name from article."""
        raise NotImplementedError

    @abstractmethod
    def _parse_time_to_read(self) -> str:
        """Parse time to read from article."""
        raise NotImplementedError

    @abstractmethod
    def _parse_url(self) -> str:
        """Parse url from article."""
        raise NotImplementedError

    @abstractmethod
    def _get_page(self) -> Any | None:
        """Get page or return None."""
        raise NotImplementedError


class ParserSchema(BaseModel):
    """Schema class for parser."""

    name: str
    verbose_name: str
    parser_obj: type[AbstarctParser]
