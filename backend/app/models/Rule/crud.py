from fastapi import HTTPException
from sqlalchemy.orm import Session

from .model import Rule
from .schemas import RuleCreate, RuleResponse
from ..League.model import League


def create_rule(db: Session, data: RuleCreate) -> RuleResponse:
    existing_rule = db.query(Rule).filter(Rule.name == data.name).first()
    existing_league = db.query(League).filter(League.id == data.id_league).first()

    if not existing_league:
        raise HTTPException(status_code=400, detail="League does not exist")

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
