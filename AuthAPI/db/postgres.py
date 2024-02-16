from exceptions import integrity_error, server_error
from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

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
        except IntegrityError:
            error = integrity_error
        except Exception:
            error = server_error
        if error:
            await session.rollback()
            raise error
