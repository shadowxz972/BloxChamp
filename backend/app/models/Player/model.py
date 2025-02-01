from sqlalchemy import Column, String, Boolean, BigInteger
from sqlalchemy.orm import relationship

from ...database.config import Base


class Player(Base):
    __tablename__ = "player"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=False)
    name = Column(String(255))
    display_name = Column(String(255))
    description = Column(String(255))
    image = Column(String(255))
    is_verified = Column(Boolean, default=False)

    user = relationship("User", back_populates="player")
