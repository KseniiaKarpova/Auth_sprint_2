from elastic.config import settings as es_settings
from elastic.index_settings import settings
from elastic.mappings import genres_mappings, movies_mappings, persons_mappings
from elasticsearch.client import Elasticsearch


class Index:
    __index_name__ = None
    __settings__: dict = None
    __mappings__: dict = None
    __client__ = Elasticsearch([es_settings.url])

    @classmethod
    def put_data(cls, data: list):
        client, index, body = cls.__client__, cls.name(), cls.settings()
        client.indices.create(index=index, body=body, ignore=400)
        for document in data:
            datum = cls.remove_not_mapped_fields(data=dict(document))
            client.index(index=index, body=datum, id=datum['id'])
            print(datum, '----------saved----------')
        client.indices.refresh(index=index)

    @classmethod
    def settings(cls):
        index_settings = cls.__settings__
        index_settings.update({'mappings': cls.__mappings__})
        return index_settings

    @classmethod
    def name(cls):
        return cls.__index_name__

    @classmethod
    def create_index(cls):
        client, index, body = cls.__client__, cls.name(), cls.settings()
        client.indices.create(index=index, body=body, ignore=400)

    @classmethod
    def remove_not_mapped_fields(cls, data: dict):
        data_keys = data.copy()
        if len(cls.__mappings__['properties'].keys()) < len(data.keys()):
            for key in data_keys.keys():
                if not cls.__mappings__['properties'].get(key):
                    del data[key]
        else:
            raise TypeError

        return data


class MoviesIndex(Index):
    __index_name__ = 'movies'
    __settings__ = settings
    __mappings__ = movies_mappings


class PersonsIndex(Index):
    __index_name__ = 'persons'
    __settings__ = settings
    __mappings__ = persons_mappings


class GenresIndex(Index):
    __index_name__ = 'genres'
    __settings__ = settings
    __mappings__ = genres_mappings
