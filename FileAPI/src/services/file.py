from functools import lru_cache

from fastapi import Depends, UploadFile

from core.config import bucket_settings
from db import AbstractStorage
from db.minio import MinioStorage
from db.postgres import PostgresStorage
from db.proxy_storage import ProxyStorage
from services import AbstractService


class FileService(AbstractService):
    def __init__(self, stopage: AbstractStorage):
        self.stopage = stopage

    async def upload(self, file: UploadFile) -> dict:
        data = await self.stopage.save(file=file,
                                       bucket=bucket_settings.bucket_movies,
                                       path=bucket_settings.movies_path,)
        return data

    async def download(self, short_name):
        data = await self.stopage.get(bucket=bucket_settings.bucket_movies,
                                           short_name=short_name,)
        return data


@lru_cache()
def get_file_service(
    minio: AbstractStorage = Depends(MinioStorage),
    pg: AbstractStorage = Depends(PostgresStorage),
) -> FileService:
    storage = ProxyStorage(minio, pg)
    return FileService(storage)
