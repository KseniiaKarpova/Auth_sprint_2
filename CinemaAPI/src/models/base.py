import orjson
from models import orjson_dumps
from pydantic import BaseModel


class Base0rjsonModel (BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
