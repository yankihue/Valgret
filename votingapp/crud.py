from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from . import model, schema


async def get_user(db: AsyncSession, user_id: int):
    db_execute = await db.execute(select(model.User).where(model.User.id == user_id))
    return db_execute.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str):
    db_execute = await db.execute(select(model.User).where(model.User.email == email))
    return db_execute.scalars().first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    db_execute = await db.execute(select(model.User).offset(skip).limit(limit))
    return db_execute.scalars().all()


async def create_user(db: AsyncSession, user: schema.UserCreate):
    hashed_password = user.password
    db_user = model.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_items(db: AsyncSession, skip: int = 0, limit: int = 100):
    db_execute = await db.execute(select(model.Item).offset(skip).limit(limit))
    return db_execute.scalars().all()


async def create_user_item(db: AsyncSession, item: schema.ItemCreate, user_id: int):
    db_item = model.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def get_elections(db: AsyncSession, skip: int = 0, limit: int = 100):
    db_execute = await db.execute(select(model.Election).offset(skip).limit(limit))
    return db_execute.scalars().all()


async def create_election(
    db: AsyncSession, election: schema.ElectionCreate, user_id: int
):
    db_election = model.Election(**election.dict(), owner_id=user_id)
    db.add(db_election)
    await db.commit()
    await db.refresh(db_election)
    return db_election


async def create_election_candidate(
    db: AsyncSession, candidate: schema.CandidateCreate, election_id: int
):
    db_candidate = model.Candidate(**candidate.dict(), election_id=election_id)
    db.add(db_candidate)
    await db.commit()
    await db.refresh(db_candidate)
    return db_candidate


async def get_candidates(db: AsyncSession, skip: int = 0, limit: int = 100):
    db_execute = await db.execute(select(model.Candidate).offset(skip).limit(limit))
    return db_execute.scalars().all()

