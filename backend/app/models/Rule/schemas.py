from typing import Optional

from pydantic import BaseModel


class RuleCreate(BaseModel):
    id_league: int
    name: str
    content: Optional[str]

    class Config:
        extra = "forbid"


class RuleResponse(BaseModel):
    id: int
    id_league: int
    name: str
    content: Optional[str]
    is_deleted: bool

    class Config:
        from_attributes = True
