from modelos.modelos import (
    Debilidad,
    Estadisticas,
    Generacion,
    Integrante,
    Movimiento,
    PokemonIntegrante,
    Tipo,
    TipoMovimiento,
)
from modelos.modelos_de_la_db import IntegranteTabla, MovimientoTabla, PokemonTabla


def map_movimiento_tabla_to_dto(mov: MovimientoTabla) -> Movimiento:
    """Mapea una entidad MovimientoTabla a su DTO Movimiento."""
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


def map_integrante_tabla_to_dto(
    integrante: IntegranteTabla,
    pokemon: PokemonTabla | None = None,
    movimientos: list[Movimiento] | None = None,
) -> Integrante:
    """Mapea una entidad IntegranteTabla y su Pokemon asociado al DTO Integrante."""
    poke = pokemon or integrante.pokemon
    if movimientos is not None:
        movs = movimientos
    else:
        movs = [
            map_movimiento_tabla_to_dto(mov)
            for mov in (integrante.movimientos_del_integrante or [])
        ]
    return Integrante(
        id=integrante.id_integrante_dentro_del_grupo,
        apodo=integrante.apodo,
        pokemon=PokemonIntegrante(
            id=poke.id_pokemon,
            nombre=poke.nombre,
            imagen=poke.imagen,
            estadisticas=Estadisticas(
                ataque=poke.ataque,
                ataque_especial=poke.ataque_especial,
                defensa=poke.defensa,
                defensa_especial=poke.defensa_especial,
                puntos_de_golpe=poke.puntos_de_golpe,
                velocidad=poke.velocidad,
            ),
            generaciones=[
                Generacion(
                    id=gen.id_generacion,
                    nombre=gen.nombre_generacion,
                )
                for gen in poke.generaciones
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
                        for debilidad in (tipo.debilidades or [])
                    ],
                )
                for tipo in poke.tipos
            ],
        ),
        movimientos=movs,
    )
