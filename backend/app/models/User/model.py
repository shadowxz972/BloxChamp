from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from ...database.config import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    id_player = Column(BigInteger, ForeignKey("player.id"), index=True, unique=True, nullable=False)
    hashed_password = Column(String(500))
    role = Column(String(255), default="user")
    is_deleted = Column(Boolean, default=False)

    player = relationship("Player", back_populates="user", uselist=False)
