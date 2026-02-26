import csv

from dependencias.dependencias import get_database
from modelos.modelos import Pokemon, Movimiento, Generacion, Estadisticas, Habilidades
from utils.index import (
    obtener_tipo_por_pokemon,
    obtener_nombre_tipo,
    obtener_categoria,
    obtener_efecto,
)
from utils.generaciones import obtener_nombre_generacion, obtener_generacion_por_pokemon
from utils.movimientos import obtener_nombre_movimiento
from utils.pokemones import obtener_imagen_pokemon, cargar_evoluciones
from constantes.constantes import (
    RUTA_POKEMON_CSV,
    RUTA_POKEMON_EVOLUTIONS_CSV,
    RUTA_POKEMON_TYPES_CSV,
    RUTA_MOVES_CSV,
    RUTA_GENERATION_CSV,
    RUTA_POKEMON_GENERATIONS_CSV,
    RUTA_ABILITY_NAMES_CSV,
    RUTA_POKEMON_ABILITIES_CSV,
    RUTA_POKEMON_CSV,
    RUTA_POKEMON_STATS_CSV,
    RUTA_STAT_NAMES_CSV,
    RUTA_STATS_CSV,
    RUTA_POKEMON_MOVES_CSV,
)


def seed():
    cargar_pokemones(RUTA_POKEMON_CSV)
    cargar_generaciones(RUTA_GENERATION_CSV)
    cargar_pokemon_moves_csv(RUTA_POKEMON_MOVES_CSV)
    cargar_movimientos(RUTA_MOVES_CSV)
    cargar_nombres_habilidades(RUTA_ABILITY_NAMES_CSV)
    cargar_habilidades_pokemon(RUTA_POKEMON_ABILITIES_CSV)
    cargar_nombres_estadisticas(RUTA_STAT_NAMES_CSV)
    identificar_estadisticas(RUTA_STATS_CSV)
    cargar_estadisticas_pokemones(
        RUTA_POKEMON_STATS_CSV, RUTA_STAT_NAMES_CSV, RUTA_STATS_CSV
    )
    evoluciones_por_pokemon = cargar_evoluciones(RUTA_POKEMON_EVOLUTIONS_CSV)
    get_database().cargar_evoluciones(evoluciones_por_pokemon)


def cargar_generaciones(ruta_archivo):
    generaciones = []
    ids_agregados = []

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        csv_file = csv.DictReader(archivo)

        for linea in csv_file:
            generacion_id = int(linea["generation_id"])
            nombre_generacion = obtener_nombre_generacion(generacion_id)

            if generacion_id not in ids_agregados:
                generaciones.append(
                    Generacion(id=generacion_id, nombre=nombre_generacion)
                )
                ids_agregados.append(generacion_id)

    generaciones_ordenadas = sorted(generaciones, key=lambda g: g.id)

    get_database().cargar_generaciones(generaciones_ordenadas)


def cargar_pokemones(ruta_archivo):
    """
    Carga todos los Pokémon desde un archivo CSV y devuelve una lista de objetos Pokemon.
    Cada Pokémon incluye su id, generación, nombre, altura, peso e imagen generada por su id.
    """
    pokemones = []

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        csv_file = csv.DictReader(archivo)

        for linea in csv_file:
            pokemon_id = int(linea["id"])
            generaciones_lista = obtener_generacion_por_pokemon(
                RUTA_POKEMON_GENERATIONS_CSV, pokemon_id
            )
            tipos_lista = obtener_tipo_por_pokemon(RUTA_POKEMON_TYPES_CSV, pokemon_id)

            pokemones.append(
                Pokemon(
                    id=pokemon_id,
                    nombre=str(linea["identifier"]),
                    imagen=obtener_imagen_pokemon(pokemon_id),
                    generaciones=generaciones_lista,
                    tipos=tipos_lista,
                    altura=float(linea["height"]) / 10,
                    peso=float(linea["weight"]) / 10,
                )
            )

    get_database().cargar_pokemones(pokemones)


def cargar_movimientos(ruta_archivo: str):
    lista_movimientos: list[Movimiento] = []

    with open(ruta_archivo, "r", encoding="utf-8") as f:
        archivo_csv = csv.DictReader(f)

        for linea in archivo_csv:
            movimiento_id = int(linea["id"])
            nombre = obtener_nombre_movimiento(movimiento_id)
            generacion = {
                "id": int(linea["generation_id"]),
                "nombre": obtener_nombre_generacion(int(linea["generation_id"])),
            }
            tipo = {
                "id": int(linea["type_id"]),
                "nombre": obtener_nombre_tipo(int(linea["type_id"])),
            }
            categoria = obtener_categoria(int(linea["damage_class_id"]))
            try:
                potencia = int(linea["power"])
                precision = int(linea["accuracy"])
                puntos_de_poder = int(linea["pp"])
            except ValueError:
                potencia = 0
                precision = 0
                puntos_de_poder = 0
            efecto = obtener_efecto(int(linea["effect_id"]))

            movimiento = Movimiento(
                id=movimiento_id,
                nombre=nombre,
                generacion=generacion,
                tipo=tipo,
                categoria=categoria,
                potencia=potencia,
                precision=precision,
                puntos_de_poder=puntos_de_poder,
                efecto=efecto,
            )
            lista_movimientos.append(movimiento)

    get_database().cargar_movimientos(lista_movimientos)


