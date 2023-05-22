from pydantic import BaseModel
from datetime import datetime

class League(BaseModel):
    id: int
    name: str
    country: str


class Team(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class Match(BaseModel):
    id: int
    datetime: datetime
    status: str
    league: League
    home_team_id: Team
    away_team_id: Team


