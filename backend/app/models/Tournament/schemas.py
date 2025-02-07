from pydantic import BaseModel, Field


class TournamentBase(BaseModel):
    id_league: int = Field(ge=1)
    edition: str = Field(min_length=1)
    prize: int = Field(ge=0)


class TournamentCreate(TournamentBase):
    class Config:
        extra = "forbid"


class TournamentResponse(TournamentBase):
    id: int
    is_finished: bool
