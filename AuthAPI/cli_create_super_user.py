import asyncio
import logging

import typer
from core import config
from core.hasher import DataHasher
from db import postgres
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from storages.user import UserStorage

settings = config.APPSettings()
logging.getLogger('asyncio').setLevel(logging.WARNING)


def create(login: str, password: str):
    try:
        async def save():
            postgres.async_engine = create_async_engine(
                settings.db_dsn,
                poolclass=QueuePool,
                pool_pre_ping=True, pool_size=20, pool_timeout=30)

            postgres.async_session_factory = sessionmaker(
                postgres.async_engine,
                expire_on_commit=False,
                autoflush=True,
                class_=AsyncSession)

            hashed_password = await DataHasher().generate_word_hash(secret_word=password)
            storage = UserStorage()
            await storage.create(params={
                'password': hashed_password,
                'login': login,
                'is_superuser': True,
            })
            await postgres.async_engine.dispose()

        asyncio.run(save())

        print(f"Creating Super User: {login}")

    except Exception as e:
        print('Can`t create Super User')
        print(e)


if __name__ == "__main__":
    typer.run(create)
