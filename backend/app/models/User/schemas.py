from pydantic import BaseModel, AfterValidator, Field
from ...schemas.LoginForm.helpers import validar_password
from typing import Annotated

class UserCreate(BaseModel):
    id_player:int
    password:Annotated[str,AfterValidator(validar_password)]


class UserResponse(BaseModel):
    id:int
    id_player:int
    role:str
    is_deleted:bool