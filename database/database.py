from fastapi import HTTPException
from sqlmodel import Session, select, func
from modelos.modelos import (
    Equipo,
    Habilidades,
    IntegranteUpsert,
    Movimiento,
    EquipooUpsert,
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

    def get_tipos(self) -> list[Tipo]:
        tipos = self.session.exec(select(Tipo)).all()
        return tipos

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
            debilidadaes = session.exec(query).all()
            tipo.debilidades = debilidadaes
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
        query = self.__build_query_filtros(filtros)
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
                    for generacion in session.get(
                        PokemonTabla, pokemon.id_pokemon
                    ).generaciones
                ],
                tipos=[
                    TipoMovimiento(id=tipo.id_tipo, nombre=tipo.nombre_tipo)
                    for tipo in session.get(PokemonTabla, pokemon.id_pokemon).tipos
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
        integrantes = []
        query = select(IntegranteTabla).where(IntegranteTabla.id_equipo == id_equipo)

        results = session.exec(query).all()

        for integrante in results:
            pokemon_del_integrante = session.get(PokemonTabla, integrante.id_pokemon)
            movis = integrante.movimientos_del_integrante
            integrantes.append(
                Integrante(
                    id=integrante.id_integrante_dentro_del_grupo,
                    apodo=integrante.apodo,
                    pokemon=PokemonIntegrante(
                        id=integrante.id_pokemon,
                        nombre=pokemon_del_integrante.nombre,
                        imagen=pokemon_del_integrante.imagen,
                        estadisticas=Estadisticas(
                            ataque=pokemon_del_integrante.ataque,
                            ataque_especial=pokemon_del_integrante.ataque_especial,
                            defensa=pokemon_del_integrante.defensa,
                            defensa_especial=pokemon_del_integrante.defensa_especial,
                            puntos_de_golpe=pokemon_del_integrante.puntos_de_golpe,
                            velocidad=pokemon_del_integrante.velocidad,
                        ),
                        generaciones=[
                            Generacion(
                                id=generacion.id_generacion,
                                nombre=generacion.nombre_generacion,
                            )
                            for generacion in pokemon_del_integrante.generaciones
                        ],
                        tipos=[
                            Tipo(
                                id=tipo.id_tipo,
                                nombre=tipo.nombre_tipo,
                                debilidades=[
                                    Debilidad(
                                        id=debilidad.id_debilidad,
                                        nombre=debilidad.nombre,
                                    )
                                    for debilidad in tipo.debilidades
                                ],
                            )
                            for tipo in pokemon_del_integrante.tipos
                        ],
                    ),
                    movimientos=[
                        self.mostrar_por_metodo_de_mov(movi_integrante)
                        for movi_integrante in movis
                    ],
                )
            )

        return integrantes

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
        query = (
            select(
                EquipoTabla,
                GeneracionTabla,
                func.count(IntegranteTabla.id_integrante_dentro_del_grupo).label(
                    "cantidad_integrantes"
                ),
            )
            .join(
                GeneracionTabla,
                EquipoTabla.id_generacion_del_equipo == GeneracionTabla.id_generacion,
                isouter=True,
            )
            .join(
                IntegranteTabla,
                EquipoTabla.id_equipo == IntegranteTabla.id_equipo,
                isouter=True,
            )
        )

        equipos_encontrados = session.exec(select(EquipoTabla)).all()
        for equipo in equipos_encontrados:
            equipos.append(
                EquipoListado(
                    id=equipo.id_equipo,
                    nombre=equipo.nombre_equipo,
                    generacion=Generacion(
                        id=equipo.id_generacion_del_equipo,
                        nombre=session.get(
                            GeneracionTabla, equipo.id_generacion_del_equipo
                        ).nombre_generacion,
                    ),
                    cantidad_integrantes=len(equipo.integrantes),
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

        integrantes_equipo = equipo.integrantes
        equipo_borrado = Equipo(
            id=equipo.id_equipo,
            nombre=equipo.nombre_equipo,
            generacion=Generacion(
                id=equipo.id_generacion_del_equipo,
                nombre=session.get(
                    GeneracionTabla, equipo.id_generacion_del_equipo
                ).nombre_generacion,
            ),
            integrantes=[
                Integrante(
                    id=integrante_equipo.id_integrante_dentro_del_grupo,
                    apodo=integrante_equipo.apodo,
                    pokemon=PokemonIntegrante(
                        id=integrante_equipo.id_pokemon,
                        nombre=integrante_equipo.pokemon.nombre,
                        imagen=integrante_equipo.pokemon.imagen,
                        estadisticas=Estadisticas(
                            ataque=integrante_equipo.pokemon.ataque,
                            ataque_especial=integrante_equipo.pokemon.ataque_especial,
                            defensa=integrante_equipo.pokemon.defensa,
                            defensa_especial=integrante_equipo.pokemon.defensa_especial,
                            puntos_de_golpe=integrante_equipo.pokemon.puntos_de_golpe,
                            velocidad=integrante_equipo.pokemon.velocidad,
                        ),
                        generaciones=[
                            Generacion(
                                id=gen.id_generacion, nombre=gen.nombre_generacion
                            )
                            for gen in integrante_equipo.pokemon.generaciones
                        ],
                        tipos=[
                            Tipo(
                                id=tipo.id_tipo,
                                nombre=tipo.nombre_tipo,
                                debilidades=[
                                    Debilidad(
                                        id=debilidad.id_debilidad,
                                        nombre=debilidad.nombre,
                                    )
                                    for debilidad in tipo.debilidades
                                ],
                            )
                            for tipo in integrante_equipo.pokemon.tipos
                        ],
                    ),
                    movimientos=[
                        self.mostrar_por_metodo_de_mov(movi_integrante)
                        for movi_integrante in integrante_equipo.movimientos_del_integrante
                    ],
                )
                for integrante_equipo in integrantes_equipo
            ],
        )
        for integrante in equipo.integrantes:
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
        for integrantes in equipo.integrantes:
            generacion_pokemon = session.get(
                PokemonGeneracionTabla,
                (integrantes.id_pokemon, datos_actualizados.id_generacion),
            )
            if not generacion_pokemon:
                raise HTTPException(
                    status_code=400,
                    detail=f"Uno de los pokemones no es adecuado para la nueva generacion",
                )

        equipo.nombre_equipo = datos_actualizados.nombre
        equipo.id_generacion_del_equipo = datos_actualizados.id_generacion

        session.add(equipo)
        session.commit()
        session.refresh(equipo)
        return Equipo(
            id=equipo.id_equipo,
            nombre=equipo.nombre_equipo,
            generacion=Generacion(
                id=equipo.id_generacion_del_equipo,
                nombre=session.get(
                    GeneracionTabla, equipo.id_generacion_del_equipo
                ).nombre_generacion,
            ),
            integrantes=[
                Integrante(
                    id=integrante_equipo.id_integrante_dentro_del_grupo,
                    apodo=integrante_equipo.apodo,
                    pokemon=PokemonIntegrante(
                        id=integrante_equipo.id_pokemon,
                        nombre=integrante_equipo.pokemon.nombre,
                        imagen=integrante_equipo.pokemon.imagen,
                        estadisticas=Estadisticas(
                            ataque=integrante_equipo.pokemon.ataque,
                            ataque_especial=integrante_equipo.pokemon.ataque_especial,
                            defensa=integrante_equipo.pokemon.defensa,
                            defensa_especial=integrante_equipo.pokemon.defensa_especial,
                            puntos_de_golpe=integrante_equipo.pokemon.puntos_de_golpe,
                            velocidad=integrante_equipo.pokemon.velocidad,
                        ),
                        generaciones=[
                            Generacion(
                                id=gen.id_generacion, nombre=gen.nombre_generacion
                            )
                            for gen in integrante_equipo.pokemon.generaciones
                        ],
                        tipos=[
                            Tipo(
                                id=tipo.id_tipo,
                                nombre=tipo.nombre_tipo,
                                debilidades=[
                                    Debilidad(
                                        id=debilidad.id_debilidad,
                                        nombre=debilidad.nombre,
                                    )
                                    for debilidad in tipo.debilidades
                                ],
                            )
                            for tipo in integrante_equipo.pokemon.tipos
                        ],
                    ),
                    movimientos=[
                        self.mostrar_por_metodo_de_mov(movi_integrante)
                        for movi_integrante in integrante_equipo.movimientos_del_integrante
                    ],
                )
                for integrante_equipo in equipo.integrantes
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

        return Integrante(
            id=integrante_creado.id_integrante_dentro_del_grupo,
            apodo=integrante_creado.apodo,
            pokemon=PokemonIntegrante(
                nombre=pokemon_encontrado.nombre,
                estadisticas=Estadisticas(
                    ataque=pokemon_encontrado.ataque,
                    ataque_especial=pokemon_encontrado.ataque_especial,
                    defensa=pokemon_encontrado.defensa,
                    defensa_especial=pokemon_encontrado.defensa_especial,
                    puntos_de_golpe=pokemon_encontrado.puntos_de_golpe,
                    velocidad=pokemon_encontrado.velocidad,
                ),
                generaciones=[
                    Generacion(
                        id=generacion.id_generacion, nombre=generacion.nombre_generacion
                    )
                    for generacion in pokemon_encontrado.generaciones
                ],
                id=pokemon_encontrado.id_pokemon,
                imagen=pokemon_encontrado.imagen,
                tipos=[
                    Tipo(
                        debilidades=[
                            Debilidad(
                                id=debilidad.id_debilidad, nombre=debilidad.nombre
                            )
                            for debilidad in tipo.debilidades
                        ],
                        id=tipo.id_tipo,
                        nombre=tipo.nombre_tipo,
                    )
                    for tipo in pokemon_encontrado.tipos
                ],
            ),
            movimientos=[],
        )

    def delete_integrante(
        self, session: Session, id_equipo: int, integrante_id: int
    ) -> Integrante:
        movimientos_mostrar = []
        equipo_encontrado = session.get(EquipoTabla, id_equipo)
        if not equipo_encontrado:
            raise HTTPException(
                status_code=404,
                detail=f"El equipo con id {id_equipo} no existe",
            )
        integrante = None
        for integrante_buscar in equipo_encontrado.integrantes:
            if integrante_id == integrante_buscar.id_integrante_dentro_del_grupo:
                integrante = integrante_buscar

        if integrante is None:
            raise HTTPException(
                status_code=404,
                detail=f"Integrante de id {integrante_id} no encontrado en este equipo",
            )

        pokemon_encontrado = session.get(PokemonTabla, integrante.id_pokemon)
        for movimiento in integrante.movimientos_del_integrante:
            movimiento_mostrar = self.mostrar_por_metodo_de_mov(movimiento)
            movimientos_mostrar.append(movimiento_mostrar)

        session.delete(integrante)
        session.commit()
        pokemon_encontrado = session.get(PokemonTabla, integrante.id_pokemon)
        return Integrante(
            id=integrante.id_integrante_dentro_del_grupo,
            apodo=integrante.apodo,
            pokemon=PokemonIntegrante(
                estadisticas=Estadisticas(
                    ataque=pokemon_encontrado.ataque,
                    ataque_especial=pokemon_encontrado.ataque_especial,
                    defensa=pokemon_encontrado.defensa,
                    defensa_especial=pokemon_encontrado.defensa_especial,
                    puntos_de_golpe=pokemon_encontrado.puntos_de_golpe,
                    velocidad=pokemon_encontrado.velocidad,
                ),
                generaciones=[
                    Generacion(
                        id=generacion.id_generacion, nombre=generacion.nombre_generacion
                    )
                    for generacion in pokemon_encontrado.generaciones
                ],
                id=pokemon_encontrado.id_pokemon,
                imagen=pokemon_encontrado.imagen,
                nombre=pokemon_encontrado.nombre,
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
        return Movimiento(
            id=mov.id_movimiento,
            nombre=mov.nombre,
            generacion=Generacion(
                id=mov.generacion.id_generacion,
                nombre=mov.generacion.nombre_generacion,
            ),
            tipo=TipoMovimiento(
                id=mov.tipo.id_tipo,
                nombre=mov.tipo.nombre_tipo,
            ),
            categoria=mov.clase_de_daño,
            potencia=mov.poder,
            precision=mov.precision,
            puntos_de_poder=mov.PP,
            efecto=mov.efecto,
        )
