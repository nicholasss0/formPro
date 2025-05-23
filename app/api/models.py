from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    polss = relationship("Poll", back_populates="owner")
    votes = relationship("Vote", back_populates="user")


class Poll(Base):
    __tablename__ = "polls"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner =  relationship("User", back_populates="polls")
    options = relationship("Option", back_populates="poll")


class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    poll_id = Column(Integer, ForeignKey("polls.id"))

    poll = relationship("Poll", back_populates="options")
    votes = relationship("Vote", back_populates="option")


class Vote(Base):
    __tablename__= "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    option_id = Column(Integer, ForeignKey("options.id"))
    voted_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="votes")
    option = relationship("Option", back_populates="votes")