from unittest.mock import patch

import pytest

from telegram_news_bot.config import settings
from telegram_news_bot.schemas import Post


@pytest.fixture
def changed_settings():
    settings.page_count_to_check = 1
    yield


def test_parse_correctly(parser_instance, changed_settings):
    expected = Post(name="Test", time_to_read="5 min", url="https://habr.com/test")
    html = f"""
        <article class="tm-articles-list__item">
            <h2 class="tm-title"><span>{expected.name}</span></h2>
            <span class="tm-article-reading-time__label">{expected.time_to_read}</span>
            <a
                class="tm-title__link"
                href="{expected.url.replace('https://habr.com', '')}"></a>
        </article>
        """
    with patch("telegram_news_bot.parsers.habr.HabrParser._get_page") as mock_get_page:
        mock_get_page.return_value = html

        articles = parser_instance.parse()
        assert articles == [expected]
        assert len(articles) == 1


def test_parse_correctly_empty_page(parser_instance, changed_settings):
    expected = []
    html = ""
    with patch("telegram_news_bot.parsers.habr.HabrParser._get_page") as mock_get_page:
        mock_get_page.return_value = html

        articles = parser_instance.parse()
        assert articles == expected
