from pydantic import BaseModel
from datetime import datetime

class LeagueCreate(BaseModel):
    id: int
    name: str
    country: str


class League(LeagueCreate):

    class Config:
        orm_mode = True

class Team(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class Match(BaseModel):
    id: int
    datetime: datetime
    status: str
    league: League | None = None
    home_team: Team | None = None
    away_team: Team | None = None

    class Config:
        orm_mode = True
