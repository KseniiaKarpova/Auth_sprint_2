from datetime import timedelta
from uuid import UUID

from core.config import settings
from core.hasher import DataHasher
from pydantic import BaseModel, Field, validator


class UserCredentials(BaseModel):
    login: str | None = Field(None, description="login")
    password: str
    email: str


class UserLogin(BaseModel):
    login: str
    password: str
    agent: str


class UserData(BaseModel):
    password: str
    email: str
    surname: str | None
    name: str | None


class AuthSettingsSchema(BaseModel):
    authjwt_secret_key: str = settings.auth.secret_key
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}
    authjwt_algorithm: str = "HS256"
    access_expires: int = timedelta(minutes=15)
    refresh_expires: int = timedelta(days=30)


class LoginResponseSchema(BaseModel):
    access_token: str = Field(description='Access token value')
    refresh_token: str | None = Field(None, description='Refresh token value')


class JWTUserData(BaseModel):
    login: str
    uuid: UUID


class UserUpdate(BaseModel):
    password: str = Field(None, description="new login")
    login: str = Field(None, description="new password")

    @validator("password")
    def hash_pass(cls, value):
        if not value:
            return None
        return DataHasher().sync_generater(secret_word=value)
