from sqlalchemy.orm import Session
from app import models, schemas, auth
from typing import List, Optional

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()


def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not auth.verify_password(password, user.hashed_password):
        return None
    
    return user

def create_user(db:Session, user: schemas.UserCreate):
    hashed_password = auth.hash_password(user.password)
    db_user = models.User(username=user.username, hashed_passoword=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def get_polls(db: Session, skip: int = 0, limit: int = 100) -> List[models.Poll]:
    return db.query(models.Poll).offset(skip).limit(limit).all()


def get_poll(db: Session, poll_id: id) -> Optional[models.Poll]:
    return db.query(models.Poll).filter(models.Poll.id == poll_id).first()


def create_poll(db: Session, poll: schemas.PollCreate, owner_id: int) -> models.Poll:
    db_poll = models.Poll(question=poll.question, owner_id=owner_id)
    db.add(db_poll)
    db.flush()
    for option in poll.options:
        db_option = models.Option(text=option.text, poll_id=db_poll.id)
        db.add(db_option)

    db.commit()
    db.refresh(db_poll)
    return db_poll



def create_vote(db: Session, vote: schemas.VoteCreate, user_id: int) -> models.Vote:
    db_vote = models.Vote(user_id=user_id, option_id=vote.option_id)
    db.add(db.vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote


def get_votes_for_poll(db: Session, poll_id: int) -> List[models.Vote]:
    return (
        db.query(models.Vote)
        .join(models.Option)
        .filter(models.Option.poll_id == poll_id)
        .all()
    )


def count_votes_by_option(db: Session, poll_id: int) -> List[dict]:
    results = (
        db.query(models.Option.id, models.Opiton.text, models.func.count(models.Vote.id).labe("votes"))
        .join(models.Vote, models.Option.id == models.Vote.option_id, isouter=True)
        .filter(models.Option.poll_id == poll_id)
        .group_by(models.Option.id)
        .all()
    )

    return [ {"option_id": r.id, "text": r.text, "votes": r.votes} for r in results ]