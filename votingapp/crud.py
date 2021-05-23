from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import model, ranking, schema

# TODO: isort

# Specify return types for all functions for type hints

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user(db: AsyncSession, user_id: int):
    db_execute = await db.execute(select(model.User).where(model.User.id == user_id))
    return db_execute.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str):
    db_execute = await db.execute(select(model.User).where(model.User.email == email))
    return db_execute.scalars().first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    db_execute = await db.execute(select(model.User).offset(skip).limit(limit))
    return db_execute.scalars().all()


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password):
    return pwd_context.hash(password)


# TODO: Remove plain password from POST request response
async def create_user(db: AsyncSession, user: schema.UserCreate):
    hashed_password = await get_password_hash(user.password)
    db_user = model.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_elections(db: AsyncSession, skip: int = 0, limit: int = 100):
    db_execute = await db.execute(select(model.Election).offset(skip).limit(limit))
    return db_execute.scalars().all()


async def create_election(
    db: AsyncSession, election: schema.ElectionBase, user_id: int
):
    db_election = model.Election(**election.dict(), owner_id=user_id)
    db.add(db_election)
    await db.commit()
    await db.refresh(db_election)
    return db_election


async def create_election_candidate(
    db: AsyncSession, candidate: schema.CandidateBase, election_id: int
):
    db_candidate = model.Candidate(**candidate.dict(), election_id=election_id)
    db.add(db_candidate)
    await db.commit()
    await db.refresh(db_candidate)
    return db_candidate


async def get_candidates(db: AsyncSession, election_id: int):
    db_execute = await db.execute(
        select(model.Candidate).where(model.Candidate.election_id == election_id)
    )
    return db_execute.scalars().all()


# TODO: create vote as a list of character elements like
# preference = ['A', 'B', 'C','D']


async def create_election_ballot(
    db: AsyncSession,
    ballot: schema.BallotBase,
    election_id: int,
    owner_id: int,
):
    db_ballot = model.Ballot(
        **ballot.dict(),
        election_id=election_id,
        owner_id=owner_id,
    )
    db.add(db_ballot)
    await db.commit()
    await db.refresh(db_ballot)
    return db_ballot


async def get_ballots(db: AsyncSession, election_id: int):
    db_execute = await db.execute(
        select(model.Ballot).where(model.Ballot.election_id == election_id)
    )
    return db_execute.scalars().all()


async def get_ranking(db: AsyncSession, election_id: int):
    pref = []
    ballots = await get_ballots(db, election_id)
    for ballot in ballots:
        pref.append(ballot.preference)
    results = ranking.schulze(pref)
    return results
