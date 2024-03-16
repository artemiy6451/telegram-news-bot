"""Template for fabric classes."""

from abc import ABC, abstractmethod

from telegram_news_bot.parsers.habr import HabrParser
from telegram_news_bot.parsers.medium import MediumParser


class Fabric(ABC):
    """Template class for fabrics."""

    @abstractmethod
    def create_fabric(self):
        """Create new fabric method."""
        raise NotImplementedError


class HabrFabric(Fabric):
    def create_fabric(self):
        return HabrParser()


class MediumFabric(Fabric):
    def create_fabric(self):
        return MediumParser()
