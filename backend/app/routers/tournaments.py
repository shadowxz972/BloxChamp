from fastapi import APIRouter, Depends, HTTPException, status
from ..database.config import get_db
from sqlalchemy.orm import Session
from ..models.Tournament.schemas import TournamentCreate, TournamentResponse
from ..models.Tournament.crud import create_tournament, get_tournaments

from typing import List


router = APIRouter()

@router.post("/tournaments", response_model=TournamentResponse)
async def create_tournament_route(tournament_create: TournamentCreate, db: Session= Depends(get_db)):
    try:
        tournament = create_tournament(db, tournament_create)
        tournament.league.is_active = True
        db.commit()
        db.refresh(tournament)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"error: {e}")

    return tournament

@router.get("/tournaments", response_model=list[TournamentResponse])
async def get_tournaments_route(db: Session= Depends(get_db)):
    return get_tournaments(db)