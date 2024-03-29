"""File with parser logic for site habr."""

from http import HTTPStatus
from time import sleep

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from fake_headers import Headers
from loguru import logger

from telegram_news_bot.config import settings
from telegram_news_bot.parser import AbstarctParser
from telegram_news_bot.schemas import Post


class HabrParser(AbstarctParser):
    """Class for parsing data from habr site."""

    def __init__(self) -> None:
        """Init parser."""
        logger.debug("Init parser.")
        self.session = requests.session()
        self.session.headers = Headers(
            browser="chrome", os="win", headers=True
        ).generate()

    def parse(self, tags: list[str]) -> list[Post]:
        """Parse data from first `n` pages of habr.

        Return list[Post] from all pages.
        """
        logger.debug("Parsig habr site.")
        articles: list[Post] = []
        for tag in tags:
            articles.extend(self._collect_all_articles_by_tag(tag)[::-1])
        return articles

    def _collect_all_articles_by_tag(self, tag: str) -> list[Post]:
        """Parse all articles from habr by tag."""
        logger.debug(f"Parsig articles by tag {tag}.")
        articles: list[Post] = []
        for page_number in range(1, settings.page_count_to_check + 1):
            page = self._get_page(tag, page_number)
            if page is None:
                continue
            raw_articles = self._parse_raw_articles(page, page_number)
            articles.extend(self._transform_articles(raw_articles))
            sleep(settings.time_for_connect_to_server)
        return articles

    def _transform_articles(self, raw_articles: ResultSet) -> list[Post]:
        parsed_articles: list[Post] = []
        for article in raw_articles:
            parsed_articles.append(
                Post(
                    name=self._parse_name(article),
                    time_to_read=self._parse_time_to_read(article),
                    url=self._parse_url(article),
                )
            )
        return parsed_articles

    def _parse_raw_articles(self, page, page_number) -> ResultSet:
        logger.debug(f"Parsig page #{page_number}.")
        soup = BeautifulSoup(page, "lxml")
        raw_articles = soup.find_all("article", class_="tm-articles-list__item")
        return raw_articles

    def _parse_name(self, article) -> str:
        try:
            logger.debug("Parsing article name.")
            name = article.find("h2", class_="tm-title").find("span")
            return name.text
        except AttributeError as e:
            logger.debug(f"Can not parse name: {e}")
            return "Name"

    def _parse_time_to_read(self, article) -> str:
        logger.debug("Parsing article time to read.")
        try:
            time_to_read = article.find("span", class_="tm-article-reading-time__label")
            return time_to_read.text.strip()
        except AttributeError as e:
            logger.debug(f"Can not parse time to read: {e}\n {article}")
            return "0 min."

    def _parse_url(self, article) -> str:
        logger.debug("Parsing article url.")
        try:
            url = "https://habr.com" + article.find("a", class_="tm-title__link").get(
                "href"
            )
            return url
        except (AttributeError, TypeError) as e:
            logger.debug(f"Can not parse url: {e}")
            return "https://habr.com"

    def _get_page(self, tag: str, page_number: int) -> str | None:
        logger.debug("Send get response to server.")
        try:
            self.response = self.session.get(
                settings.habr_url.format(page=page_number, tag=tag), timeout=5
            )
            if self.response.status_code == HTTPStatus.OK:
                return self.response.text
            else:
                logger.warning(
                    f"""Something wrong with server: {
                        settings.habr_url.format(page=page_number, tag=tag)
                    }"""
                )
                return None
        except requests.exceptions.RequestException as e:
            logger.error(
                f"Request error: \n{e}\n{settings.habr_url.format(page_number, tag=tag)}"
            )
