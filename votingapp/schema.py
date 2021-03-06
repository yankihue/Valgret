from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class CandidateBase(BaseModel):
    info: str


class Candidate(CandidateBase):
    id: int
    election_id: int

    class Config:
        orm_mode = True


class BallotBase(BaseModel):
    preference: str
    pass


class Ballot(BallotBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class ElectionBase(BaseModel):
    title: str
    description: Optional[str] = None


class Election(ElectionBase):
    id: int
    owner_id: int
    created_date: datetime
    candidates: List[Candidate] = []
    ballots: List[Ballot] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    elections: List[Election] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
