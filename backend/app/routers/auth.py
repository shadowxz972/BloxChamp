from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database.config import get_db
from ..models.User.model import User
from ..schemas.LoginForm.schemas import LoginForm, Token
from ..auth.functions import verify_password,create_access_token

router = APIRouter()

def login(db: Session, user_credentials):

    user = db.query(User).filter(User.id_player == user_credentials.id_player).first()
    print(f"usuario: {user}")
    print(f"password: {user_credentials.password}")
    print(f"hash: {user.hashed_password}")
    print(f"comparacion: {verify_password(user_credentials.password, user.hashed_password)}")
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
    access_token = create_access_token(user)
    return access_token

@router.post("/login", response_model=Token)
async def login_route(user_credentials:LoginForm,db:Session = Depends(get_db)):
    access_token = login(db,user_credentials)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
async def login_for_access_token(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Este endpoint es para poder usar las rutas protegidas desde el swagger
    """

    data = LoginForm(id_player=int(data.username), password=data.password)
    print(data)
    access_token = login(db, data)
    print(access_token)
    return {"access_token": access_token, "token_type": "bearer"}