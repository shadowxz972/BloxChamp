from fastapi import APIRouter, HTTPException, status, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database.config import get_db
from ..models.User.model import User
from ..schemas.LoginForm.schemas import LoginForm, Token
from ..auth.functions import verify_password,create_access_token

router = APIRouter()

def login(db: Session, user_credentials):

    user = db.query(User).filter(User.id_player == user_credentials.id_player).first()

    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    if user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El usuario esta eliminado"
        )
    return create_access_token(user)


@router.post("/login")
async def login_route(response:Response, user_credentials:LoginForm,db:Session = Depends(get_db)):
    access_token = login(db,user_credentials)
    response.set_cookie(
        key="bloxchamp_session",
        value=access_token,
        httponly=True,
        secure=False, #TODO: Activarlo cuando este configurado el frontend con https
        samesite="strict",
        max_age=3600,
    )
    return {"message": "Login successful"}


@router.post("/token", response_model=Token)
async def login_for_access_token(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Este endpoint es para poder usar las rutas protegidas desde el swagger
    """

    data = LoginForm(id_player=int(data.username), password=data.password)
    access_token = login(db, data)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("bloxchamp_session")
    return {"message": "logout successful"}