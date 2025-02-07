from sqlalchemy import Column, String, SmallInteger, Boolean, Integer
from sqlalchemy.orm import relationship

from ...database.config import Base


class League(Base):
    __tablename__ = "league"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), index=True, unique=True)
    tier = Column(SmallInteger, index=True, unique=True)
    description = Column(String(1000), default="Add a description")
    is_active = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    trophy = relationship("Trophy", back_populates="league", uselist=False)
    rules = relationship("Rule", back_populates="league", uselist=True)
    tournaments = relationship("Tournament", back_populates="league", uselist=True)
