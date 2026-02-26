from typing import Annotated
from fastapi import Depends
from database.database import Database

__database_instancia = None


def inicializar_deps():
    global __database_instancia
    __database_instancia = Database()


def get_database() -> Database:
    global __database_instancia
    if __database_instancia is None:
        raise RuntimeError("La instancia de la base de datos no fue inicializada")
    return __database_instancia


DatabaseDep = Annotated[Database, Depends(get_database)]
