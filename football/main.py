from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from typing import List
import psycopg2
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello AcePred"}

@app.get("/matches")
def get_matches(db: Session = Depends(get_db)):
    matches = db.query(models.Match).options(
        selectinload(models.Match.league),
        selectinload(models.Match.home_team),
        selectinload(models.Match.away_team)
        ).all()
    return {
        "result": len(matches),
        "response": matches
        }


@app.get("/teams", response_model=List[schemas.Team])
def get_teams(db: Session = Depends(get_db)):
    teams = db.query(models.Team).all()
    return teams
