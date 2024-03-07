"""File with template of parsers class."""

from abc import ABC, abstractmethod
from typing import Any

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
    def _parse_page(self) -> list[Post]:
        """Parse articles from one page."""
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


class Parser(BaseModel):
    """Schema class for parser."""

    name: str
    verbose_name: str
    parser_obj: type[AbstarctParser]
