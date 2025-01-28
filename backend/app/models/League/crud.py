from sqlalchemy.orm import Session
from .schemas import LeagueCreate, LeagueResponse
from .model import League
from fastapi import HTTPException, status
from typing import List
def create_league(db:Session, data:LeagueCreate) -> LeagueResponse:

    existing_league = db.query(League).filter(League.name == data.name).first()
    existing_tier = db.query(League).filter(League.tier == data.tier).first()
    if existing_league:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="League already exists")
    if existing_tier:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tier already exists")

    league = League(
        name=data.name,
        tier=data.tier,
        description=data.description
    )
    db.add(league)
    db.commit()
    db.refresh(league)

    return LeagueResponse.model_validate(league)

def get_leagues(db:Session) -> list[League]:
    return db.query(League).filter(League.is_deleted == False).order_by(League.tier).all()