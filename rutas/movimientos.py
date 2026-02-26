from fastapi import APIRouter, Depends
from dependencias.dependencias import DatabaseDep
from dependencias.dependencias_de_la_db import SessionDep
from modelos.filtros import FiltrosMovimiento
from modelos.modelos import Movimiento, MovimientoDetallado

router = APIRouter()


@router.get("/")
def get_movimientos(
    session: SessionDep, db: DatabaseDep, filtros: FiltrosMovimiento = Depends()
) -> list[Movimiento]:
    movimientos = db.get_movimientos(session, filtros)

    return movimientos


@router.get("/{id}")
def get_movimiento(
    session: SessionDep, db: DatabaseDep, id: int
) -> MovimientoDetallado:
    movimiento = db.get_movimiento(session, id)

    return movimiento
