from sqlalchemy.future import select

from app.db.repositories.base import BaseRepository
from app.models.domain.url import URL


class URLRepository(BaseRepository):
    """
    Class representation for insert and query operations on the url table

    :param db_session: database session
    """

    def __init__(self, db_session):
        super().__init__(db_session)

    async def get_url_from_link(self, link: str):
        """Query the url in the database

        :param link: URL to be queried in the database
        """
        q = await self.db_session.execute(select(URL).where(URL.link == link))
        return q.scalars().first()
