from pydantic import BaseModel


class DailyLogCreate(BaseModel):
    date: str
    games: int
    feeling: str
    notes: str


class DailyLog(DailyLogCreate):
    id: str
