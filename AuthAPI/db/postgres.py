from fastapi import Depends
from exceptions import integrity_error, server_error
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

async_session_factory: sessionmaker | None = None
async_engine: AsyncEngine | None = None


def get_async_engine() -> AsyncEngine | None:
    return async_engine


def get_async_factory() -> sessionmaker:
    return async_session_factory


async def create_async_session(factory=Depends(get_async_factory)) -> AsyncSession:
    async with factory() as session:
        yield session


async def commit_async_session(session: AsyncSession):
    async with session:
        error = None
        try:
            await session.commit()
        except IntegrityError as err:
            error = integrity_error
        except Exception as err:
            error = server_error
        if error:
            await session.rollback()
            raise error
