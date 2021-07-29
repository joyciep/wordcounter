import re

import requests
from bs4 import BeautifulSoup
from starlette import status


class ScraperException(Exception):
    """Raised when scraper failed"""

    pass


class ScraperService:
    """
    Class representation for scraping web pages

    :param url: URL to scrape
    :param word: word to search in the web page
    """

    def __init__(self, url: str, word: str):
        self.url = url
        self.word = word

    def run_and_get_word_count(self) -> int:
        """Send request to the URL, parse returned content, and count words in the content"""
        r = requests.get(self.url)
        if r.status_code != status.HTTP_200_OK:
            raise ScraperException
        soup = BeautifulSoup(r.content, "html.parser")
        matches = soup(text=re.compile(f"{self.word}"))
        count = 0
        for match in matches:
            words = re.findall(fr"\b{self.word}\b", match)
            count = count + len(words)
        return count
