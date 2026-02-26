from typing import Annotated, Generator
from fastapi import Depends
from sqlmodel import Session, create_engine
from constantes.constantes import SQLITE_FILE_PATH

engine = None


def init_engine():
    global engine
    engine = create_engine(f"sqlite:///{SQLITE_FILE_PATH}", echo=True)


def get_engine():
    return engine


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
