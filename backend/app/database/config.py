from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from ..config import MYSQL_ROOT_PASSWORD, MYSQL_DATABASE, ENV

DATABASE_URL = f"mysql+pymysql://root:{MYSQL_ROOT_PASSWORD}@mysql:3306/{MYSQL_DATABASE}" if ENV == "production" else f"sqlite:///./{MYSQL_DATABASE}.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if ENV != "production" else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Para heredar a los modelos
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
