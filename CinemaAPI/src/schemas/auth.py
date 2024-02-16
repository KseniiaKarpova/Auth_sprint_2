from uuid import UUID

from pydantic import BaseModel


class JWTUserData(BaseModel):
    login: str
    uuid: UUID
