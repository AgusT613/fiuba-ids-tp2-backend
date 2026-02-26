import csv
from constantes.constantes import RUTA_MOVE_NAMES_CSV, ID_ESPANOL, METODO_MOVIMIENTO
from modelos.modelos import PokemonMovimiento
from dependencias.dependencias_de_la_db import get_engine
from sqlmodel import Session, select
from modelos.modelos_de_la_db import PokemonMovimientoAprendizajeTabla, PokemonTabla


def obtener_nombre_movimiento(id_movimiento: int):
    """
    Busca el nombre del movimiento en español en el archivo "move_names.csv"
    """
    nombre = ""

    with open(RUTA_MOVE_NAMES_CSV, encoding="utf-8") as f:
        archivo_csv = csv.DictReader(f)

        for linea in archivo_csv:
            linea_move_id = int(linea["move_id"])
            linea_lang_id = int(linea["local_language_id"])

            if linea_move_id == id_movimiento and linea_lang_id == ID_ESPANOL:
                nombre = linea["name"]
                break

    return nombre


def agregar_resultado_listado(lista_filtrados: list, results):
    for pokemon, _ in results:
        lista_filtrados.append(
            PokemonMovimiento(
                id=pokemon.id_pokemon,
                nombre=pokemon.nombre,
                imagen=pokemon.imagen,
                altura=pokemon.altura,
                peso=pokemon.peso,
            )
        )


def get_query_filtrar(metodo_movimiento_id: int, movimiento_id: int):
    query = (
        select(PokemonTabla, PokemonMovimientoAprendizajeTabla)
        .join(
            PokemonMovimientoAprendizajeTabla,
            PokemonTabla.id_pokemon == PokemonMovimientoAprendizajeTabla.id_pokemon,
        )
        .where(
            PokemonMovimientoAprendizajeTabla.metodo_de_aprendizaje
            == metodo_movimiento_id,
            PokemonMovimientoAprendizajeTabla.id_movimiento == movimiento_id,
        )
    )

    return query


def filtrar_pokemones(
    movimiento_id: int,
) -> tuple[list[PokemonMovimiento], list[PokemonMovimiento], list[PokemonMovimiento]]:
    """
    Devuelve tres listas con todos los pokemones que pueden aprender "movimiento"

    - metodo_movimiento = "huevo" | "nivel" | "maquina"
    """
    pokemon_por_huevo = []
    pokemon_por_nivel = []
    pokemon_por_maquina = []

    with Session(get_engine()) as session:
        query_huevo = get_query_filtrar(METODO_MOVIMIENTO["huevo"], movimiento_id)
        query_nivel = get_query_filtrar(METODO_MOVIMIENTO["nivel"], movimiento_id)
        query_maquina = get_query_filtrar(METODO_MOVIMIENTO["maquina"], movimiento_id)

        results_huevo = session.exec(query_huevo).all()
        results_nivel = session.exec(query_nivel).all()
        results_maquina = session.exec(query_maquina).all()

        agregar_resultado_listado(pokemon_por_huevo, results_huevo)
        agregar_resultado_listado(pokemon_por_nivel, results_nivel)
        agregar_resultado_listado(pokemon_por_maquina, results_maquina)

    return pokemon_por_huevo, pokemon_por_nivel, pokemon_por_maquina
