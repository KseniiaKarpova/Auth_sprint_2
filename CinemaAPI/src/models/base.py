from pydantic import BaseModel


class Base0rjsonModel (BaseModel):
    class Config:
        from_attributes = True
