from pydantic import BaseModel, constr
from pydantic.networks import HttpUrl


class WordCountRequest(BaseModel):
    word: constr(min_length=1)
    url: HttpUrl


class WordCountResponse(BaseModel):
    status: str
    count: int
