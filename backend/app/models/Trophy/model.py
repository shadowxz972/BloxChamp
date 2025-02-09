from sqlalchemy import Column, Integer, String, ForeignKey, SmallInteger
from ...database.config import Base
from sqlalchemy.orm import relationship

class Trophy(Base):
    __tablename__ = "trophy"

    id = Column(Integer, primary_key=True, index=True)
    id_league = Column(SmallInteger, ForeignKey("league.id"), unique=True, nullable=False)
    name = Column(String(255))
    image = Column(String(255))

    league = relationship("League", back_populates="trophy")