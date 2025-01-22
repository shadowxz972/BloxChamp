from fastapi import APIRouter, Depends
from ..models.League.crud import create_league, get_leagues
from ..models.League.schemas import LeagueCreate
from ..database.config import get_db
from typing import List
from ..models.Rule.schemas import RuleCreate, RuleResponse
from ..models.League.schemas import LeagueResponse
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, File, UploadFile, Form
from ..models.Trophy.model import Trophy
from ..models.Trophy.crud import create_trophy, get_trophy
from ..models.Trophy.schemas import TrophyResponse
from ..models.Rule.crud import create_rule, get_rules

router = APIRouter()


@router.post("/leagues", response_model=LeagueResponse)
async def create_league_route(data: LeagueCreate, db=Depends(get_db)):
    return create_league(db, data)


@router.get("/leagues/", response_model=List[LeagueResponse])
async def get_leagues_route(db=Depends(get_db)) -> List[LeagueResponse]:
    return get_leagues(db)


@router.post("/trophy", response_model=TrophyResponse)
async def create_trophy_route(
        db: Session = Depends(get_db),
        id_league: int = Form(...),
        name: str = Form(...),
        image: UploadFile = File(...)
) -> TrophyResponse:
    return await create_trophy(db, id_league, name, image)


@router.get("/trophy/{id_league}", response_model=TrophyResponse)
async def get_trophy_route(id_league: int, db: Session = Depends(get_db)) -> TrophyResponse:
    return get_trophy(db, id_league)


@router.post("/rules", response_model=RuleResponse)
async def create_rule_route(data: RuleCreate, db: Session = Depends(get_db)) -> RuleResponse:
    return create_rule(db, data)


@router.get("/rules/{id_league}", response_model=List[RuleResponse])
async def get_rules_route(id_league: int, db: Session = Depends(get_db)) -> List[RuleResponse]:
    return get_rules(db, id_league)
