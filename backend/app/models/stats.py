from pydantic import BaseModel


class SummaryStats(BaseModel):
    total_games: int
    wins: int
    losses: int
    winrate: float
    average_kda: float


class ChampionStats(BaseModel):
    champion: str
    games: int
    wins: int
    winrate: float
    average_kda: float


class RoleStats(BaseModel):
    role: str
    games: int
    wins: int
    winrate: float
    average_kda: float


class StatsResponse(BaseModel):
    summary: SummaryStats
    champion_performance: list[ChampionStats]
    role_performance: list[RoleStats]
