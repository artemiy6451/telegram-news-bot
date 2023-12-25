"""File with for program."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class Label(BaseModel):
    """Schema class for label.

    `name`: str
    """

    name: str


class Tag(BaseModel):
    """Schema class for tag.

    `name`: str
    """

    name: str


class Post(BaseModel):
    """Schema class for parsed post."""

    author: str | None
    name: str | None
    difficulty: Literal["Простой", "Средний", "Сложный"] | None
    time_to_read: str | None
    labels: tuple[Label, ...] | None
    tags: tuple[Tag, ...] | None
    description: str | None
    published: datetime | None = datetime.now()
    url: str | None
