from datetime import datetime, timezone

from .model import User
from .schemas import UserCreate,UserResponse
from ...models.TempPhrase.model import TempPhrase
from ...models.TempPhrase.crud import get_player_description
from ...auth.functions import hash_password,compare_normalized_strings
from sqlalchemy.orm import Session
from ...constants import valid_roles

async def create_user(db:Session,data:UserCreate) -> User:
    existing_user = db.query(User).filter(User.id_player == data.id_player).first()
    if existing_user:
        raise ValueError("User already exists")

    roblox_desc = await get_player_description(data.id_player)

    if roblox_desc is None:
        raise ValueError("Player not found")

    temp_desc:TempPhrase = db.query(TempPhrase).filter(TempPhrase.id_player == data.id_player).first()
    if temp_desc is None:
        raise ValueError("Temp phrase not found")

    if temp_desc.exp.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        db.delete(temp_desc)
        db.commit()
        raise ValueError("Temp phrase expired")

    if not compare_normalized_strings(temp_desc.phrase,roblox_desc):
        raise ValueError("Temp phrase not correct")

    user = User(
        id_player=data.id_player,
        hashed_password=hash_password(data.password)
    )

    db.delete(temp_desc)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_role_user(db:Session,id_user:int,role:str) -> UserResponse:
    user = db.query(User).filter(User.id == id_user).first()
    if user is None:
        raise ValueError("User not found")

    if role.lower() not in valid_roles:
        raise ValueError("Invalid role")

    user.role = role.lower()
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user, from_attributes=True)

