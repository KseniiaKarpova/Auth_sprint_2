from pydantic import BaseModel


class Base0rjsonSchema(BaseModel):
    class Config:
        from_attrbutes = True
