import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class PostgresSettings(BaseSettings):
    name: str = ...
    user: str = ...
    host: str = ...
    port: int = ...
    password: str = ...

    model_config: str = SettingsConfigDict(env_prefix='db_')

    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
    
settings = PostgresSettings()

engine = create_engine(
    settings.url,
    pool_pre_ping=True, pool_size=20, pool_timeout=30)

Base = declarative_base()
