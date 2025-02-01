from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ...database.config import Base


class TempPhrase(Base):
    __tablename__ = "temp_phrase"

    id = Column(Integer, primary_key=True, index=True)
    id_player = Column(BigInteger, ForeignKey("player.id"))
    phrase = Column(String(500))
    exp = Column(DateTime(timezone=True))

    player = relationship("Player")
