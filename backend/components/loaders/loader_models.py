from pydantic import BaseModel


class SchemaParser(BaseModel):
    start: str
    end: str
