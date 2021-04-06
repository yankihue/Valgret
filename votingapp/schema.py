from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class CandidateBase(BaseModel):
    info: str


class CandidateCreate(CandidateBase):
    pass


class Candidate(CandidateBase):
    id: int
    election_id: int

    class Config:
        orm_mode = True


class BallotBase(BaseModel):
    preference: str
    pass


class BallotCreate(BallotBase):
    pass


class Ballot(BallotBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class ElectionBase(BaseModel):
    title: str
    description: Optional[str] = None


class ElectionCreate(ElectionBase):
    pass


class Election(ElectionBase):
    id: int
    owner_id: int
    created_date: datetime
    candidates: List[Candidate] = []
    ballots: List[Ballot] = []

    class Config:
        orm_mode = True
