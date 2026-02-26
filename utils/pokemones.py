import csv
from modelos.modelos import Evoluciones, Pokemon
from constantes.constantes import RUTA_POKEMON_CSV


def obtener_nombre_pokemon(ruta_archivo, id_buscado):
    """
    Busca el nombre (identifier) de un Pokémon en el archivo CSV dado su ID.
    Devuelve el nombre del Pokémon si se encuentra, o vacío si no.
    """
    with open(ruta_archivo) as archivo:
        csvFile = csv.DictReader(archivo)

        for linea in csvFile:
            if int(linea["id"]) == id_buscado:
                return str(linea["identifier"])

    return ""


def obtener_imagen_pokemon(pokemon_id: int) -> str:
    return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"


def cargar_evoluciones(ruta_archivo):
    """
    Carga las evoluciones de los Pokémon desde un archivo CSV.
    Devuelve un diccionario donde la clave es el ID de un Pokémon
    y el valor es una lista de objetos Evoluciones que representan
    a los Pokémon a los que puede evolucionar.
    """
    evoluciones_por_pokemon = {}

    with open(ruta_archivo) as archivo:
        csvFile = csv.DictReader(archivo)

        for linea in csvFile:
            id_pokemon = int(linea["id"])
            id_evolution = int(linea["evolution_id"])
            evolucion = Evoluciones(
                id=id_evolution,
                imagen=obtener_imagen_pokemon(int(linea["evolution_id"])),
                nombre=obtener_nombre_pokemon(RUTA_POKEMON_CSV, id_evolution),
            )

            if id_pokemon not in evoluciones_por_pokemon:
                evoluciones_por_pokemon[id_pokemon] = []

            evoluciones_por_pokemon[id_pokemon].append(evolucion)

    return evoluciones_por_pokemon


def es_del_mismo_tipo(tipo_a_chequear, pokemon: Pokemon) -> bool:
    for t in pokemon.tipos:
        if t.id_tipo == tipo_a_chequear:
            return True
    return False
