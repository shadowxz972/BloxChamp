from typing import List

from fastapi import APIRouter, Depends
from fastapi import HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session

from ..auth.functions import get_current_user
from ..database.config import get_db
from ..models.League.crud import create_league, get_leagues
from ..models.League.schemas import LeagueCreate
from ..models.League.schemas import LeagueResponse
from ..models.Rule.crud import create_rule, get_rules
from ..models.Rule.schemas import RuleCreate, RuleResponse
from ..models.Trophy.crud import create_trophy, get_trophy
from ..models.Trophy.schemas import TrophyResponse

router = APIRouter()


@router.post("/", response_model=LeagueResponse)
async def create_league_route(data: LeagueCreate, db=Depends(get_db), user=Depends(get_current_user)):
    if user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to do this")

    return create_league(db, data)


@router.get("/", response_model=List[LeagueResponse])
async def get_leagues_route(db=Depends(get_db)):
    return get_leagues(db)


@router.post("/trophy", response_model=TrophyResponse)
async def create_trophy_route(
        db: Session = Depends(get_db),
        id_league: int = Form(...),
        name: str = Form(...),
        image: UploadFile = File(...),
        user=Depends(get_current_user)
) -> TrophyResponse:
    if user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to do this")

    return await create_trophy(db, id_league, name, image)


@router.get("/trophy/{id_league}", response_model=TrophyResponse)
async def get_trophy_route(id_league: int, db: Session = Depends(get_db)) -> TrophyResponse:
    trophy = get_trophy(db, id_league)
    if trophy is None:
        raise HTTPException(status_code=404, detail="Trophy not found")
    return trophy


@router.post("/rules", response_model=RuleResponse)
async def create_rule_route(data: RuleCreate, db: Session = Depends(get_db),
                            user=Depends(get_current_user)) -> RuleResponse:
    if user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to do this")
    return create_rule(db, data)


@router.get("/rules/{id_league}", response_model=List[RuleResponse])
async def get_rules_route(id_league: int, db: Session = Depends(get_db)) -> List[RuleResponse]:
    return get_rules(db, id_league)
