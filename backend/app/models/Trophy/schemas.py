from pydantic import BaseModel


class TrophyCreate(BaseModel):
    id_league: int
    name: str

    class Config:
        extra = "forbid"


class TrophyResponse(BaseModel):
    id: int
    id_league: int
    name: str
    image: str

    class Config:
        from_attributes = True
