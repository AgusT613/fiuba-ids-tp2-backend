from fastapi import APIRouter, HTTPException

from dependencias.dependencias import DatabaseDep
from dependencias.dependencias_de_la_db import SessionDep
from modelos.modelos import (
    Equipo,
    EquipooUpsert,
    Generacion,
    Integrante,
    IntegranteUpsert,
    Movimiento,
    MovimientoAIntegrante,
    IntegranteDeEquipoUpsert,
    EquipoListado,
    Pokemon,
    TipoMovimiento,
    PokemonIntegrante,
    Estadisticas,
    Tipo,
    Debilidad,
)
from modelos.modelos_de_la_db import (
    EquipoTabla,
    PokemonTabla,
)

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


@router.put("/{id_equipo}/integrantes/{id_integrante}")
def edit_integrante_de_equipo(
    session: SessionDep,
    db: DatabaseDep,
    id_equipo: int,
    id_integrante: int,
    body: IntegranteDeEquipoUpsert,
):
    equipo = session.get(EquipoTabla, id_equipo)
    movimientos_mostrar = []

    if len(body.movimientos) > 4:
        raise HTTPException(status_code=400, detail="Maximo 4 movimientos")
    for integrante in equipo.integrantes:
        if integrante.id_integrante_dentro_del_grupo == id_integrante:
            integrante.movimientos_del_integrante = []
            pokemon_encontrado = session.get(PokemonTabla, integrante.id_pokemon)
            for movimiento_id in body.movimientos:
                movimiento = db.get_movimiento_simple(session, movimiento_id)
                if not movimiento:
                    raise HTTPException(
                        status_code=404, detail="Movimiento no encontrado"
                    )
                if movimiento not in integrante.movimientos_del_integrante:
                    movimiento_mostrar = db.mostrar_por_metodo_de_mov(movimiento)
                    movimientos_mostrar.append(movimiento_mostrar)
                    integrante.movimientos_del_integrante.append(movimiento)
                else:
                    raise HTTPException(
                        status_code=400, detail="Un movimiento esta repetido"
                    )

            integrante.apodo = body.apodo
            session.commit()
            return Integrante(
                id=integrante.id_integrante_dentro_del_grupo,
                apodo=integrante.apodo,
                pokemon=PokemonIntegrante(
                    id=integrante.id_pokemon,
                    nombre=pokemon_encontrado.nombre,
                    imagen=pokemon_encontrado.imagen,
                    estadisticas=Estadisticas(
                        ataque=integrante.pokemon.ataque,
                        ataque_especial=integrante.pokemon.ataque_especial,
                        defensa=integrante.pokemon.defensa,
                        defensa_especial=integrante.pokemon.defensa_especial,
                        puntos_de_golpe=integrante.pokemon.puntos_de_golpe,
                        velocidad=integrante.pokemon.velocidad,
                    ),
                    generaciones=[
                        Generacion(
                            id=generacion.id_generacion,
                            nombre=generacion.nombre_generacion,
                        )
                        for generacion in pokemon_encontrado.generaciones
                    ],
                    tipos=[
                        Tipo(
                            debilidades=[
                                Debilidad(
                                    id=debilidad.id_debilidad, nombre=debilidad.nombre
                                )
                                for debilidad in tipo.debilidades
                            ],
                            nombre=tipo.nombre_tipo,
                            id=tipo.id_tipo,
                        )
                        for tipo in pokemon_encontrado.tipos
                    ],
                ),
                movimientos=movimientos_mostrar,
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


@router.post("/{id_equipo}/integrantes/{id_integrante}/movimientos")
def add_movimiento_a_integrante(
    session: SessionDep,
    db: DatabaseDep,
    id_equipo: int,
    id_integrante: int,
    id_movimiento: MovimientoAIntegrante,
):
    equipo = session.get(EquipoTabla, id_equipo)

    for integrante in equipo.integrantes:
        if integrante.id_integrante_dentro_del_grupo == id_integrante:
            movimiento = db.get_movimiento_simple(session, id_movimiento.id_movimiento)
            if not movimiento:
                raise HTTPException(status_code=404, detail="Movimiento no encontrado")
            ya_tiene_mov = any(
                mov.id_movimiento == movimiento.id_movimiento
                for mov in integrante.movimientos_del_integrante
            )
            if not ya_tiene_mov:
                if len(integrante.movimientos_del_integrante) == 4:
                    raise HTTPException(status_code=400, detail="Maximo 4 movimientos")
                integrante.movimientos_del_integrante.append(movimiento)
                session.commit()
                return Movimiento(
                    id=movimiento.id_movimiento,
                    nombre=movimiento.nombre,
                    generacion=Generacion(
                        id=movimiento.generacion.id_generacion,
                        nombre=movimiento.generacion.nombre_generacion,
                    ),
                    tipo=TipoMovimiento(
                        id=movimiento.tipo.id_tipo, nombre=movimiento.tipo.nombre_tipo
                    ),
                    categoria=movimiento.clase_de_daño,
                    potencia=movimiento.poder,
                    precision=movimiento.precision,
                    puntos_de_poder=movimiento.PP,
                    efecto=movimiento.efecto,
                )
            else:
                raise HTTPException(status_code=400, detail="Movimiento Repetido")
    raise HTTPException(status_code=404, detail="Integrante no encontrado")


@router.delete("/{id_equipo}/integrantes/{id_integrante}", response_model=Integrante)
def delete_integrante(
    session: SessionDep, db: DatabaseDep, id_equipo: int, id_integrante: int
) -> Integrante:
    integrante = db.delete_integrante(session, id_equipo, id_integrante)
    return integrante
