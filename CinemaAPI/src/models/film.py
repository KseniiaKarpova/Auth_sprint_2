import uuid

from models.base import Base0rjsonModel


class BaseModelOrjson(Base0rjsonModel):
    id: uuid.UUID


class Film(BaseModelOrjson):
    title: str
    imdb_rating: float


class FilmDetail(BaseModelOrjson):
    title: str
    imdb_rating: float = None
    genre: list
    title: str
    description: str | None = None
    director: list = None
    actors: list = None
    writers: list = None
    file: str = None
