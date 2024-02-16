movies_mappings = {
    "dynamic": "strict",
    "properties": {
        "id": {
            "type": "keyword"
        },
        "imdb_rating": {
            "type": "float"
        },
        "genre": {
            "type": "keyword"
        },
        "file": {
            "type": "text",
            "analyzer": "ru_en",
            "fields": {
                "raw": {
                    "type": "text"
                }
            }
        },
        "title": {
            "type": "text",
            "analyzer": "ru_en",
            "fields": {
                "raw": {
                    "type": "keyword"
                }
            }
        },
        "description": {
            "type": "text",
            "analyzer": "ru_en"
        },
        "director": {
            "type": "text",
            "analyzer": "ru_en"
        },
        "actors_names": {
            "type": "text",
            "analyzer": "ru_en"
        },
        "writers_names": {
            "type": "text",
            "analyzer": "ru_en"
        },
        "actors": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
                "id": {
                    "type": "keyword"
                },
                "name": {
                    "type": "text",
                    "analyzer": "ru_en"
                }
            }
        },
        "writers": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
                "id": {
                    "type": "keyword"
                },
                "name": {
                    "type": "text",
                    "analyzer": "ru_en"
                }
            }
        }
    }
}


persons_mappings = {
    "dynamic": "strict",
    "properties": {
        "id": {
            "type": "keyword"
        },
        "name": {
            "type": "text",
            "analyzer": "ru_en",
            "fields": {
                "raw": {
                    "type": "keyword"
                }
            }
        },
        "films": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
                "id": {
                    "type": "keyword"
                },
                "roles": {
                    "type": "text",
                    "analyzer": "ru_en"
                },
            }
        },
    }
}


genres_mappings = {
    "dynamic": "strict",
    "properties": {
        "id": {
            "type": "keyword"
        },
        "name": {
            "type": "text",
            "analyzer": "ru_en",
            "fields": {
                "raw": {
                    "type": "keyword"
                }
            }
        },
        "description": {
            "type": "text",
            "analyzer": "ru_en"
        },
    }
}
