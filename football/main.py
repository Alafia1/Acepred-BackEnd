from datetime import date, datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import DATE, cast, func
from sqlalchemy.orm import Session, selectinload
from typing import List
import psycopg2
from pydantic import BaseModel
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello AcePred"}

@app.get("/matches", response_model=List[schemas.Match])
def get_matches_on_date(date: date | None = None, league: int | None = None, team: int | None = None, db: Session = Depends(get_db)):
    if league and team and date:
        target_datetime = datetime.combine(date, datetime.min.time())
        next_datetime = target_datetime + timedelta(days=1)
        matches = db.query(models.Match).options(
        selectinload(models.Match.league),
        selectinload(models.Match.home_team),
        selectinload(models.Match.away_team)
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

@app.get("/date", response_model=List[schemas.Match])
def get_matches(date: date, db: Session = Depends(get_db)):
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

@app.get("/matches/{id}", response_model=schemas.Match )
def get_matches(id: int, db: Session = Depends(get_db)):
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
def get_teams(id: int, db: Session = Depends(get_db)):
    teams = db.query(models.Team).filter(models.Team.id == id).first()
    return teams

@app.get("/leagues", response_model=List[schemas.League])
def get_leagues(db: Session = Depends(get_db)):
    leagues = db.query(models.League).all()
    return leagues

