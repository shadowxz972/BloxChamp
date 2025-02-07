from .model import Tournament
from sqlalchemy.orm import Session
from .schemas import TournamentCreate
from ..League.model import League

from fastapi import status, HTTPException


def create_tournament(db: Session, data: TournamentCreate) -> Tournament:

    existing_league = db.query(League).filter(League.id == data.id_league).first()

    if not existing_league:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="League not found")

    if existing_league.is_active:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="League already active")

    if not existing_league.trophy:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="League dont have trophy")

    tournament = Tournament(
        id_league=data.id_league,
        edition=data.edition,
        prize=data.prize,
    )

    db.add(tournament)
    db.commit()
    db.refresh(tournament)
    return tournament

def get_tournaments(db: Session):
    return db.query(Tournament).all()