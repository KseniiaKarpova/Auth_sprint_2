import uuid

from models.base import Base0rjsonModel


class Genre(Base0rjsonModel):
    id: uuid.UUID
    name: str
    description: str | None = None
