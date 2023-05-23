from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class League(Base):
    __tablename__ = "league"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    
    # Define relationship to Match table
    matches = relationship('Match', back_populates='league')

class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    # Define relationship to Match table
    home_matches = relationship('Match', foreign_keys='Match.home_team_id', back_populates='home_team')
    away_matches = relationship('Match', foreign_keys='Match.away_team_id', back_populates='away_team')

class Match(Base):
    __tablename__ = "match"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    league_id = Column(Integer, ForeignKey('league.id'), nullable=False)
    home_team_id = Column(Integer, ForeignKey('team.id'), nullable=False)
    away_team_id = Column(Integer, ForeignKey('team.id'), nullable=False)
    datetime = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    
    # Define relationship to League & Team table
    league = relationship('League', back_populates='matches')
    home_team = relationship('Team', foreign_keys=[home_team_id], back_populates='home_matches')
    away_team = relationship('Team', foreign_keys=[away_team_id], back_populates='away_matches')
