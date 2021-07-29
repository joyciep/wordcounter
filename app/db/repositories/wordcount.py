from sqlalchemy.future import select
from loguru import logger

from app.db.repositories.base import BaseRepository
from app.db.repositories.url import URLRepository
from app.models.domain.wordcount import WordCount
from app.models.domain.url import URL


class WordCountRepository(BaseRepository):
    """
    Class representation for insert and query operations on the word count table

    :param db_session: database session
    """

    def __init__(self, db_session):
        super().__init__(db_session)
        self.url_repository = URLRepository(db_session)

    async def create_word_count(self, word: str, count: int, url: str):
        """Inserts the word, count, and the url to the database

        :param word: word to be inserted to the database
        :param count: word count to be inserted to the database
        :param url: URL to be inserted to the database
        """
        logger.info("saving word count in database")
        url_ = await self.url_repository.get_url_from_link(url)
        url_ = URL(link=url)
        new_word_count = WordCount(word=word, count=count)
        new_word_count.url = url_
        self.db_session.add(new_word_count)
        await self.db_session.commit()

    async def get_word_count(self, word: str, url: str):
        """Query the word and the url in the database

        :param word: word to be queried in the database
        :param url: URL to be queried in the database
        """
        logger.info("getting word count in database")
        q = await self.db_session.execute(
            select(WordCount).join(URL).where(WordCount.word == word, URL.link == url)
        )
        return q.scalars().first()
