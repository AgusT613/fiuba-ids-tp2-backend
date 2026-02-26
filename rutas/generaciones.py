from fastapi import APIRouter
from modelos.modelos import Generacion
from constantes.constantes import RUTA_GENERATION_NAMES_CSV
from dependencias.dependencias import DatabaseDep

router = APIRouter()


@router.get("/")
def listar_generaciones(db: DatabaseDep) -> list[Generacion]:
    return db.obtener_generaciones()
