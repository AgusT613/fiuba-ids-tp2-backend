from fastapi import APIRouter, HTTPException

from dependencias.dependencias import DatabaseDep
from modelos.modelos import (
    Equipo,
    EquipooUpsert,
    Integrante,
    IntegranteUpsert,
    MovimientoAIntegrante,
    IntegranteDeEquipoUpsert,
)

router = APIRouter()


@router.get("/")
def listar_equipo(db: DatabaseDep) -> list[Equipo]:
    return db.listar_equipos()


@router.get("/{_id}", response_model=Equipo)
def obtener_equipo(db: DatabaseDep, _id: int) -> Equipo:
    return db.obtener_equipo(_id)


@router.post("/", response_model=Equipo, status_code=201)
def create(db: DatabaseDep, equipo_a_crear: EquipooUpsert) -> Equipo:
    equipo = db.add(equipo_a_crear)
    return equipo


@router.delete("/{_id}")
def delete(db: DatabaseDep, _id: int) -> Equipo:
    equipo = db.delete(_id)
    return equipo


@router.post("/{id_equipo}/integrantes", response_model=Integrante)
def agregar_integrante(
    db: DatabaseDep, id_equipo: int, integrante_a_agregar: IntegranteUpsert
):
    integrante = db.add_integrante(id_equipo, integrante_a_agregar)
    return integrante


@router.put("/{id_equipo}/integrantes/{id_integrante}")
def editar_integrante_equipo(
    db: DatabaseDep, id_equipo: int, id_integrante: int, body: IntegranteDeEquipoUpsert
):
    equipo = db.obtener_equipo(id_equipo)
    if len(body.movimientos) > 4:
        raise HTTPException(status_code=400, detail="Maximo 4 movimientos")
    for integrante in equipo.integrantes:
        if integrante.id == id_integrante:
            for movimiento_id in body.movimientos:
                movimiento = db.obtener_movimiento_simple(movimiento_id)
                if movimiento not in integrante.movimientos:
                    integrante.movimientos.append(movimiento)

            integrante.apodo = body.apodo

            return integrante


@router.put("/{id_equipo}")
def update(
    db: DatabaseDep, id_equipo: int, equipo_actualizado: EquipooUpsert
) -> Equipo:
    equipo = db.update_equipos(id_equipo, equipo_actualizado)
    return equipo


@router.post("/{id_equipo}/integrantes/{integrante_id}/movimientos")
def agregar_movimiento_integrante(
    db: DatabaseDep,
    id_equipo: int,
    integrante_id: int,
    id_movimiento: MovimientoAIntegrante,
):
    equipo = db.obtener_equipo(id_equipo)
    movimiento = None
    for integrante in equipo.integrantes:
        if integrante.id == integrante_id:
            movimiento = db.obtener_movimiento_simple(id_movimiento.id_movimiento)
            if movimiento and movimiento not in integrante.movimientos:
                if len(integrante.movimientos) == 4:
                    raise HTTPException(status_code=400, detail="Maximo 4 movimientos")
                integrante.movimientos.append(movimiento)
                return movimiento
    if not movimiento:
        raise HTTPException(status_code=404, detail="Integrante no encontrado")


@router.delete("/{id_equipo}/integrantes/{integrante_id}", response_model=Integrante)
def eliminar_integrante(
    db: DatabaseDep, id_equipo: int, integrante_id: int
) -> Integrante:
    integrante = db.delete_integrante(id_equipo, integrante_id)
    return integrante
