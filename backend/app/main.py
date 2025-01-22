import time

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers.users import router as users_router
from .config import ENV, PORT
from .database.config import Base, engine
from .routers.players import router as players_router
from .routers.auth import router as auth_router
from .routers.leagues import router as leagues_router
from pathlib import Path
Base.metadata.create_all(bind=engine)

app = FastAPI()

static_path = "./backend/app/static" if ENV != "production" else "app/static"
Path(static_path).mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=static_path), name="static")
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(players_router, prefix="/players", tags=["players"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

app.include_router(leagues_router, prefix="/leagues", tags=["leagues"])


@app.get("/")
async def root():
    return {"message": "Bienvenido a BloxChamp!"}


directory_app = "app.main:app" if ENV == "production" else "backend.app.main:app"

if __name__ == "__main__":
    time.sleep(2) if ENV == "production" else None # para asegurar que se conecte el mysql
    uvicorn.run(
        app=directory_app,
        host="0.0.0.0" if ENV == "production" else "127.0.0.1",
        port=PORT,
        reload=True if ENV == "development" else False
    )
