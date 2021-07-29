from sqlalchemy import Column, Integer, String

from app.db.session import Base


class URL(Base):
    __tablename__ = "url"
    id = Column(Integer, primary_key=True)
    link = Column(String)
