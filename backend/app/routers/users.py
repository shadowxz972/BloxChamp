

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..auth.functions import get_current_user
from ..models.User.schemas import UserCreate,UserResponse
from ..models.User.crud import create_user, update_role_user
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
    return UserResponse.model_validate(new_user, from_attributes=True)


@router.get("/temp_phrase/{player_id}")
async def temp_phrase_route(player_id:int, db=Depends(get_db)):
    return create_temp_phrase(db,player_id)

@router.get("/update_role/{user_id}/{role}", response_model=UserResponse)
async def update_role_route(user_id:int,role:str, db:Session=Depends(get_db), user = Depends(get_current_user)):
    """
    Actualiza el rol de un usuario en el sistema, verificando previamente los permisos del usuario autenticado.
    Se requiere que el usuario tenga el rol de "admin" o "superadmin". Si no cumple con este requisito,
    se lanza una excepción HTTP. Este endpoint utiliza la función ``update_role_user`` para realizar
    la operación en la base de datos.
    """
    try:
        if user.role not in ["admin","superadmin"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to do this")

        if user.id == user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't change your own role")


        user = update_role_user(db,user_id,role)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}")
    return user
