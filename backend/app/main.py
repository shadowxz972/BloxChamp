import time

import uvicorn
from fastapi import FastAPI
from .routers.users import router as users_router
from .config import ENV, PORT
from .database.config import Base, engine
from .routers.players import router as players_router
from .routers.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(players_router, prefix="/players", tags=["players"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])


@app.get("/")
async def root():
    return {"message": "Bienvenido a BloxChamp!"}


directory_app = "app.main:app" if ENV == "production" else "backend.app.main:app"

if __name__ == "__main__":
    time.sleep(5) if ENV == "production" else None # para asegurar que se conecte el mysql
    uvicorn.run(
        app=directory_app,
        host="0.0.0.0" if ENV == "production" else "127.0.0.1",
        port=PORT,
        reload=True,
    )
