from typing import Annotated, Generator
from fastapi import Depends
from sqlmodel import Session, create_engine
from config.settings import settings

engine = None


def init_engine(db_url: str | None = None):
    global engine
    url = db_url or settings.database_url
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    engine = create_engine(url, echo=True, connect_args=connect_args)


def get_engine():
    global engine
    if engine is None:
        init_engine()
    return engine


def get_session() -> Generator[Session, None, None]:
    with Session(get_engine()) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
