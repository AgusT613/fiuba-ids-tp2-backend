from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select, func
from modelos.modelos import (
    Equipo,
    Habilidades,
    IntegranteUpsert,
    Movimiento,
    EquipooUpsert,
    EquipoUpsert,
    Integrante,
    Tipo,
    MovimientoDetallado,
    Generacion,
    TipoMovimiento,
    EquipoListado,
    PokemonLista,
    Debilidad,
    Evoluciones,
    PokemonIntegrante,
    Estadisticas,
)
from modelos.mappers import map_integrante_tabla_to_dto, map_movimiento_tabla_to_dto
from modelos.modelos_de_la_db import (
    DebilidadTabla,
    EquipoTabla,
    IntegranteTabla,
    PokemonGeneracionTabla,
    PokemonTabla,
    HabilidadesTabla,
    EvolucionTabla,
    GeneracionTabla,
    PokemonTipoTabla,
    TipoDebilidadTabla,
    TipoTabla,
    MovimientoTabla,
    PokemonMovimientoAprendizajeTabla,
    PokemonHabilidadTabla,
)
from constantes.constantes import METODO_MOVIMIENTO
from modelos.filtros import FiltrosPokemon, FiltrosMovimiento
from utils.movimientos import filtrar_pokemones


class Database:
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
        habilidades = [
            Habilidades(id=habilidad.id_habilidad, nombre=habilidad.nombre_habilidad)
            for habilidad in session.exec(query).all()
        ]
        return habilidades

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

    def get_movimientos(
        self, session: Session, filtros: FiltrosMovimiento
    ) -> list[Movimiento]:
        query = (
            select(
                MovimientoTabla,
                GeneracionTabla,
                TipoTabla,
            )
            .join(
                GeneracionTabla,
                MovimientoTabla.id_generacion_del_movimiento
                == GeneracionTabla.id_generacion,
            )
            .join(
                TipoTabla, MovimientoTabla.id_tipo_del_movimiento == TipoTabla.id_tipo
            )
            .limit(filtros.limit)
            .offset(filtros.offset)
        )

        if filtros.nombre_parcial:
            query = query.where(
                MovimientoTabla.nombre.like(f"%{filtros.nombre_parcial}%")
            )
        if filtros.tipo:
            query = query.where(MovimientoTabla.id_tipo_del_movimiento == filtros.tipo)

        movimientos = []
        results = session.exec(query).all()

        for mov, generacion, tipo in results:
            movimiento = Movimiento(
                id=mov.id_movimiento,
                nombre=mov.nombre,
                generacion=Generacion(
                    id=generacion.id_generacion, nombre=generacion.nombre_generacion
                ),
                tipo=TipoMovimiento(id=tipo.id_tipo, nombre=tipo.nombre_tipo),
                categoria=mov.clase_de_daño,
                potencia=mov.poder,
                precision=mov.precision,
                puntos_de_poder=mov.PP,
                efecto=mov.efecto,
            )

            movimientos.append(movimiento)

        return movimientos

    def get_movimiento_simple(
        self, session: Session, movimiento_id: int
    ) -> MovimientoTabla:
        movimiento = session.get(MovimientoTabla, movimiento_id)

        if not movimiento:
            raise HTTPException(status_code=404, detail="Movimiento no encontrado")

        return movimiento

    def get_movimiento(
        self, session: Session, movimiento_id: int
    ) -> MovimientoDetallado:
        query = (
            select(MovimientoTabla, GeneracionTabla, TipoTabla)
            .where(MovimientoTabla.id_movimiento == movimiento_id)
            .join(
                GeneracionTabla,
                MovimientoTabla.id_generacion_del_movimiento
                == GeneracionTabla.id_generacion,
            )
            .join(
                TipoTabla, MovimientoTabla.id_tipo_del_movimiento == TipoTabla.id_tipo
            )
        )

        result = session.exec(query).first()

        if not result:
            raise HTTPException(status_code=404, detail="Movimiento no encontrado")

        mov, generacion, tipo = result[0], result[1], result[2]
        pokemon_por_huevo, pokemon_por_nivel, pokemon_por_maquina = filtrar_pokemones(
            movimiento_id
        )

        movimiento_detallado = MovimientoDetallado(
            id=mov.id_movimiento,
            nombre=mov.nombre,
            generacion=Generacion(
                id=generacion.id_generacion, nombre=generacion.nombre_generacion
            ),
            tipo=TipoMovimiento(id=tipo.id_tipo, nombre=tipo.nombre_tipo),
            categoria=mov.clase_de_daño,
            potencia=mov.poder,
            precision=mov.precision,
            puntos_de_poder=mov.PP,
            efecto=mov.efecto,
            pokemon_por_huevo=pokemon_por_huevo,
            pokemon_por_nivel=pokemon_por_nivel,
            pokemon_por_maquina=pokemon_por_maquina,
        )

        return movimiento_detallado

    def get_generaciones(self, session: Session) -> list[Generacion]:
        generaciones = []
        results = session.exec(select(GeneracionTabla)).all()

        for g in results:
            generacion = Generacion(id=g.id_generacion, nombre=g.nombre_generacion)
            generaciones.append(generacion)

        return generaciones

    def get_tipos_pokemon(self, session: Session, pokemon_id: int) -> list[TipoTabla]:
        query = (
            select(TipoTabla)
            .join(PokemonTipoTabla, PokemonTipoTabla.id_tipo == TipoTabla.id_tipo)
            .where(PokemonTipoTabla.id_pokemon == pokemon_id)
        )
        tipos = session.exec(query).all()
        for tipo in tipos:
            query = (
                select(DebilidadTabla)
                .join(
                    TipoDebilidadTabla,
                    TipoDebilidadTabla.fk_id_debilidad == DebilidadTabla.id_debilidad,
                )
                .where(TipoDebilidadTabla.fk_id_tipo == tipo.id_tipo)
            )
            debilidades = session.exec(query).all()
            tipo.debilidades = debilidades
        return [
            Tipo(
                id=tipo.id_tipo,
                nombre=tipo.nombre_tipo,
                debilidades=[
                    Debilidad(id=debilidad.id_debilidad, nombre=debilidad.nombre)
                    for debilidad in tipo.debilidades
                ],
            )
            for tipo in tipos
        ]

    def get_pokemones(
        self, session: Session, filtros: FiltrosPokemon
    ) -> list[PokemonLista]:
        query = (
            self.__build_query_filtros(filtros)
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
            [self.mostrar_por_metodo_de_mov(m) for m in movimientos_huevo],
            [self.mostrar_por_metodo_de_mov(m) for m in movimientos_maquina],
            [self.mostrar_por_metodo_de_mov(m) for m in movimientos_nivel],
        )

    def get_integrantes_equipo(
        self, session: Session, id_equipo: int
    ) -> list[Integrante]:
        query = (
            select(IntegranteTabla)
            .where(IntegranteTabla.id_equipo == id_equipo)
            .options(
                selectinload(IntegranteTabla.pokemon),
                selectinload(IntegranteTabla.movimientos_del_integrante),
            )
        )
        results = session.exec(query).all()
        return [map_integrante_tabla_to_dto(integrante) for integrante in results]

    def get_equipo(self, session: Session, id: int) -> Equipo:
        query = (
            select(EquipoTabla, GeneracionTabla)
            .join(
                GeneracionTabla,
                EquipoTabla.id_generacion_del_equipo == GeneracionTabla.id_generacion,
            )
            .where(EquipoTabla.id_equipo == id)
        )

        result = session.exec(query).first()

        if not result:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")
        equipo, generacion = result
        equipo = Equipo(
            id=equipo.id_equipo,
            nombre=equipo.nombre_equipo,
            generacion=Generacion(
                id=generacion.id_generacion, nombre=generacion.nombre_generacion
            ),
            integrantes=self.get_integrantes_equipo(session, id),
        )

        return equipo

    def get_equipos(self, session: Session) -> list[EquipoListado]:
        equipos = []
        equipos_encontrados = session.exec(
            select(EquipoTabla).options(
                selectinload(EquipoTabla.generacion),
                selectinload(EquipoTabla.integrantes),
            )
        ).all()
        for equipo in equipos_encontrados:
            equipos.append(
                EquipoListado(
                    id=equipo.id_equipo,
                    nombre=equipo.nombre_equipo,
                    generacion=Generacion(
                        id=equipo.id_generacion_del_equipo,
                        nombre=equipo.generacion.nombre_generacion
                        if equipo.generacion
                        else session.get(
                            GeneracionTabla, equipo.id_generacion_del_equipo
                        ).nombre_generacion,
                    ),
                    cantidad_integrantes=len(equipo.integrantes or []),
                )
            )

        return equipos

    def create_equipo(
        self, session: Session, equipo_a_crear: EquipooUpsert
    ) -> EquipoTabla:
        existente = session.exec(
            select(EquipoTabla).where(
                EquipoTabla.nombre_equipo == equipo_a_crear.nombre
            )
        ).first()
        if existente:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe un equipo con ese nombre: {equipo_a_crear.nombre}",
            )

        generacion = session.get(GeneracionTabla, equipo_a_crear.id_generacion)
        if not generacion:
            raise HTTPException(
                status_code=404,
                detail=f"La generación con id {equipo_a_crear.id_generacion} no existe",
            )

        nuevo_equipo = EquipoTabla(
            nombre_equipo=equipo_a_crear.nombre,
            id_generacion_del_equipo=equipo_a_crear.id_generacion,
        )
        session.add(nuevo_equipo)
        session.commit()
        session.refresh(nuevo_equipo)
        return Equipo(
            id=nuevo_equipo.id_equipo,
            nombre=nuevo_equipo.nombre_equipo,
            generacion=Generacion(
                id=nuevo_equipo.id_generacion_del_equipo,
                nombre=session.get(
                    GeneracionTabla, nuevo_equipo.id_generacion_del_equipo
                ).nombre_generacion,
            ),
            integrantes=[],
        )

    def delete_equipo(self, session: Session, id: int) -> Equipo:
        equipo = session.get(EquipoTabla, id)
        if equipo is None:
            raise HTTPException(
                status_code=404, detail=f"Equipo de id {id} no encontrado"
            )

        generacion_nombre = (
            equipo.generacion.nombre_generacion
            if equipo.generacion
            else session.get(
                GeneracionTabla, equipo.id_generacion_del_equipo
            ).nombre_generacion
        )
        equipo_borrado = Equipo(
            id=equipo.id_equipo,
            nombre=equipo.nombre_equipo,
            generacion=Generacion(
                id=equipo.id_generacion_del_equipo,
                nombre=generacion_nombre,
            ),
            integrantes=[
                map_integrante_tabla_to_dto(integrante)
                for integrante in (equipo.integrantes or [])
            ],
        )
        for integrante in (equipo.integrantes or []):
            session.delete(integrante)
        session.delete(equipo)
        session.commit()
        return equipo_borrado

    def update_equipo(
        self, session: Session, id_equipo: int, datos_actualizados: EquipooUpsert
    ) -> EquipoTabla:
        equipo = session.get(EquipoTabla, id_equipo)

        existente = session.exec(
            select(EquipoTabla).where(
                (EquipoTabla.nombre_equipo == datos_actualizados.nombre)
                & (EquipoTabla.id_equipo != id_equipo)
            )
        ).first()
        if existente:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe un equipo con ese nombre: {datos_actualizados.nombre}",
            )

        generacion = session.get(GeneracionTabla, datos_actualizados.id_generacion)
        if not generacion:
            raise HTTPException(
                status_code=404,
                detail=f"La generación con id {datos_actualizados.id_generacion} no existe",
            )
        for integrante in (equipo.integrantes or []):
            generacion_pokemon = session.get(
                PokemonGeneracionTabla,
                (integrante.id_pokemon, datos_actualizados.id_generacion),
            )
            if not generacion_pokemon:
                raise HTTPException(
                    status_code=400,
                    detail="Uno de los pokemones no es adecuado para la nueva generacion",
                )

        equipo.nombre_equipo = datos_actualizados.nombre
        equipo.id_generacion_del_equipo = datos_actualizados.id_generacion

        session.add(equipo)
        session.commit()
        session.refresh(equipo)
        generacion_nombre = (
            equipo.generacion.nombre_generacion
            if equipo.generacion
            else session.get(
                GeneracionTabla, equipo.id_generacion_del_equipo
            ).nombre_generacion
        )
        return Equipo(
            id=equipo.id_equipo,
            nombre=equipo.nombre_equipo,
            generacion=Generacion(
                id=equipo.id_generacion_del_equipo,
                nombre=generacion_nombre,
            ),
            integrantes=[
                map_integrante_tabla_to_dto(integrante)
                for integrante in (equipo.integrantes or [])
            ],
        )

    def add_integrante(
        self, session: Session, id_equipo: int, nuevo_integrante: IntegranteUpsert
    ) -> Integrante:
        gen_valida = False
        equipo_encontrado = session.get(EquipoTabla, id_equipo)
        if not equipo_encontrado:
            raise HTTPException(
                status_code=404,
                detail=f"El equipo con id {id_equipo} no existe",
            )
        pokemon_encontrado = session.get(PokemonTabla, nuevo_integrante.id_pokemon)
        if not pokemon_encontrado:
            raise HTTPException(
                status_code=404,
                detail=f"El pokemon con id {nuevo_integrante.id_pokemon} no existe",
            )
        for generacion in pokemon_encontrado.generaciones:
            if generacion.id_generacion == equipo_encontrado.id_generacion_del_equipo:
                gen_valida = True

        if not gen_valida:
            raise HTTPException(
                status_code=400,
                detail="Generación del pokemon no pertenece a la generación del equipo",
            )
        ids_ocupados = session.exec(
            select(IntegranteTabla.id_integrante_dentro_del_grupo).where(
                IntegranteTabla.id_equipo == id_equipo
            )
        ).all()
        max_id = 0
        for i in range(1, 7):
            if i not in ids_ocupados:
                max_id = i
                break

        if max_id == 0:
            raise HTTPException(
                status_code=400,
                detail="Se alcanzó la cantidad máxima de integrantes: 6",
            )
        integrante_creado = IntegranteTabla(
            id_integrante_dentro_del_grupo=max_id,
            apodo=nuevo_integrante.apodo,
            id_pokemon=nuevo_integrante.id_pokemon,
            id_equipo=id_equipo,
        )
        session.add(integrante_creado)
        session.commit()
        session.refresh(integrante_creado)

        return map_integrante_tabla_to_dto(integrante_creado, pokemon_encontrado)

    def delete_integrante(
        self, session: Session, id_equipo: int, integrante_id: int
    ) -> Integrante:
        equipo_encontrado = session.get(EquipoTabla, id_equipo)
        if not equipo_encontrado:
            raise HTTPException(
                status_code=404,
                detail=f"El equipo con id {id_equipo} no existe",
            )
        integrante = None
        for integrante_buscar in (equipo_encontrado.integrantes or []):
            if integrante_id == integrante_buscar.id_integrante_dentro_del_grupo:
                integrante = integrante_buscar

        if integrante is None:
            raise HTTPException(
                status_code=404,
                detail=f"Integrante de id {integrante_id} no encontrado en este equipo",
            )

        pokemon_encontrado = session.get(PokemonTabla, integrante.id_pokemon)
        integrante_dto = map_integrante_tabla_to_dto(integrante, pokemon_encontrado)
        session.delete(integrante)
        session.commit()
        return integrante_dto

    def __build_query_filtros(self, filtros: FiltrosPokemon):
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

        query = query.limit(filtros.limit).offset(filtros.offset)
        return query

    def mostrar_por_metodo_de_mov(self, mov: MovimientoTabla) -> Movimiento:
        return map_movimiento_tabla_to_dto(mov)
