import csv
from constantes.constantes import RUTA_MOVE_NAMES_CSV, ID_ESPANOL, METODO_MOVIMIENTO
from modelos.modelos import PokemonMovimiento


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


def filtrar_pokemones(
    movimiento_id: int, listado_pokemones, listado_moves_csv
) -> tuple[list[PokemonMovimiento], list[PokemonMovimiento], list[PokemonMovimiento]]:
    """
    Devuelve tres listas con todos los pokemones que pueden aprender "movimiento"

    - metodo_movimiento = "huevo" | "nivel" | "maquina"
    """
    pokemon_por_huevo = []
    pokemon_por_nivel = []
    pokemon_por_maquina = []

    for m in listado_moves_csv:
        if m["linea_move_id"] != movimiento_id:
            continue

        pokemon_id = m["linea_pokemon_id"]
        metodo = m["linea_move_method_id"]

        if m["linea_move_id"] == movimiento_id:
            for p in listado_pokemones:
                pokemon = PokemonMovimiento(
                    id=p.id,
                    nombre=p.nombre,
                    imagen=p.imagen,
                    altura=p.altura,
                    peso=p.peso,
                )

                if pokemon.id == pokemon_id and metodo == METODO_MOVIMIENTO["huevo"]:
                    pokemon_por_huevo.append(pokemon)

                elif pokemon.id == pokemon_id and metodo == METODO_MOVIMIENTO["nivel"]:
                    pokemon_por_nivel.append(pokemon)

                elif (
                    pokemon.id == pokemon_id and metodo == METODO_MOVIMIENTO["maquina"]
                ):
                    pokemon_por_maquina.append(pokemon)

    return pokemon_por_huevo, pokemon_por_nivel, pokemon_por_maquina
