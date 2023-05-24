from datetime import date, datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import DATE, cast, func
from sqlalchemy.orm import Session, selectinload
from typing import List
import psycopg2
from pydantic import BaseModel
from . import models, schemas, util
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello AcePred"}

@app.get("/matches", response_model=List[schemas.Match])
def get_matches(date: date | None = None, league: int | None = None, team: int | None = None, db: Session = Depends(get_db)):
    if league and team and date:
        target_datetime = datetime.combine(date, datetime.min.time())
        next_datetime = target_datetime + timedelta(days=1)
        matches = db.query(models.Match).options(
        selectinload(models.Match.league),
        selectinload(models.Match.home_team),
        selectinload(models.Match.away_team),
        ).filter(
        models.Match.league_id == league, 
        (models.Match.home_team_id == team) | (models.Match.away_team_id == team),
        models.Match.datetime >= target_datetime,
        models.Match.datetime < next_datetime
        ).all()
        return matches
    
    elif league and team:
        matches = db.query(models.Match).options(
            selectinload(models.Match.league),
            selectinload(models.Match.home_team),
            selectinload(models.Match.away_team)
            ).filter(models.Match.league_id == league, (models.Match.home_team_id == team) | (models.Match.away_team_id == team)).all()
        return matches
    
    elif league  and date:
        target_datetime = datetime.combine(date, datetime.min.time())
        next_datetime = target_datetime + timedelta(days=1)
        matches = db.query(models.Match).options(
        selectinload(models.Match.league),
        selectinload(models.Match.home_team),
        selectinload(models.Match.away_team)
        ).filter(
        models.Match.league_id == league,
        models.Match.datetime >= target_datetime,
        models.Match.datetime < next_datetime
        ).all()
        return matches
    
    elif team and date:
        target_datetime = datetime.combine(date, datetime.min.time())
        next_datetime = target_datetime + timedelta(days=1)
        matches = db.query(models.Match).options(
        selectinload(models.Match.league),
        selectinload(models.Match.home_team),
        selectinload(models.Match.away_team)
        ).filter( 
        (models.Match.home_team_id == team) | (models.Match.away_team_id == team),
        models.Match.datetime >= target_datetime,
        models.Match.datetime < next_datetime
        ).all()
        return matches
    
    elif league:
        matches = db.query(models.Match).options(
            selectinload(models.Match.league),
            selectinload(models.Match.home_team),
            selectinload(models.Match.away_team)
            ).filter(models.Match.league_id == league).all()
        return matches
    
    elif team:
        matches = db.query(models.Match).options(
            selectinload(models.Match.league),
            selectinload(models.Match.home_team),
            selectinload(models.Match.away_team)
            ).filter(
            (models.Match.home_team_id == team) | (models.Match.away_team_id == team)
            ).all()
        return matches
    elif date:
        target_datetime = datetime.combine(date, datetime.min.time())
        next_datetime = target_datetime + timedelta(days=1)
        matches = db.query(models.Match).options(
            selectinload(models.Match.league),
            selectinload(models.Match.home_team),
            selectinload(models.Match.away_team)
        ).filter(
        models.Match.datetime >= target_datetime,
        models.Match.datetime < next_datetime
        ).all()
        return matches

    matches = db.query(models.Match).options(
        selectinload(models.Match.league),
        selectinload(models.Match.home_team),
        selectinload(models.Match.away_team)
        ).all()
    return matches


@app.get("/matches/{id}", response_model=schemas.Match )
def get_matches_one(id: int, db: Session = Depends(get_db)):
    match = db.query(models.Match).options(
        selectinload(models.Match.league),
        selectinload(models.Match.home_team),
        selectinload(models.Match.away_team)
        ).filter(models.Match.id == id).first()
    return match

@app.get("/teams", response_model=List[schemas.Team])
def get_teams(db: Session = Depends(get_db)):
    teams = db.query(models.Team).all()
    return teams

@app.get("/teams/{id}", response_model=schemas.Team)
def get_teams_one(id: int, db: Session = Depends(get_db)):
    teams = db.query(models.Team).filter(models.Team.id == id).first()
    return teams

@app.get("/leagues", response_model=List[schemas.League])
def get_leagues(db: Session = Depends(get_db)):
    leagues = db.query(models.League).all()
    return leagues
 
@app.get("/test",)# response_model=List[schemas.League])
def get_test(db: Session = Depends(get_db)):
    matches = db.query(models.Match).options(
        selectinload(models.Match.league),
        selectinload(models.Match.home_team),
        selectinload(models.Match.away_team),
        ).all()
    print(type(matches))
    data = {"result": len(matches),
            "response": []}
    for match in matches:
        goals = db.query(models.Goal).filter(models.Goal.match_id == match.id).first()
        score = db.query(models.Score).filter(models.Score.match_id == match.id).first()
        li = {
            "id": match.id,
            "datetime": match.datetime,
            "status": match.status,
            "league": {
                "id": match.league.id,
                "name": match.league.name,
                "country": match.league.country
            },
            "team":{
                "home": {
                    "id": match.home_team.id,
                    "name": match.home_team.name,
                    "winner": util.winner(goals.home, goals.away)
                },
                "away": {
                    "id": match.away_team.id,
                    "name": match.away_team.name,
                    "winner": util.winner(goals.away, goals.home)
                }
            },
            "goals":{
                "home": goals.home,
                "away": goals.away
            },
            "score":{
                "halftime": {
                    "home": score.home_half,
                    "away": score.away_half
                },
                "fulltime": {
                    "home": score.home_full,
                    "away": score.away_full
                },
                "extra-time": {
                    "home": score.home_extra,
                    "away": score.away_extra
                },
                "fulltime": {
                    "home": score.home_penalties,
                    "away": score.away_penalties
                }
            }
        }
        data["response"].append(li)
    return data