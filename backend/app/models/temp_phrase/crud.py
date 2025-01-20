from httpx import AsyncClient
from fastapi import HTTPException, status
from faker import Faker
from sqlalchemy.orm import Session
from .model import TempPhrase
from datetime import datetime, timedelta, timezone

async def get_player_description(player_id: int) -> str:
    url = f"https://users.roblox.com/v1/users/{player_id}"
    try:
        async with AsyncClient() as client:
            response = await client.get(url)
            response = response.json()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {e}")

    if response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")

    return response["description"]

fake = Faker("en_US")

def create_random_phrase(quantity=20) -> str:
    return " ".join(fake.words(nb=quantity))

def create_temp_phrase(db:Session, player_id) -> str:
    existing_temp_phrase = db.query(TempPhrase).filter(TempPhrase.id_player == player_id).first()
    if existing_temp_phrase:
        db.delete(existing_temp_phrase)
        db.commit()

    temp_phrase = TempPhrase(
        id_player=player_id,
        phrase=create_random_phrase(),
        exp= datetime.now(timezone.utc) + timedelta(minutes=15)
    )
    db.add(temp_phrase)
    db.commit()
    db.refresh(temp_phrase)

    return temp_phrase.phrase
