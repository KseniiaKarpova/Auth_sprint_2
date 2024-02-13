from abc import abstractmethod
from uuid import UUID

from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch, NotFoundError
from storages.base_storage import BaseStorage
from utils.jaeger import tracer


class GenreBaseStorage(BaseStorage):
    @abstractmethod
    async def get_data_list(self) -> list | None:
        pass

    @abstractmethod
    async def get_data_by_id(self, id: UUID) -> dict | None:
        pass


class GenreElasticStorage(GenreBaseStorage):
    def __init__(self):
        self.elastic: AsyncElasticsearch = get_elastic()

    async def get_data_list(self):
        with tracer.start_as_current_span('elasticsearch-request'):
            try:
                doc = await self.elastic.search(index="genres")
                hits = doc['hits']['hits']
                genres = [hit['_source'] for hit in hits]
                return genres
            except NotFoundError:
                return None

    async def get_data_by_id(self, id: UUID) -> dict | None:
        try:
            with tracer.start_as_current_span('elasticsearch-request'):
                doc = await self.elastic.get(index="genres", id=id)
        except NotFoundError:
            return None
        return doc["_source"]
