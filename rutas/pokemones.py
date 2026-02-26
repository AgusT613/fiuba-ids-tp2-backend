from fastapi import APIRouter, HTTPException, Depends
from dependencias.dependencias import DatabaseDep
from dependencias.dependencias_de_la_db import SessionDep
from modelos.modelos import PokemonPorId, PokemonLista, Generacion
from modelos.modelos_de_la_db import PokemonTabla
from modelos.filtros import FiltrosPokemon

router = APIRouter()


@router.get("/")
def get_pokemones(
    session: SessionDep, db: DatabaseDep, filtros: FiltrosPokemon = Depends()
) -> list[PokemonLista]:
    pokemones = db.get_pokemones(session, filtros)

    return pokemones


@router.get("/{id}", response_model=PokemonPorId)
def get_pokemon(session: SessionDep, id: int, db: DatabaseDep):
    if id < 0:
        raise HTTPException(status_code=422, detail="El ID no puede ser negativo")

    pokemon = session.get(PokemonTabla, id)

    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon no encontrado")

    habilidades = db.get_habilidades(session, id)
    generaciones = [
        Generacion(id=generacion.id_generacion, nombre=generacion.nombre_generacion)
        for generacion in pokemon.generaciones
    ]
    tipos = db.get_tipos_pokemon(session, id)
    evoluciones = db.get_evoluciones(session, id)
    movimientos_huevo, movimientos_maquina, movimientos_nivel = (
        db.get_movimientos_pokemon(session, id)
    )

    return PokemonPorId(
        id=pokemon.id_pokemon,
        nombre=pokemon.nombre,
        imagen=pokemon.imagen,
        altura=pokemon.altura,
        peso=pokemon.peso,
        generaciones=generaciones,
        tipos=tipos,
        habilidades=habilidades,
        estadisticas={
            "ataque": pokemon.ataque,
            "defensa": pokemon.defensa,
            "ataque_especial": pokemon.ataque_especial,
            "defensa_especial": pokemon.defensa_especial,
            "puntos_de_golpe": pokemon.puntos_de_golpe,
            "velocidad": pokemon.velocidad,
        },
        evoluciones=evoluciones,
        movimientos_huevo=movimientos_huevo,
        movimientos_maquina=movimientos_maquina,
        movimientos_nivel=movimientos_nivel,
    )
