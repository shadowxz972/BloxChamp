from ...database.config import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    id_player = Column(Integer, ForeignKey("player.id"),index=True ,unique=True)
    hashed_password = Column(String(500))
    role = Column(String(255), default="user")
    is_deleted = Column(Boolean, default=False)

    player = relationship("Player", back_populates="user", uselist=False)