import asyncio

import pytest_asyncio
from aiohttp import ClientSession
from functional.settings import test_settings


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name='aiohttp_session', scope='session')
async def aiohttp_session():
    session = ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(name='make_get_request')
def make_get_request(aiohttp_session: ClientSession):
    async def inner(endpoint, params=None):
        url = f"{test_settings.service_url}{endpoint}"
        async with aiohttp_session.get(url, params=params) as response:
            json, status = await response.json(), response.status
        return json, status
    return inner


@pytest_asyncio.fixture(name='make_post_request')
def make_post_request(aiohttp_session: ClientSession):
    async def inner(endpoint, json=None):
        url = f"{test_settings.service_url}{endpoint}"
        async with aiohttp_session.post(url, json=json) as response:
            json, status_code = await response.json(), response.status_code
        return json, status_code
    return inner
