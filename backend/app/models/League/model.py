from sqlalchemy import Column, String, SmallInteger, Boolean
from sqlalchemy.orm import relationship

from ...database.config import Base


class League(Base):
    """
    Represents a sports league.

    This class is an ORM mapping that defines a league entity, its properties, and
    its relationships in the database. The purpose of this class is to store and
    manage information about a league, including its name, tier, and active
    status, along with its associated trophies and rules.

    :ivar id: The unique identifier for the league.
    :type id: int
    :ivar name: The name of the league, which must be unique.
    :type name: str
    :ivar tier: The tier of the league, represented as a small integer and must
        be unique.
    :type tier: int
    :ivar is_active: Indicates whether the league is actively in use.
    :type is_active: bool
    :ivar is_deleted: Indicates whether the league has been marked as deleted.
    :type is_deleted: bool
    :ivar trophy: The relationship to a single Trophy entity associated with
        the league. Defines a one-to-one relationship.
    :type trophy: Trophy or None
    :ivar rules: The relationship to multiple Rule entities associated with the
        league. Defines a one-to-many relationship.
    :type rules: List[Rule]
    """
    __tablename__ = "league"

    id = Column(SmallInteger, primary_key=True, index=True)
    name = Column(String(255), index=True, unique=True)
    tier = Column(SmallInteger, index=True, unique=True)
    description = Column(String(1000), default="Add a description")
    is_active = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    trophy = relationship("Trophy", back_populates="league", uselist=False)
    rules = relationship("Rule", back_populates="league", uselist=True)
