from pydantic import BaseModel


class Match(BaseModel):
    id: str
    date: str
    champion: str
    role: str
    result: str
    kills: int
    deaths: int
    assists: int
    duration_minutes: int
