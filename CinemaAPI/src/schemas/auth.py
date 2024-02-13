from pydantic import BaseModel
from uuid import UUID


class JWTUserData(BaseModel):
    login: str
    uuid: UUID
