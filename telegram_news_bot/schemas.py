"""File with for program."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class Article(BaseModel):
    """Schema class for parsed article."""

    author: str | None
    name: str | None
    difficulty: Literal["Простой", "Средний", "Сложный"] | None
    time_to_read: str | None
    labels: tuple[str, ...] | None
    tags: tuple[str, ...] | None
    description: str | None
    published: datetime | None = datetime.now()
    url: str | None
