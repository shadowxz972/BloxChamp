from typing import Annotated

from pydantic import BaseModel, AfterValidator

from ...schemas.LoginForm.helpers import validar_password


class UserCreate(BaseModel):
    id_player: int
    password: Annotated[str, AfterValidator(validar_password)]

    class Config:
        extra = "forbid"


class UserResponse(BaseModel):
    id: int
    id_player: int
    role: str
    is_deleted: bool


class UserChangePassword(BaseModel):
    old_password: Annotated[str, AfterValidator(validar_password)]
    new_password: Annotated[str, AfterValidator(validar_password)]