def cargar_nombres_habilidades(ruta_archivo):
    nombres_habilidades = {}
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        csv_file = csv.DictReader(f)
        for linea in csv_file:
            if linea["local_language_id"] == "7":
                habilidad_id = int(linea["ability_id"])
                nombres_habilidades[habilidad_id] = linea["name"]
    return nombres_habilidades


def cargar_habilidades_pokemon(ruta_archivo):
    habilidades_por_pokemon = {}
    nombres_habilidades = cargar_nombres_habilidades(RUTA_ABILITY_NAMES_CSV)

    with open(ruta_archivo, "r", encoding="utf-8") as f:
        csv_file = csv.DictReader(f)
        for linea in csv_file:
            id_pokemon = int(linea["pokemon_id"])
            habilidad_id = int(linea["ability_id"])
            nombre_habilidad = nombres_habilidades.get(habilidad_id)

            habilidad = Habilidades(id=habilidad_id, nombre=nombre_habilidad)

            if id_pokemon not in habilidades_por_pokemon:
                habilidades_por_pokemon[id_pokemon] = []
            habilidades_por_pokemon[id_pokemon].append(habilidad)

    get_database().cargar_habilidades(habilidades_por_pokemon)


def cargar_nombres_estadisticas(ruta_archivo):
    nombres_estadisticas = {}
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        csv_file = csv.DictReader(f)
        for linea in csv_file:
            if linea["local_language_id"] == "7":
                stat_id = int(linea["stat_id"])
                nombre = linea["name"].strip().lower().replace(" ", "_")

                if nombre == "ps":
                    nombre = "puntos_de_golpe"

                nombres_estadisticas[stat_id] = nombre
    return nombres_estadisticas


def identificar_estadisticas(ruta_archivo):
    identificadores = {}
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        csv_file = csv.DictReader(f)
        for linea in csv_file:
            stat_id = int(linea["id"])
            identificador = linea["identifier"].strip().lower()
            identificadores[stat_id] = identificador
    return identificadores


def cargar_estadisticas_pokemones(ruta_archivo, ruta_nombres, ruta_stat):

    nombres_estadisticas = cargar_nombres_estadisticas(ruta_nombres)
    identificar_estadisticas(ruta_stat)

    estadisticas_de_pokemon = {}

    with open(ruta_archivo, "r", encoding="utf-8") as f:
        csv_file = csv.DictReader(f)
        for linea in csv_file:
            id_pokemon = int(linea["pokemon_id"])
            stat_id = int(linea["stat_id"])
            base_stat = int(linea["base_stat"])

            stat_name = nombres_estadisticas.get(stat_id, "")

            if stat_name and base_stat is not None:
                if id_pokemon not in estadisticas_de_pokemon:
                    estadisticas_de_pokemon[id_pokemon] = {
                        "ataque": 0,
                        "defensa": 0,
                        "ataque_especial": 0,
                        "defensa_especial": 0,
                        "puntos_de_golpe": 0,
                        "velocidad": 0,
                    }

                if stat_name in estadisticas_de_pokemon[id_pokemon]:
                    estadisticas_de_pokemon[id_pokemon][stat_name] += base_stat

    for id_pokemon, stats in estadisticas_de_pokemon.items():
        estadisticas_de_pokemon[id_pokemon] = Estadisticas(
            ataque=stats["ataque"],
            defensa=stats["defensa"],
            ataque_especial=stats["ataque_especial"],
            defensa_especial=stats["defensa_especial"],
            puntos_de_golpe=stats["puntos_de_golpe"],
            velocidad=stats["velocidad"],
        )

    get_database().cargar_estadisticas(estadisticas_de_pokemon)


def cargar_pokemon_moves_csv(ruta_archivo):
    lista_movimientos_csv = []

    with open(ruta_archivo) as f:
        archivo_csv = csv.DictReader(f)

        for linea in archivo_csv:
            linea_move_method_id = int(linea["pokemon_move_method_id"])
            linea_move_id = int(linea["move_id"])
            linea_group_id = int(linea["version_group_id"])
            linea_pokemon_id = int(linea["pokemon_id"])

            if linea_group_id == 1 and linea_move_method_id in [1, 2, 4]:
                lista_movimientos_csv.append(
                    {
                        "linea_move_method_id": linea_move_method_id,
                        "linea_move_id": linea_move_id,
                        "linea_pokemon_id": linea_pokemon_id,
                    }
                )

    get_database().cargar_pokemon_moves_csv(lista_movimientos_csv)
