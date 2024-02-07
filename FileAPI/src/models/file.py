from uuid import UUID

from pydantic import BaseModel


class File(BaseModel):
    short_name: str
    filename: str
    file_type: str
    size: float
