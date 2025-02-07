from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, SmallInteger
from sqlalchemy.orm import relationship

from ...database.config import Base

class Tournament(Base):
    __tablename__ = 'tournament'

    id = Column(Integer, primary_key=True)
    id_league = Column(SmallInteger, ForeignKey('league.id'))
    edition = Column(String(255))
    prize = Column(Integer)
    is_finished = Column(Boolean, default=False)

    league = relationship('League', back_populates='tournaments')