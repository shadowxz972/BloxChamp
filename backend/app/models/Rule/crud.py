from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from .model import Rule
from .schemas import RuleCreate, RuleResponse


def create_rule(db: Session, data: RuleCreate) -> RuleResponse:
    existing_rule = db.query(Rule).filter(Rule.name == data.name).first()
    if existing_rule:
        raise HTTPException(status_code=400, detail="Rule already exists")

    rule = Rule(
        id_league=data.id_league,
        name=data.name,
        content=data.content
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return RuleResponse.model_validate(rule)


def get_rules(db: Session, id_league: int):
    return db.query(Rule).filter(Rule.id_league == id_league).all()
