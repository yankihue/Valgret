
<a href="https://github.com/yankihue/Valgret">
    <img src="/logo.png" alt="logo" title="Valgret" align="right" height="80" />
</a>

# Valgret API

Valgret is an open-source project that implements the [Schulze method](https://en.wikipedia.org/wiki/Schulze_method) of voting complete with a user interface and database. It was created for organizations of any size to provide tools for internal decision-making, public polling and transparency.

This module was written with [FastAPI](https://fastapi.tiangolo.com) using an asynchronous postgresql database. The complementary front end code can be found in [this repository]().
## Installation
Valgret uses [poetry](https://python-poetry.org/) for dependency management.

Clone the repository and run:
```bash
poetry install
```
to install required dependencies. Afterwards, create an .env file containing:


```
SQLALCHEMY_DATABASE_URI = "postgresql+asyncpg://user:password@postgresserver/db"
```
Modify the connection string for your own database server. 

#### Docker container example: 
For a postgresql docker image that was created with these settings:
```bash
docker run -d --name postgres -e POSTGRES_PASSWORD=admin -v ${HOME}/Desktop/postgres-data/:/var/lib/postgresql/data -p 5432:5432 postgres
```
the .env file will be
```
SQLALCHEMY_DATABASE_URI = "postgresql+asyncpg://postgres:admin@localhost/postgres"
```


Valgret uses [alembic](https://alembic.sqlalchemy.org/en/latest/) to manage migrations. 
```bash
alembic revision
alembic upgrade head
```

You can run the app with:


```bash
uvicorn votingapp.main:app --reload
```
Afterwards you can check [localhost:8000/docs]() for interactive API docs and more info.
## Usage


For a full list of features and how to access them please refer to the [documentation](). 

## Tests
Activate the virtual environment if you're not in it
```bash
poetry shell
```
and make sure a database server is running. To run the tests:
```bash
pytest
```

## Contributing
Pull requests are welcome. 


## License
[GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)
