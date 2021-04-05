from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner", lazy="noload")
    elections = relationship("Election", back_populates="owner", lazy="noload")
    ballots = relationship("Ballot", back_populates="owner", lazy="noload")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


class Election(Base):
    __tablename__ = "elections"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    owner = relationship("User", back_populates="elections")
    candidates = relationship("Candidate", back_populates="owner", lazy="noload")
    ballots = relationship("Ballot", back_populates="election", lazy="noload")


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    info = Column(String, index=True)
    election_id = Column(Integer, ForeignKey("elections.id"))
    owner = relationship("Election", back_populates="candidates", lazy="noload")


class Ballot(Base):
    __tablename__ = "ballots"

    id = Column(Integer, primary_key=True, index=True)
    preference = Column(String, index=True)
    election_id = Column(Integer, ForeignKey("elections.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="ballots")
    election = relationship("Election", back_populates="ballots")

