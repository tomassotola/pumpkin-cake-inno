from pydantic import BaseModel


class Location(BaseModel):
    url: str
    meta: str


class Agent(BaseModel):
    meta: str
    locations: list[Location]


class Config(BaseModel):
    agent_name: str
