from fastapi import Depends
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
