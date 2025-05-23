from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class OptionCreate(BaseModel):
    text: str


class PollCreate(BaseModel):
    question: str
    options: List[OptionCreate]


class OptionOut(BaseModel):
    id: int
    text: str

    class Config:
        orm_mode = True

class PollOut(BaseModel):
    id: int
    question: str
    created_at: datetime
    owner_id: int
    options: List[OptionOut]

    class Config:
        orm_mode = True


class VoteCreate(BaseModel):
    option_id: int