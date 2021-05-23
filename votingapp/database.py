import os

from dotenv import find_dotenv, load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

# this line is to connect to our base dir and connect to our .env file
load_dotenv(find_dotenv())

# this is to access the db so any route can acccess the database session
SQLALCHEMY_DATABASE_URL = os.environ["SQLALCHEMY_DATABASE_URI"]
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
)

# SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:password@postgresserver/db"


Base = declarative_base()
