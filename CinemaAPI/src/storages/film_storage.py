from abc import abstractmethod
from uuid import UUID

from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch, NotFoundError
from storages.base_storage import BaseStorage
from utils.jaeger import tracer


class FilmBaseStorage(BaseStorage):
    @abstractmethod
    async def get_data_list(self, sort, genre_id: UUID, page_number: int, page_size: int) -> list:
        pass

    @abstractmethod
    async def get_data_by_id(self, id: UUID) -> dict | None:
        pass

    @abstractmethod
    async def search_data(self, query, page_number: int, page_size: int) -> list | None:
        pass


class FilmElasticStorage(FilmBaseStorage):
    def __init__(self):
        self.elastic: AsyncElasticsearch = get_elastic()

    async def search_data(self, query, page_number, page_size):
        search_query = {"query_string": {"default_field": "title", "query": query}}
        with tracer.start_as_current_span('elasticsearch-request'):
            docs = await self.elastic.search(
                index="movies",
                body={
                    "_source": ["id", "title", "imdb_rating"],
                    "from": (page_number - 1) * page_size,
                    "size": page_size,
                    "query": search_query,
                },
                params={"filter_path": "hits.hits._source"},
            )
        if not docs:
            return None
        return [film["_source"] for film in docs["hits"]["hits"]]

    async def get_data_by_id(self, id: UUID) -> dict | None:
        try:
            with tracer.start_as_current_span('elasticsearch-request'):
                doc = await self.elastic.get(index="movies", id=id)
        except NotFoundError:
            return None
        return doc["_source"]

    async def get_data_list(
        self, sort: str, genre: str, page_number: int, page_size: int
    ) -> list | None:
        if sort[0] == "-":
            sort = {sort[1:]: "desc"}
        else:
            sort = {sort: "asc"}
        filter_query = {"match_all": {}} if genre is None else {
            "match": {
                "genre": {
                    "query": genre,
                    "operator": "and",
                    "fuzziness": "AUTO"
                    }}}
        with tracer.start_as_current_span('elasticsearch-request'):
            docs = await self.elastic.search(
                index="movies",
                body={
                    "_source": ["id", "title", "imdb_rating"],
                    "sort": sort,
                    "from": (page_number - 1) * page_size,
                    "size": page_size,
                    "query": filter_query,
                },
                params={"filter_path": "hits.hits._source"},
            )
        if not docs:
            return None
        return [film["_source"] for film in docs["hits"]["hits"]]
