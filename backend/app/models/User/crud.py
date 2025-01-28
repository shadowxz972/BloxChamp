from datetime import datetime, timezone

from sqlalchemy.orm import Session

from .model import User
from .schemas import UserCreate, UserResponse, UserChangePassword
from ...auth.functions import hash_password, verify_password, compare_normalized_strings
from ...constants import valid_roles
from ...models.Player.crud import create_player
from ...models.Player.schemas import PlayerCreate
from ...models.TempPhrase.crud import get_player_description
from ...models.TempPhrase.model import TempPhrase


async def create_user(db: Session, data: UserCreate) -> User:
    existing_user = db.query(User).filter(User.id_player == data.id_player).first()
    if existing_user:
        raise ValueError("User already exists")

    roblox_desc = await get_player_description(data.id_player)

    if roblox_desc is None:
        raise ValueError("Player not found")

    temp_desc: TempPhrase = db.query(TempPhrase).filter(TempPhrase.id_player == data.id_player).first()
    if temp_desc is None:
        raise ValueError("Temp phrase not found")

    if temp_desc.exp.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        db.delete(temp_desc)
        db.commit()
        raise ValueError("Temp phrase expired")

    if not compare_normalized_strings(temp_desc.phrase, roblox_desc):
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


def update_role_user(db: Session, id_user: int, role: str) -> UserResponse:
    user = db.query(User).filter(User.id == id_user).first()
    if user is None:
        raise ValueError("User not found")

    if role.lower() not in valid_roles:
        raise ValueError("Invalid role")

    user.role = role.lower()
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user, from_attributes=True)


def change_password(db: Session, id_user: int, data: UserChangePassword) -> UserResponse:
    user: User = db.query(User).filter(User.id == id_user).first()
    if user is None:
        raise ValueError("User not found")

    if not verify_password(data.old_password, user.hashed_password):
        raise ValueError("Invalid password")

    user.hashed_password = hash_password(data.new_password)
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user, from_attributes=True)


async def create_default_superadmin(db: Session, id_player):
    if id_player is None:
        return
    existing_superadmin = db.query(User).filter(User.id_player == id_player or User.role == "superadmin").first()
    if existing_superadmin:
        return

    default_password = "Xpassword@10"

    superadmin = User(
        id_player=id_player,
        hashed_password=hash_password(default_password),
        role="superadmin"
    )

    await create_player(db, PlayerCreate(id=id_player))

    db.add(superadmin)
    db.commit()
    db.refresh(superadmin)

