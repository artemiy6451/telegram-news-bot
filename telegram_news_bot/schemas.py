"""File with for program."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class Article(BaseModel):
    """Schema class for parsed article."""

    author: str
    name: str
    difficulty: Literal["Простой", "Средний", "Сложный"] | None
    time_to_read: str
    labels: tuple[str | None]
    tags: tuple[str | None]
    description: str | None
    published: datetime
    url: str
