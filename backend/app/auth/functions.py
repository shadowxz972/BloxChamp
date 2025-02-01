from datetime import datetime, timezone, timedelta

from fastapi import HTTPException, status, Depends, Request
from jwt import PyJWTError, decode, encode
from sqlalchemy.orm import Session

from .config import pwd_context, oauth2_scheme
from ..config import SECRET_KEY, ALGORITHM
from ..constants import ACCESS_TOKEN_EXPIRE_MINUTES
from ..database.config import get_db
from ..models.User.model import User


# Funciones para manejar contraseñas
def hash_password(password: str) -> str:
    """
    Hashea la contraseña
    :param password:
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def verify_token(token: str):
    """
    Verifica el token JWT y retorna el user id
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se ha podido validar las credenciales",
    )
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if not user_id:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    return user_id


# Funciones para manejar la verificacion del usuario
def normalize_string(cadena):
    return " ".join(cadena.strip().lower().split())


def compare_normalized_strings(original_phrase, user_phrase):
    return normalize_string(original_phrase) == normalize_string(user_phrase)


def create_access_token(user: User):
    expiration = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user.id),
        "exp": expiration
    }
    token = encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_current_user(request: Request, db: Session = Depends(get_db), token_oauth=Depends(oauth2_scheme)) -> User:
    # Lee el token desde la cookie
    token = request.cookies.get("bloxchamp_session") or token_oauth
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se ha podido encontrar el token en la cookie"
        )

    user_id = verify_token(token)

    # Buscar el usuario en la base de datos
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se ha podido encontrar el usuario"
        )

    if user.is_deleted:
        raise HTTPException(
            status_code=401,
            detail="El usuario está eliminado"
        )

    return user
