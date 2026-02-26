from fastapi import APIRouter, HTTPException
from dependencias.dependencias import DatabaseDep
from modelos.modelos import Pokemon, PokemonPorId
from utils.pokemones import es_del_mismo_tipo

router = APIRouter()


@router.get("/")
def obtener_pokemones(
    db: DatabaseDep, tipo: int | None = None, nombre_parcial: str | None = None
) -> list[Pokemon]:
    pokemones = db.obtener_pokemones()
    pokemones_filtrados = []

    if tipo is not None and nombre_parcial is None:
        for p in pokemones:
            if es_del_mismo_tipo(tipo, p):
                pokemones_filtrados.append(p)
        pokemones = pokemones_filtrados

    if nombre_parcial is not None and tipo is None:
        for p in pokemones:
            if nombre_parcial.lower() not in p.nombre.lower():
                continue
            pokemones_filtrados.append(p)
        pokemones = pokemones_filtrados

    if nombre_parcial is not None and tipo is not None:
        for p in pokemones:
            if nombre_parcial.lower() in p.nombre.lower() and es_del_mismo_tipo(
                tipo, p
            ):
                pokemones_filtrados.append(p)
        pokemones = pokemones_filtrados
    return pokemones


@router.get("/{id}", response_model=PokemonPorId)
def get_pokemon(id: int, db: DatabaseDep):
    if id < 0:
        raise HTTPException(status_code=422, detail="El ID no puede ser negativo")

    pokemon = db.get(id)
    if pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon no encontrado")

    habilidades = db.get_habilidades(id)
    estadisticas = db.get_estadisticas(id)
    evoluciones = db.get_evoluciones(id)
    movimientos_huevo, movimientos_maquina, movimientos_nivel = (
        db.obtener_movimientos_pokemon(id)
    )

    return PokemonPorId(
        id=pokemon.id,
        nombre=pokemon.nombre,
        imagen=pokemon.imagen,
        altura=pokemon.altura,
        peso=pokemon.peso,
        generaciones=pokemon.generaciones,
        tipos=pokemon.tipos,
        habilidades=habilidades,
        estadisticas=estadisticas,
        evoluciones=evoluciones,
        movimientos_huevo=movimientos_huevo,
        movimientos_maquina=movimientos_maquina,
        movimientos_nivel=movimientos_nivel,
    )
