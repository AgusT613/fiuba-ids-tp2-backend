from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select
from constantes.constantes import METODO_MOVIMIENTO
from modelos.filtros import FiltrosPokemon
from modelos.mappers import map_movimiento_tabla_to_dto
from modelos.modelos import (
    Debilidad,
    Evoluciones,
    Generacion,
    Habilidades,
    PokemonLista,
    Tipo,
    TipoMovimiento,
)
from modelos.modelos_de_la_db import (
    DebilidadTabla,
    EvolucionTabla,
    GeneracionTabla,
    HabilidadesTabla,
    PokemonGeneracionTabla,
    PokemonHabilidadTabla,
    PokemonMovimientoAprendizajeTabla,
    PokemonTabla,
    PokemonTipoTabla,
    TipoDebilidadTabla,
    TipoTabla,
    MovimientoTabla,
)


class PokemonRepositorio:
    """Repositorio para consultas relacionadas con Pokemones, Tipos, Habilidades y Evoluciones."""

    def get_pokemon(self, session: Session, id: int) -> PokemonTabla:
        query = (
            select(PokemonTabla, GeneracionTabla, TipoTabla)
            .join(
                PokemonGeneracionTabla,
                PokemonGeneracionTabla.id_pokemon == PokemonTabla.id_pokemon,
            )
            .join(
                GeneracionTabla,
                GeneracionTabla.id_generacion == PokemonGeneracionTabla.id_generacion,
            )
            .join(
                PokemonTipoTabla, PokemonTipoTabla.id_pokemon == PokemonTabla.id_pokemon
            )
            .join(TipoTabla, TipoTabla.id_tipo == PokemonTipoTabla.id_tipo)
            .where(PokemonTabla.id_pokemon == id)
        )
        pokemon = session.exec(query).first()
        if not pokemon:
            raise HTTPException(status_code=404, detail="Pokémon no encontrado")

        return pokemon

    def get_habilidades(self, session: Session, id: int) -> list[Habilidades]:
        query = (
            select(HabilidadesTabla)
            .join(
                PokemonHabilidadTabla,
                PokemonHabilidadTabla.id_habilidad == HabilidadesTabla.id_habilidad,
            )
            .where(PokemonHabilidadTabla.id_pokemon == id)
        )
        return [
            Habilidades(id=habilidad.id_habilidad, nombre=habilidad.nombre_habilidad)
            for habilidad in session.exec(query).all()
        ]

    def get_evoluciones(self, session: Session, id: int) -> list[Evoluciones]:
        query = select(EvolucionTabla).where(EvolucionTabla.fk_id_pokemon == id)
        evoluciones = session.exec(query).all()

        return [
            Evoluciones(
                id=evo.id_evolucion,
                nombre=evo.nombre_evolucion,
                imagen=evo.imagen,
            )
            for evo in evoluciones
        ]

    def get_tipos_pokemon(self, session: Session, pokemon_id: int) -> list[TipoTabla]:
        query = (
            select(TipoTabla)
            .join(PokemonTipoTabla, PokemonTipoTabla.id_tipo == TipoTabla.id_tipo)
            .where(PokemonTipoTabla.id_pokemon == pokemon_id)
        )
        tipos = session.exec(query).all()
        for tipo in tipos:
            debilidades_query = (
                select(DebilidadTabla)
                .join(
                    TipoDebilidadTabla,
                    TipoDebilidadTabla.fk_id_debilidad == DebilidadTabla.id_debilidad,
                )
                .where(TipoDebilidadTabla.fk_id_tipo == tipo.id_tipo)
            )
            tipo.debilidades = session.exec(debilidades_query).all()
        return [
            Tipo(
                id=tipo.id_tipo,
                nombre=tipo.nombre_tipo,
                debilidades=[
                    Debilidad(id=debilidad.id_debilidad, nombre=debilidad.nombre)
                    for debilidad in (tipo.debilidades or [])
                ],
            )
            for tipo in tipos
        ]

    def get_pokemones(
        self, session: Session, filtros: FiltrosPokemon
    ) -> list[PokemonLista]:
        query = (
            self._build_query_filtros(filtros)
            .options(
                selectinload(PokemonTabla.generaciones),
                selectinload(PokemonTabla.tipos),
            )
        )
        pokemones = session.exec(query).all()
        return [
            PokemonLista(
                id=pokemon.id_pokemon,
                nombre=pokemon.nombre,
                imagen=pokemon.imagen,
                generaciones=[
                    Generacion(
                        id=generacion.id_generacion, nombre=generacion.nombre_generacion
                    )
                    for generacion in pokemon.generaciones
                ],
                tipos=[
                    TipoMovimiento(id=tipo.id_tipo, nombre=tipo.nombre_tipo)
                    for tipo in pokemon.tipos
                ],
            )
            for pokemon in pokemones
        ]

    def get_movimientos_pokemon(self, session: Session, pokemon_id: int):
        query = (
            select(
                MovimientoTabla, PokemonMovimientoAprendizajeTabla.metodo_de_aprendizaje
            )
            .join(
                PokemonMovimientoAprendizajeTabla,
                PokemonMovimientoAprendizajeTabla.id_movimiento
                == MovimientoTabla.id_movimiento,
            )
            .where(PokemonMovimientoAprendizajeTabla.id_pokemon == pokemon_id)
        )
        resultados = session.exec(query).all()

        movimientos_huevo = []
        movimientos_maquina = []
        movimientos_nivel = []

        for movimiento, metodo in resultados:
            if metodo == METODO_MOVIMIENTO["huevo"]:
                movimientos_huevo.append(movimiento)
            elif metodo == METODO_MOVIMIENTO["maquina"]:
                movimientos_maquina.append(movimiento)
            elif metodo == METODO_MOVIMIENTO["nivel"]:
                movimientos_nivel.append(movimiento)
        return (
            [map_movimiento_tabla_to_dto(m) for m in movimientos_huevo],
            [map_movimiento_tabla_to_dto(m) for m in movimientos_maquina],
            [map_movimiento_tabla_to_dto(m) for m in movimientos_nivel],
        )

    def _build_query_filtros(self, filtros: FiltrosPokemon):
        query = select(PokemonTabla)
        if filtros:
            if filtros.nombre_parcial:
                query = query.where(
                    PokemonTabla.nombre.like(f"%{filtros.nombre_parcial}%")
                )
            if filtros.tipo is not None:
                query = query.join(PokemonTipoTabla).where(
                    PokemonTipoTabla.id_tipo == filtros.tipo
                )

        return query.limit(filtros.limit).offset(filtros.offset)
