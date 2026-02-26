from fastapi import APIRouter
from dependencias.dependencias import DatabaseDep
from modelos.modelos import Movimiento, MovimientoDetallado
from fastapi import HTTPException

router = APIRouter()


@router.get("/")
def obtener_movimientos(db: DatabaseDep) -> list[Movimiento]:
    return db.obtener_movimientos()


@router.get("/{id}")
def obtener_movimiento_id(db: DatabaseDep, id: int) -> MovimientoDetallado:
    movimiento = db.obtener_movimiento(id)

    if not movimiento:
        raise HTTPException(status_code=404, detail=f"Movimiento no encontrado")

    return movimiento
