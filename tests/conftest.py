import pytest
from sqlmodel import SQLModel, create_engine, Session
from database.database import Database


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def db():
    return Database()
