from fastapi import FastAPI, Depends, HTTPException
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, schema


from .database import Base, engine

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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


@app.post("/token", response_model=schema.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    db_user = await crud.get_user_by_email(db, email=form_data.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    verification = await crud.verify_password(
        plain_password=form_data.password, hashed_password=db_user.hashed_password
    )
    if not verification:
        raise HTTPException(status_code=403, detail="Incorrect password")

    return {"access_token": db_user.email, "token_type": "bearer"}


@app.get("/")
async def root():
    return {
        "message": "Hello! Welcome to votingapp. Head on to the docs to get started."
    }


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


@app.get("/elections/", response_model=List[schema.Election])
async def read_elections(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await crud.get_elections(db, skip=skip, limit=limit)


@app.post("/elections/create", response_model=schema.Election)
async def create_election(
    user_id: int, election: schema.ElectionBase, db: AsyncSession = Depends(get_db)
):
    return await crud.create_election(db=db, election=election, user_id=user_id)


@app.post("/elections/{election_id}/add_candidate/", response_model=schema.Candidate)
async def create_election_candidate(
    election_id: int,
    candidate: schema.CandidateBase,
    db: AsyncSession = Depends(get_db),
):
    return await crud.create_election_candidate(
        db=db, candidate=candidate, election_id=election_id
    )


@app.get("/elections/{election_id}", response_model=List[schema.Candidate])
async def read_candidates(election_id: int, db: AsyncSession = Depends(get_db)):
    db_candidate = await crud.get_candidates(db, election_id=election_id)
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return db_candidate


# TODO: create vote as a list of character elements like
# preference = ['A', 'B', 'C','D']


@app.post("/elections/{election_id}/vote/", response_model=schema.Ballot)
async def create_ballot(
    election_id: int,
    owner_id: int,
    ballot: schema.BallotBase,
    db: AsyncSession = Depends(get_db),
):
    return await crud.create_election_ballot(
        db=db,
        ballot=ballot,
        election_id=election_id,
        owner_id=owner_id,
    )


@app.get("/elections/{election_id}/ballots", response_model=List[schema.Ballot])
async def read_ballots(election_id: int, db: AsyncSession = Depends(get_db)):
    db_ballot = await crud.get_ballots(db, election_id=election_id)
    if db_ballot is None:
        raise HTTPException(status_code=404, detail="Ballot not found")
    return db_ballot


@app.get("/elections/{election_id}/results")
async def read_ranking(election_id: int, db: AsyncSession = Depends(get_db)):

    return await crud.get_ranking(
        db=db,
        election_id=election_id,
    )
