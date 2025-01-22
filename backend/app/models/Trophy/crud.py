import uuid
from pathlib import Path

from fastapi import HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session

from .model import Trophy
from .schemas import TrophyCreate, TrophyResponse
from ...config import ROOT_PATH
from ...models.League.model import League

domain = "http://localhost:5000"  # TODO: convertirlo en variable de entorno
UPLOAD_FOLDER = ROOT_PATH / "static" / "images" / "trophies"
Path(UPLOAD_FOLDER).mkdir(exist_ok=True, parents=True)


async def create_trophy(
        db: Session,
        id_league: int = Form(...),
        name: str = Form(...),
        image: UploadFile = File(...)
) -> TrophyResponse:
    data = TrophyCreate(id_league=id_league, name=name)
    tipos_mime_permitidos = ["image/jpeg", "image/png"]
    extensiones_permitidas = [".jpg", ".jpeg", ".png"]
    existing_trophy = db.query(Trophy).filter(Trophy.name == data.name or Trophy.id_league == data.id_league).first()
    is_league_exist = db.query(League).filter(League.id == data.id_league).first()

    if not is_league_exist:
        raise HTTPException(status_code=400, detail="League does not exist")
    if existing_trophy:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Trophy already exists")

    if image.content_type not in tipos_mime_permitidos:
        raise HTTPException(status_code=400,
                            detail=f"Tipo de archivo no permitido. Solo se permiten: {', '.join(tipos_mime_permitidos)}.")

    if not any(image.filename.lower().endswith(ext) for ext in extensiones_permitidas):
        raise HTTPException(status_code=400,
                            detail=f"Extensión no permitida. Solo se permiten archivos con extensiones: {', '.join(extensiones_permitidas)}.")

    file_path = Path(UPLOAD_FOLDER) / f"{str(uuid.uuid4())}-{image.filename}"

    with open(file_path, "wb") as buffer:  # esto crea la imagen
        buffer.write(await image.read())

    trophy = Trophy(
        id_league=data.id_league,
        name=data.name,
        image=f"{domain}/static/images/trophies/{file_path.name}"
    )
    db.add(trophy)
    db.commit()
    db.refresh(trophy)

    return TrophyResponse.model_validate(trophy)

def get_trophy(db: Session, id_league: int) -> TrophyResponse:
    return db.query(Trophy).filter(Trophy.id_league == id_league).first()
