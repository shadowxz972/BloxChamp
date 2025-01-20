from fastapi import APIRouter, Depends

from ..auth.functions import get_current_user
from ..models.Player.crud import create_player, read_players
from ..database.config import get_db
from sqlalchemy.orm import Session
from ..models.Player.schemas import PlayerCreate, PlayerResponse
from typing import List

router = APIRouter()

@router.post("/players", response_model=PlayerResponse)
async def create_player_route(data: PlayerCreate,db:Session = Depends(get_db)) -> PlayerResponse:
    return await create_player(db,data)

@router.get("/players", response_model=List[PlayerResponse])
async def read_players_route(skip:int = 0, limit:int = 50,db:Session = Depends(get_db), user = Depends(get_current_user)):
    return read_players(db,skip,limit)