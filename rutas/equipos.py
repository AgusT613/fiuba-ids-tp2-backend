from fastapi import APIRouter

from dependencias.dependencias import DatabaseDep
from dependencias.dependencias_de_la_db import SessionDep
from modelos.modelos import (
    Equipo,
    EquipoUpsert,
    EquipooUpsert,
    Integrante,
    IntegranteUpsert,
    Movimiento,
    MovimientoAIntegrante,
    IntegranteDeEquipoUpsert,
    EquipoListado,
)
from servicios.equipo_servicio import EquipoServicio

router = APIRouter()


@router.get("/")
def get_equipos(session: SessionDep, db: DatabaseDep) -> list[EquipoListado]:
    return db.get_equipos(session)


@router.get("/{id}", response_model=Equipo)
def get_equipo(session: SessionDep, db: DatabaseDep, id: int) -> Equipo:
    return db.get_equipo(session, id)


@router.post("/", response_model=Equipo, status_code=201)
def create_equipo(
    session: SessionDep, db: DatabaseDep, equipo_a_crear: EquipooUpsert
) -> Equipo:
    equipo = db.create_equipo(session, equipo_a_crear)

    return equipo


@router.delete("/{id}")
def delete_equipo(session: SessionDep, db: DatabaseDep, id: int) -> Equipo:
    equipo = db.delete_equipo(session, id)

    return equipo


@router.post("/{id_equipo}/integrantes", response_model=Integrante)
def create_integrante_de_equipo(
    session: SessionDep,
    db: DatabaseDep,
    id_equipo: int,
    integrante_a_agregar: IntegranteUpsert,
):
    integrante = db.add_integrante(session, id_equipo, integrante_a_agregar)

    return integrante


@router.put("/{id_equipo}/integrantes/{id_integrante}", response_model=Integrante)
def edit_integrante_de_equipo(
    session: SessionDep,
    db: DatabaseDep,
    id_equipo: int,
    id_integrante: int,
    body: IntegranteDeEquipoUpsert,
) -> Integrante:
    return EquipoServicio.editar_integrante(
        session, db, id_equipo, id_integrante, body
    )


@router.put("/{id_equipo}")
def update_equipo(
    session: SessionDep,
    db: DatabaseDep,
    id_equipo: int,
    equipo_actualizado: EquipooUpsert,
) -> Equipo:
    equipo = db.update_equipo(session, id_equipo, equipo_actualizado)

    return equipo


@router.post(
    "/{id_equipo}/integrantes/{id_integrante}/movimientos",
    response_model=Movimiento,
)
def add_movimiento_a_integrante(
    session: SessionDep,
    db: DatabaseDep,
    id_equipo: int,
    id_integrante: int,
    id_movimiento: MovimientoAIntegrante,
) -> Movimiento:
    return EquipoServicio.agregar_movimiento_a_integrante(
        session, db, id_equipo, id_integrante, id_movimiento.id_movimiento
    )


@router.delete("/{id_equipo}/integrantes/{id_integrante}", response_model=Integrante)
def delete_integrante(
    session: SessionDep, db: DatabaseDep, id_equipo: int, id_integrante: int
) -> Integrante:
    integrante = db.delete_integrante(session, id_equipo, id_integrante)
    return integrante
