"""File with for program."""

from pydantic import BaseModel


class Post(BaseModel):
    """Schema class for parsed post."""

    name: str
    time_to_read: str
    url: str
