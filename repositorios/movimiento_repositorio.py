from fastapi import HTTPException
from sqlmodel import Session, select
from modelos.filtros import FiltrosMovimiento
from modelos.mappers import map_movimiento_tabla_to_dto
from modelos.modelos import Generacion, Movimiento, MovimientoDetallado, TipoMovimiento
from modelos.modelos_de_la_db import GeneracionTabla, MovimientoTabla, TipoTabla
from utils.movimientos import filtrar_pokemones


class MovimientoRepositorio:
    """Repositorio para consultas relacionadas con Movimientos."""

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
            movimiento_id, session=session
        )

        return MovimientoDetallado(
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

    def mostrar_por_metodo_de_mov(self, mov: MovimientoTabla) -> Movimiento:
        return map_movimiento_tabla_to_dto(mov)
