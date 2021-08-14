from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base
from app.models.domain.url import URL


class WordCount(Base):
    __tablename__ = "wordcount"
    id = Column(Integer, primary_key=True)
    url_id = Column(Integer, ForeignKey(URL.id))
    word = Column(String)
    count = Column(Integer)

    url = relationship("URL", foreign_keys="WordCount.url_id")
