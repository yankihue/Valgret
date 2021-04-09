# Votingapp API

Votingapp is an open-source project that implements the [Schulze method](https://en.wikipedia.org/wiki/Schulze_method) of voting complete with a user interface and database. It was created for organizations of any size to provide tools for internal decision-making, public polling and transparency.

This module was written with [FastAPI](https://fastapi.tiangolo.com) using an asynchronous postgresql database. The complementary front end code can be found in [this repository]().
## Installation

Clone the repository and run:
```bash
poetry install
```
to install required dependencies. Afterwards, create an .env file containing:


```
SQLALCHEMY_DATABASE_URI = "postgresql+asyncpg://user:password@postgresserver/db"
```
Modify the connection string for your own database server. Votingapp uses [alembic](https://alembic.sqlalchemy.org/en/latest/) to manage migrations. 

You can run the app with:


```bash
uvicorn votingapp.main:app --reload
```
Afterwards you can check [localhost:8000/docs]() for interactive API docs and more info.
## Usage


For a full list of features and how to access them please refer to the [documentation](). 


## Contributing
Pull requests are welcome. 


## License
[GPL-3.0 License]()
