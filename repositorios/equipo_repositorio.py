from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select
from modelos.mappers import map_integrante_tabla_to_dto
from modelos.modelos import (
    Equipo,
    EquipoListado,
    EquipoUpsert,
    Generacion,
    Integrante,
    IntegranteUpsert,
)
from modelos.modelos_de_la_db import (
    EquipoTabla,
    GeneracionTabla,
    IntegranteTabla,
    PokemonGeneracionTabla,
    PokemonTabla,
)


class EquipoRepositorio:
    """Repositorio para gestión de Equipos e Integrantes."""

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
        return Equipo(
            id=equipo.id_equipo,
            nombre=equipo.nombre_equipo,
            generacion=Generacion(
                id=generacion.id_generacion, nombre=generacion.nombre_generacion
            ),
            integrantes=self.get_integrantes_equipo(session, id),
        )

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
        self, session: Session, equipo_a_crear: EquipoUpsert
    ) -> Equipo:
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
        self, session: Session, id_equipo: int, datos_actualizados: EquipoUpsert
    ) -> Equipo:
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
