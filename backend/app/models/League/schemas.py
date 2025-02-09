from pydantic import BaseModel, AfterValidator
from typing import Annotated, Optional

class LeagueCreate(BaseModel):
    name:str
    description:Optional[str]
    tier:int

    class Config:
        extra = "forbid"

class LeagueResponse(BaseModel):
    id:int
    name:str
    description:Optional[str]
    tier:int
    is_deleted:bool
    is_active:bool

    class Config:
        from_attributes = True