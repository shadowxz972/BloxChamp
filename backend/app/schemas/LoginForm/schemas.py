from pydantic import BaseModel, Field, AfterValidator
from typing import Annotated
from .helpers import validar_password


class LoginForm(BaseModel):
    id_player: int = Field(description="Id del jugador de roblox")
    password: Annotated[str,AfterValidator(validar_password)] = Field( description="Contraseña con validaciones")

class Token(BaseModel):
    access_token: str
    token_type: str