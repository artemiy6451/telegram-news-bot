from http import HTTPStatus
from unittest.mock import Mock

import pytest
from bs4 import BeautifulSoup

from telegram_news_bot.parsers.habr import HabrParser


@pytest.fixture
def parser_instance():
    parser = HabrParser()
    parser.session = Mock()
    return parser


@pytest.fixture
def mock_succsessfull_response():
    mock_respose = Mock()
    mock_respose.status_code = HTTPStatus.OK
    return mock_respose


@pytest.fixture
def mock_fail_response():
    mock_respose = Mock()
    mock_respose.status_code = HTTPStatus.NOT_FOUND
    return mock_respose


@pytest.fixture
def soup_instance():
    def create_soup(html):
        return BeautifulSoup(html, "lxml")

    return create_soup
