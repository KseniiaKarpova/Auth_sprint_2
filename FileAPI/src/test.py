import random
import string

import pytest
from core.config import bucket_settings
from db.minio import MinioStorage
from db.postgres import PostgresStorage
from db.proxy_storage import ProxyStorage
from fastapi import UploadFile
from services.file import FileService

pytest_plugins = ('pytest_asyncio',)


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@pytest.mark.asyncio
async def test_file_service_object_upload(mocker):
    mock_file = mocker.Mock(spec=UploadFile)
    mock_file.filename = 'movie.mp4'
    mock_file.content_type = 'mp4'
    mock_file.size = 256

    moke_proxy_storage = mocker.Mock(ProxyStorage)
    moke_proxy_storage.save.return_value = 'movie.mp4'
    service = FileService(moke_proxy_storage)
    result = await service.upload(mock_file)

    assert result == 'movie.mp4'
    moke_proxy_storage.save.assert_called_once()


@pytest.mark.asyncio
async def test_file_service_object_download(mocker):
    moke_proxy_storage = mocker.Mock(ProxyStorage)
    moke_proxy_storage.get.return_value = 'movie.mp4'
    service = FileService(moke_proxy_storage)
    short_name = randomword(10)
    result = await service.download(short_name=short_name)

    assert result == 'movie.mp4'
    moke_proxy_storage.get.assert_called_once_with(bucket=bucket_settings.bucket_movies, short_name=short_name)


@pytest.mark.asyncio
async def test_proxy_storage_object_get(mocker):
    moke_minio = mocker.Mock(MinioStorage)
    moke_minio.get.return_value = 'movie.mp4'
    moke_pg = mocker.Mock(PostgresStorage)
    moke_pg.get.return_value = 'path'

    short_name = randomword(10)

    storage = ProxyStorage(object_storage=moke_minio, path_storage=moke_pg)
    result = await storage.get(bucket=bucket_settings.bucket_movies, short_name=short_name)

    assert result == 'movie.mp4'
