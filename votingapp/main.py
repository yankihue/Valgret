from fastapi import FastAPI, Depends, HTTPException
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, schema


from .database import Base, engine

app = FastAPI()


@app.on_event("startup")
async def start_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Dependency
async def get_db():
    session = AsyncSession(engine)
    try:
        yield session
    finally:
        await session.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/users/", response_model=schema.User)
async def create_user(user: schema.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schema.User])
async def read_users(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await crud.get_users(db, skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=schema.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schema.Item)
async def create_item_for_user(
    user_id: int, item: schema.ItemCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schema.Item])
async def read_items(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await crud.get_items(db, skip=skip, limit=limit)


@app.get("/elections/", response_model=List[schema.Election])
async def read_elections(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await crud.get_elections(db, skip=skip, limit=limit)


@app.post("/elections/create", response_model=schema.Election)
async def create_election(
    user_id: int, election: schema.ElectionCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_election(db=db, election=election, user_id=user_id)


@app.post("/elections/{election_id}/add_candidate/", response_model=schema.Candidate)
async def create_election_candidate(
    election_id: int,
    candidate: schema.CandidateCreate,
    db: AsyncSession = Depends(get_db),
):
    return await crud.create_election_candidate(
        db=db, candidate=candidate, election_id=election_id
    )


@app.get("/elections/{election_id}", response_model=List[schema.Candidate])
async def read_candidates(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await crud.get_candidates(db, skip=skip, limit=limit)
