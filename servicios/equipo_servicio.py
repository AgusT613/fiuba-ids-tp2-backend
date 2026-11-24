from fastapi import HTTPException
from sqlmodel import Session
from database.database import Database
from modelos.mappers import map_integrante_tabla_to_dto, map_movimiento_tabla_to_dto
from modelos.modelos import Integrante, IntegranteDeEquipoUpsert, Movimiento
from modelos.modelos_de_la_db import EquipoTabla, PokemonTabla


class EquipoServicio:
    """Capa de servicios y reglas de negocio para Equipos e Integrantes."""

    MAX_MOVIMIENTOS_POR_INTEGRANTE = 4

    @classmethod
    def editar_integrante(
        cls,
        session: Session,
        db: Database,
        id_equipo: int,
        id_integrante: int,
        body: IntegranteDeEquipoUpsert,
    ) -> Integrante:
        """Actualiza el apodo y la lista de movimientos de un integrante de equipo."""
        if len(body.movimientos) > cls.MAX_MOVIMIENTOS_POR_INTEGRANTE:
            raise HTTPException(status_code=400, detail="Maximo 4 movimientos")

        equipo = session.get(EquipoTabla, id_equipo)
        if not equipo:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")

        for integrante in (equipo.integrantes or []):
            if integrante.id_integrante_dentro_del_grupo == id_integrante:
                integrante.movimientos_del_integrante = []
                pokemon_encontrado = session.get(PokemonTabla, integrante.id_pokemon)
                movimientos_mostrar = []

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
                return map_integrante_tabla_to_dto(
                    integrante, pokemon_encontrado, movimientos=movimientos_mostrar
                )

        raise HTTPException(
            status_code=404,
            detail=f"Integrante de id {id_integrante} no encontrado en este equipo",
        )

    @classmethod
    def agregar_movimiento_a_integrante(
        cls,
        session: Session,
        db: Database,
        id_equipo: int,
        id_integrante: int,
        id_movimiento: int,
    ) -> Movimiento:
        """Agrega un movimiento individual a un integrante validando límites y unicidad."""
        equipo = session.get(EquipoTabla, id_equipo)
        if not equipo:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")

        for integrante in (equipo.integrantes or []):
            if integrante.id_integrante_dentro_del_grupo == id_integrante:
                movimiento = db.get_movimiento_simple(session, id_movimiento)
                if not movimiento:
                    raise HTTPException(
                        status_code=404, detail="Movimiento no encontrado"
                    )

                ya_tiene_mov = any(
                    mov.id_movimiento == movimiento.id_movimiento
                    for mov in (integrante.movimientos_del_integrante or [])
                )
                if ya_tiene_mov:
                    raise HTTPException(status_code=400, detail="Movimiento Repetido")

                if (
                    len(integrante.movimientos_del_integrante or [])
                    >= cls.MAX_MOVIMIENTOS_POR_INTEGRANTE
                ):
                    raise HTTPException(status_code=400, detail="Maximo 4 movimientos")

                integrante.movimientos_del_integrante.append(movimiento)
                session.commit()
                return map_movimiento_tabla_to_dto(movimiento)

        raise HTTPException(status_code=404, detail="Integrante no encontrado")
