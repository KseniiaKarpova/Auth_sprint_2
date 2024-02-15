from datetime import timedelta

from aiohttp import ClientSession
from db import AbstractStorage
from exceptions import file_not_found
from fastapi import UploadFile
from miniopy_async import Minio
from starlette.responses import StreamingResponse

minio: Minio = None


async def get_client() -> Minio:
    return minio


class MinioStorage(AbstractStorage):
    def __init__(self):
        self.client = minio

    async def save(self, file: UploadFile, bucket: str, path: str):

        await self.client.put_object(
            bucket_name=bucket, object_name=path + file.filename, data=file, length=-1, part_size=10 * 1024 * 1024,
        )

    async def get(self, bucket: str, path: str) -> StreamingResponse:
        try:
            session = ClientSession()
            result = await self.client.get_object(bucket, path, session)

            async def s3_stream():
                async for chunk in result.content.iter_chunked(32 * 1024):
                    yield chunk

            return StreamingResponse(
                content=s3_stream(),
                media_type='video/mp4',
                headers={'Content-Disposition': 'filename="movie.mp4"'}
            )
        except Exception:
            raise file_not_found

    async def get_presigned_url(self, bucket: str, path: str) -> str:
        return await self.client.get_presigned_url('GET', bucket, path, expires=timedelta(days=1), )
