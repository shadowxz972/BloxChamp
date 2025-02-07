import time
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import ENV, PORT, SUPERADMIN_ID
from .database.config import Base, engine, SessionLocal
from .models.User.crud import create_default_superadmin
from .routers.auth import router as auth_router
from .routers.leagues import router as leagues_router
from .routers.players import router as players_router
from .routers.users import router as users_router
from .routers.tournaments import router as tournaments_router
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app_fastapi: FastAPI):
    print("Starting up...")
    await create_default_superadmin(SessionLocal(), SUPERADMIN_ID)
    yield
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)

static_path = "./backend/app/static" if ENV != "production" else "app/static"
Path(static_path).mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=static_path), name="static")
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(players_router, prefix="/players", tags=["players"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

app.include_router(leagues_router, prefix="/leagues", tags=["leagues"])
app.include_router(tournaments_router, prefix="/tournaments", tags=["tournaments"])
@app.get("/")
async def root():
    return {"message": "Bienvenido a BloxChamp!"}


directory_app = "app.main:app" if ENV == "production" else "backend.app.main:app"

if __name__ == "__main__":
    time.sleep(2) if ENV == "production" else None  # para asegurar que se conecte el mysql
    uvicorn.run(
        app=directory_app,
        host="0.0.0.0" if ENV == "production" else "127.0.0.1",
        port=PORT,
        reload=True if ENV == "development" else False
    )
