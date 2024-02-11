from uuid import UUID

from pydantic import BaseModel, Field


class UserHistory(BaseModel):
    user_agent: str = Field(description="The device user logined from")

    class Config:
        from_attributes = True


class UserHistoryCreate(BaseModel):
    uuid: UUID = Field(description="user id")
    user_agent: str = Field(description="The device user logined from")
