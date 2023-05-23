from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from typing import List
import psycopg2
from pydantic import BaseModel
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

user = {"id": 1, "user": "Wanted"}

data = [{"id": 1, "name": "Ismaila", "user": user}, {"id": 2, "name": "Muhammed", "user": user}]

class User(BaseModel):
    id: int
    user: str

class Data(BaseModel):
    id: int
    name: str
    user: User

@app.get("/")
def root():
    return {"message": "Hello AcePred"}

@app.get("/matches", response_model=List[schemas.Match])
def get_matches(db: Session = Depends(get_db)):
    matches = db.query(models.Match).options(
        selectinload(models.Match.league),
        selectinload(models.Match.home_team),
        selectinload(models.Match.away_team)
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

@app.get("/data", response_model=List[Data])
def get_data(db: Session = Depends(get_db)):
    
    return data