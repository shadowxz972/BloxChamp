from pydantic import BaseModel
from typing import Optional

class RuleCreate(BaseModel):
    id_league:int
    name:str
    content:Optional[str]

class RuleResponse(BaseModel):
    id:int
    id_league:int
    name:str
    content:Optional[str]
    is_deleted:bool

    class Config:
        from_attributes = True