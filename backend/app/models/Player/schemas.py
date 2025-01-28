from pydantic import BaseModel

class PlayerCreate(BaseModel):
    id:int

    class Config:
        extra = "forbid"

class PlayerResponse(BaseModel):
    id:int
    name:str
    display_name:str
    description:str
    image:str
    is_verified:bool

    class Config:
        from_attributes = True

class PlayerInfo(BaseModel):
    id:int
    name:str
    display_name:str
    description:str
    image:str