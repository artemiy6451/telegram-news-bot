"""File with parser logic for site habr."""


import requests
from fake_headers import Headers


class Parser:
    """Class for parsing data from habr site."""

    def __init__(self) -> None:
        """Init method."""
        self.session = requests.session()
        self.session.headers = Headers(
            browser="chrome", os="win", headers=True
        ).generate()

        self.response = self.session.get()
