import uuid

from models.base import Base0rjsonModel


class Person(Base0rjsonModel):
    id: uuid.UUID
    name: str


class PersonDetails(Person):
    films: list
