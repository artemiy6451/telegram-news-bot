"""File with parser logic for site habr."""

from datetime import datetime
from http import HTTPStatus
from time import sleep
from typing import Literal

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from fake_headers import Headers
from loguru import logger

from telegram_news_bot.config import settings
from telegram_news_bot.schemas import Article

URL: str = "https://habr.com/ru/articles/page{}"


class Parser:
    """Class for parsing data from habr site."""

    def __init__(self) -> None:
        """Init parser."""
        logger.debug("Init parser.")
        self.session = requests.session()
        self.session.headers = Headers(
            browser="chrome", os="win", headers=True
        ).generate()

    def parse(self):
        """Parse data from first `n` pages of habr.

        Return list[Article] from all pages.
        """
        logger.debug("Parsig habr site.")
        articles: list[Article] = []
        for page_number in range(1, settings.page_count_to_check + 1):
            # page = self.__get_page(page_number)
            with open("index.html", "r") as file:
                page = file.read()
            if page is None:
                continue
            articles.extend(self.__parse_page(page, page_number))
            sleep(0.3)
        return articles

    def __parse_page(self, page, page_number) -> list[Article]:
        logger.debug(f"Parsig page #{page_number}.")
        soup = BeautifulSoup(page, "lxml")
        raw_articles: ResultSet = soup.find_all(
            "article", class_="tm-articles-list__item"
        )
        parsed_articles: list[Article] = []
        for article in raw_articles:
            parsed_articles.append(
                Article(
                    author=self.__parse_author(article),
                    name=self.__parse_name(article),
                    difficulty=self.__parse_difficulty(article),
                    time_to_read=self.__parse_time_to_read(article),
                    labels=self.__parse_labels(article),
                    tags=self.__parse_tags(article),
                    description=self.__parse_description(article),
                    published=self.__parse_published(article),
                    url=self.__parse_url(article),
                )
            )
        return parsed_articles

    def __parse_author(self, article) -> str | None:
        logger.debug("Parsing autor name.")
        try:
            author = article.find("a", class_="tm-user-info__username")
            return author.text.strip()
        except AttributeError as e:
            logger.debug(f"Can not parse author name: {e}")
            return None

    def __parse_name(self, article) -> str | None:
        logger.debug("Parsing article name.")
        try:
            name = article.find("h2", class_="tm-title").find("span")
            return name.text.strip()
        except AttributeError as e:
            logger.debug(f"Can not parse article name: {e}")
            return None

    def __parse_difficulty(
        self, article
    ) -> Literal["Простой", "Средний", "Сложный"] | None:
        logger.debug("Parsing article difficulty.")
        try:
            difficulty = article.find("span", class_="tm-article-complexity__label")
            return difficulty.text.strip()
        except AttributeError as e:
            logger.debug(f"Can not parse difficulty: {e}")
            return None

    def __parse_time_to_read(self, article) -> str | None:
        logger.debug("Parsing article time to read.")
        try:
            time_to_read = article.find("span", class_="tm-article-reading-time__label")
            return time_to_read.text.strip()
        except AttributeError as e:
            logger.debug(f"Can not parse time to read: {e}")
            return None

    def __parse_labels(self, content) -> tuple[str, ...] | None:
        logger.debug("Parsing article labels.")
        raw_labels = content.find_all("div", class_="tm-publication-label")
        parsed_labels: tuple[str, ...] = ()
        for label in raw_labels:
            try:
                parsed_labels += (label.find("span").text.strip(),)
            except AttributeError:
                parsed_labels += (label.find("a").text.strip(),)

        if parsed_labels:
            return parsed_labels
        return None

    def __parse_tags(self, article) -> tuple[str, ...] | None:
        logger.debug("Parsing article tags.")
        try:
            raw_tags = article.find_all("a", class_="tm-publication-hub__link")
            parsed_tags = tuple(
                tag.find("span", class_="").text.strip() for tag in raw_tags
            )
            return parsed_tags
        except AttributeError as e:
            logger.debug(f"Can not parse tags: {e}")
            return None

    def __parse_description(self, article) -> str | None:
        logger.debug("Parsing article descriptions.")
        try:
            paragraphs = article.find("div", class_="article-formatted-body").find_all(
                "p"
            )
            descriptions: str = "\n".join(
                (paragraph.text.strip() for paragraph in paragraphs)
            )
            return descriptions
        except AttributeError as e:
            logger.debug(f"Can not parse descriptions: {e}")
            return None

    def __parse_published(self, article) -> datetime | None:
        logger.debug("Parsing article published time.")
        try:
            raw_datetime = (
                article.find("a", class_="tm-article-datetime-published")
                .find("time")
                .get("datetime")
            )
            return datetime.fromisoformat(raw_datetime.replace("Z", "+00:00"))
        except AttributeError as e:
            logger.debug(f"Can not parse published time: {e}")
            return None

    def __parse_url(self, article) -> str | None:
        logger.debug("Parsing article url.")
        try:
            url = "https://habr.com" + article.find("a", class_="tm-title__link").get(
                "href"
            )
            return url
        except AttributeError as e:
            logger.debug(f"Can not parse url: {e}")
            return None

    def __get_page(self, page_number: int) -> str | None:
        logger.debug("Send get response to server.")
        self.response = self.session.get(URL.format(page_number))
        if self.response.status_code == HTTPStatus.OK:
            return self.response.text
        else:
            return None
