from elasticsearch import AsyncElasticsearch
from typing import Optional

es: Optional[AsyncElasticsearch] = None


def get_elastic() -> AsyncElasticsearch:
    return es
