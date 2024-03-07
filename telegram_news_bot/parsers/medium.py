"""Parser for site `medium`."""

import json
from http import HTTPStatus
from time import sleep

import requests
from fake_headers import Headers
from loguru import logger

from telegram_news_bot.config import settings
from telegram_news_bot.parser import AbstarctParser
from telegram_news_bot.schemas import Post
from telegram_news_bot.templates import render_template


class MediumParser(AbstarctParser):
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
        return self._parse_all_tags()

    def _parse_all_tags(self) -> list[Post]:
        """Parse all pages for all tags."""
        logger.debug("Parse pages for all tags.")
        articles: list[Post] = []
        for tag in settings.medium_tags:
            articles.extend(self._parse_all_pages_for_tag(tag))
        return articles

    def _parse_all_pages_for_tag(self, tag: str) -> list[Post]:
        """Parse all pages from site for one tag."""
        logger.debug(f"Parse pages for {tag} tag.")
        articles: list[Post] = []
        for page_number in range(0, settings.page_count_to_check):
            if settings.test_mode:
                page = self.__test_mode_parse()
            else:
                page = self._get_page(_from=page_number * 25, limit=25, tag_slug=tag)
            if page is None:
                continue
            articles.extend(self._parse_page(page, page_number))
            sleep(settings.time_for_connect_to_server)
        return articles

    def _parse_page(self, page: dict, page_number: int) -> list[Post]:
        logger.debug(f"Parsig page #{page_number + 1}.")
        raw_articles = (
            page.get("data")
            .get("tagFromSlug")
            .get("viewerEdge")
            .get("recommendedPostsFeed")
            .get("items")
        )
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

    def _parse_name(self, article: dict) -> str:
        logger.debug("Parse name.")
        return article["post"]["title"]

    def _parse_time_to_read(self, article: dict) -> str:
        logger.debug("Parse time to read.")
        return str(int(article["post"]["readingTime"])) + " min."

    def _parse_url(self, article: dict) -> str:
        logger.debug("Parse url.")
        return article["post"]["mediumUrl"]

    def _get_page(self, tag_slug: str, _from: int = 0, limit: int = 25) -> dict | None:
        logger.debug("Get medium page.")
        try:
            response = self.session.post(
                url=settings.medium_url,
                json=self.__get_rendered_query(
                    _from=_from, limit=limit, tag_slug=tag_slug
                ),
            )
            with open(settings.data_dir / "medium.html", "wb") as file:
                file.write(response.content)
            if response.status_code == HTTPStatus.OK:
                return response.json()
            else:
                return None
        except requests.exceptions.ConnectionError as error:
            logger.error(f"Can not get medium page: \n{error}")

    def __test_mode_parse(self) -> dict | None:
        logger.warning("Running with test mode!")
        try:
            with open(settings.data_dir / "medium.html", "r") as file:
                page = json.loads(file.read())
            return page
        except Exception:
            page = self._get_page(_from=0, limit=25, tag_slug=settings.medium_tags[0])
            return page

    @staticmethod
    def __get_rendered_query(
        tag_slug: str,
        _from: int = 0,
        limit: int = 25,
    ) -> dict:
        data = {
            "from": _from,
            "limit": limit,
            "tag_slug": tag_slug,
        }
        query = json.loads(render_template("medium_get_post_graphql.j2", data=data))
        return query
