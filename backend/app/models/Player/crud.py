from fastapi import HTTPException, status
from httpx import AsyncClient
from sqlalchemy.orm import Session

from .model import Player
from .schemas import PlayerCreate, PlayerResponse, PlayerInfo


async def get_player_info(player_id: int) -> PlayerInfo:
    url = f"https://users.roblox.com/v1/users/{player_id}"
    url_image = f"https://thumbnails.roblox.com/v1/users/avatar?userIds={player_id}&size=420x420&format=Png&isCircular=false"
    try:
        async with AsyncClient() as client:
            response = await client.get(url)
            response = response.json()
            response_image = await client.get(url_image)
            response_image = response_image.json()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {e}")

    return PlayerInfo(
        id=response["id"],
        name=response["name"],
        display_name=response["displayName"],
        description=response["description"],
        image=response_image["data"][0]["imageUrl"]
    )


async def create_player(db: Session, data: PlayerCreate) -> PlayerResponse:
    existing_player = db.query(Player).filter(Player.id == data.id).first()
    if existing_player:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Player already exists")

    player_info = await get_player_info(data.id)
    player = Player(
        id=data.id,
        name=player_info.name,
        display_name=player_info.display_name,
        description=player_info.description,
        image=player_info.image
    )

    db.add(player)
    db.commit()
    return PlayerResponse.model_validate(player, from_attributes=True)


async def refresh_player_info(db: Session, player_id: int) -> PlayerResponse:
    player: Player = db.query(Player).filter(Player.id == player_id).first()

    if player is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")

    player_info = await get_player_info(player.id)
    player.name = player_info.name
    player.display_name = player_info.display_name
    player.description = player_info.description
    player.image = player_info.image
    db.commit()
    return PlayerResponse.model_validate(player, from_attributes=True)


def read_players(db: Session, skip: int = 0, limit: int = 50, hide_unverified: bool = False):
    if hide_unverified:
        return db.query(Player).filter(Player.is_verified == True).offset(skip).limit(limit).all()
    return db.query(Player).offset(skip).limit(limit).all()
