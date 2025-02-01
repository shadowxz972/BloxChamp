from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, SmallInteger
from sqlalchemy.orm import relationship

from ...database.config import Base


class Rule(Base):
    __tablename__ = "rule"

    id = Column(Integer, primary_key=True, index=True)
    id_league = Column(SmallInteger, ForeignKey("league.id"))
    name = Column(String(255), nullable=False)
    content = Column(String(500))
    is_deleted = Column(Boolean, default=False)

    league = relationship("League", back_populates="rules")
