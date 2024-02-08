import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class Base0rjsonSchema(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
