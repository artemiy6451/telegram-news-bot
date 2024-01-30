"""Parser for site `medium`."""

import json
from http import HTTPStatus
from time import sleep

import requests
from fake_headers import Headers
from loguru import logger

from telegram_news_bot.config import settings
from telegram_news_bot.schemas import Post
from telegram_news_bot.templates import render_template


class MediumParser:
    """Class for parsing data from medium site."""

    def __init__(self) -> None:
        """Init parser."""
        self.session = requests.session()
        self.session.headers = Headers(
            browser="chrome", os="win", headers=True
        ).generate()

    def parse(self) -> list[Post]:
        """Parse articles from medium site."""
        logger.debug("Parse medium articles.")
        articles: list[Post] = []
        for page_number in range(1, settings.page_count_to_check + 1):
            if settings.test_mode:
                logger.warning("Running with test mode!")
                with open(settings.base_dir / "../data" / "medium.html", "r") as file:
                    page = json.loads(file.read())
            else:
                page = self.__get_page(_from=page_number * 25, limit=25)
            if page is None:
                continue
            articles.extend(self.__parse_page(page, page_number))
            sleep(0.3)
        return articles

    def __parse_page(self, page: dict, page_number: int) -> list[Post]:
        logger.debug(f"Parsig page #{page_number}.")
        raw_articles = page["data"]["staffPicksFeed"]["items"]
        parsed_articles: list[Post] = []
        for article in raw_articles:
            parsed_articles.append(
                Post(
                    name=self.__parse_name(article),
                    time_to_read=self.__parse_time_to_read(article),
                    url=self.__parse_url(article),
                )
            )
        return parsed_articles

    def __parse_name(self, article: dict) -> str:
        logger.debug("Parse name.")
        return article["post"]["title"]

    def __parse_time_to_read(self, article: dict) -> str:
        logger.debug("Parse time to read.")
        return str(int(article["post"]["readingTime"])) + " min."

    def __parse_url(self, article: dict) -> str:
        logger.debug("Parse url.")
        return article["post"]["mediumUrl"]

    def __get_page(self, _from: int = 0, limit: int = 25) -> dict | None:
        logger.debug("Get medium page.")
        response = self.session.post(
            url=settings.medium_url,
            json=self.__get_rendered_query(_from=_from, limit=limit),
        )
        with open("data/medium.html", "wb") as file:
            file.write(response.content)
        if response.status_code == HTTPStatus.OK:
            return response.json()
        else:
            return None

    @staticmethod
    def __get_rendered_query(_from: int = 0, limit: int = 25) -> dict:
        data = {
            "from": _from,
            "limit": limit,
        }
        query = json.loads(render_template("medium_get_post_graphql.j2", data=data))
        return query
