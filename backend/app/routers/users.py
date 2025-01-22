

from fastapi import APIRouter, Depends, HTTPException, status
from ..models.User.schemas import UserCreate,UserResponse
from ..models.User.crud import create_user
from ..database.config import get_db
from ..models.TempPhrase.crud import create_temp_phrase


router = APIRouter()

@router.post("/new_user", response_model=UserResponse)
async def create_user_route(data:UserCreate,db=Depends(get_db)) -> UserResponse:
    try:

        new_user = await create_user(db,data)
        new_user.player.is_verified = True
        db.commit()
        db.refresh(new_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {e}")
    return new_user


@router.get("/temp_phrase/{player_id}")
async def temp_phrase_route(player_id:int, db=Depends(get_db)):
    return create_temp_phrase(db,player_id)