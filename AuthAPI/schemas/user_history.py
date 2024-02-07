from pydantic import BaseModel, Field
from uuid import UUID


class UserHistory(BaseModel):
    user_agent: str = Field(description="The device user logined from")

    class Config:
        from_attributes = True


class UserHistoryCreate(BaseModel):
    uuid: UUID = Field(description="user id")
    user_agent: str = Field(description="The device user logined from")
