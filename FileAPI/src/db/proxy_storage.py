import shortuuid
from db import AbstractStorage


class ProxyStorage(AbstractStorage):
    def __init__(self, object_storage, path_storage) -> None:
        self.object_storage = object_storage
        self.path_storage = path_storage

    async def save(self, file, bucket, path):
        short_name = shortuuid.uuid(name=file.filename)
        data = {
            'short_name': short_name,
            'filename': file.filename,
            'file_type': file.content_type,
            'size': file.size,
        }
        await self.path_storage.save(data, path+file.filename)
        await self.object_storage.save(file, bucket, path)
        return data

    async def get(self, bucket, short_name):
        path = await self.path_storage.get(short_name)
        result = await self.object_storage.get(bucket, path)
        return result
