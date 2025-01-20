from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from ...database.config import Base
from sqlalchemy.orm import relationship

class TempPhrase(Base):
    __tablename__ = "temp_phrase"

    id = Column(Integer, primary_key=True, index=True)
    id_player = Column(Integer, ForeignKey("player.id"))
    phrase = Column(String(500))
    exp = Column(DateTime(timezone=True))

    player = relationship("Player")
