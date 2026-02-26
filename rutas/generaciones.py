from fastapi import APIRouter
from modelos.modelos import Generacion
from dependencias.dependencias import DatabaseDep
from dependencias.dependencias_de_la_db import SessionDep

router = APIRouter()


@router.get("/")
def get_generaciones(session: SessionDep, db: DatabaseDep) -> list[Generacion]:
    return db.get_generaciones(session)
