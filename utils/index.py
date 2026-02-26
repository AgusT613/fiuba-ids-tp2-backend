import csv
from constantes.constantes import (
    RUTA_MOVE_DAMAGE_CLASS_PROSE_CSV,
    RUTA_MOVE_EFFECT_PROSE_CSV,
    RUTA_POKEMON_TYPES_CSV,
    RUTA_TYPE_EFFICACY_CSV,
    RUTA_TYPE_NAMES_CSV,
    ID_ESPANOL,
)
from modelos.modelos import Tipo


def obtener_categoria(id: int) -> str:
    """
    Busca el nombre de la categoria en el archivo "move_damage_class_prose.csv"
    """
    nombre = ""

    with open(RUTA_MOVE_DAMAGE_CLASS_PROSE_CSV, encoding="utf-8") as f:
        archivo_csv = csv.DictReader(f)

        for linea in archivo_csv:
            linea_damage_id = int(linea["move_damage_class_id"])
            linea_lang_id = int(linea["local_language_id"])

            if linea_damage_id == id and linea_lang_id == ID_ESPANOL:
                nombre = linea["name"]
                break

    return nombre


def obtener_efecto(id: int) -> str:
    """
    Busca la descripcion del efecto en el archivo "move_effect_prose.csv"
    """
    efecto = ""

    with open(RUTA_MOVE_EFFECT_PROSE_CSV, encoding="utf-8") as f:
        archivo_csv = csv.DictReader(f)

        for linea in archivo_csv:
            linea_effect_id = int(linea["move_effect_id"])

            if linea_effect_id == id:
                efecto = linea["short_effect"]
                break

    return efecto


def obtener_nombre_tipo(id: int) -> str:
    """
    Busca el nombre del tipo de movimiento en el archivo "type_names.csv"
    """
    nombre = ""

    with open(RUTA_TYPE_NAMES_CSV, encoding="utf-8") as f:
        archivo_csv = csv.DictReader(f)

        for linea in archivo_csv:
            linea_type_id = int(linea["type_id"])
            linea_lang_id = int(linea["local_language_id"])

            if linea_type_id == id and linea_lang_id == ID_ESPANOL:
                nombre = linea["name"]
                break

    return nombre


def cargar_nombres_tipos(ruta_archivo):
    """
    Carga los nombres de los tipos en español (local_language_id == 7) desde un archivo CSV.
    Devuelve un diccionario donde la clave es el id del tipo y el valor es su nombre.
    """
    nombres_tipos = {}

    with open(ruta_archivo, encoding="utf-8") as archivo:
        csvFile = csv.DictReader(archivo)

        for linea in csvFile:
            if linea["local_language_id"] == "7":
                id = int(linea["type_id"])
                nombres_tipos[id] = linea["name"]

    return nombres_tipos


def cargar_tipos(ruta_archivo):
    """
    Asocia los tipos con cada Pokémon usando su id. Usa los nombres cargados desde type_names.csv.
    Devuelve un diccionario donde la clave es el id del Pokémon y el valor es una lista de objetos Tipo.
    """
    tipos_por_pokemon = {}
    nombres_tipos = cargar_nombres_tipos(RUTA_TYPE_NAMES_CSV)

    with open(ruta_archivo, encoding="utf-8") as archivo:
        csvFile = csv.DictReader(archivo)

        for linea in csvFile:
            id_pokemon = int(linea["pokemon_id"])
            tipo_id = int(linea["type_id"])
            nombre_tipo = nombres_tipos.get(tipo_id)
            tipo = Tipo(id=tipo_id, nombre=nombre_tipo)

            if id_pokemon not in tipos_por_pokemon:
                tipos_por_pokemon[id_pokemon] = []

            tipos_por_pokemon[id_pokemon].append(tipo)

    return tipos_por_pokemon


def obtener_ids_tipos_por_id_pokemon(id_pokemon: int) -> list[int]:
    """
    Busca todos los type_id del Pokémon dado su id, usando el archivo pokemon_types.csv.
    """
    tipos = []
    with open(RUTA_POKEMON_TYPES_CSV, encoding="utf-8") as archivo:
        csvFile = csv.DictReader(archivo)
        for linea in csvFile:
            if int(linea["pokemon_id"]) == id_pokemon:
                tipos.append(int(linea["type_id"]))  # type_id
    return tipos


def obtener_debilidades_por_tipo(id_tipo: int) -> list[dict]:
    """
    Busca los tipos que le hacen más daño (damage_factor > 100) al tipo dado.
    """
    debilidades = []
    with open(RUTA_TYPE_EFFICACY_CSV, encoding="utf-8") as archivo:
        csvFile = csv.DictReader(archivo)
        for linea in csvFile:
            tipo_atacante = int(
                linea["damage_type_id"]
            )  # damage_type_id (el que ataca)
            tipo_defensor = int(
                linea["target_type_id"]
            )  # target_type_id (el que recibe el daño)
            factor = int(linea["damage_factor"])  # damage_factor

            # Solo buscamos las relaciones donde damage_factor > 100
            if tipo_defensor == id_tipo and factor > 100:
                nombre_tipo = obtener_nombre_tipo(
                    tipo_atacante
                )  # Nombre del tipo atacante
                debilidades.append({"id": tipo_atacante, "nombre": nombre_tipo})
    return debilidades


def obtener_tipo_por_pokemon(ruta_archivo, id_buscado):
    """
    Devuelve una lista de tipos (cada uno con id y nombre) para un Pokémon dado su ID.
    """
    tipos = []
    nombres_tipos = cargar_nombres_tipos(RUTA_TYPE_NAMES_CSV)

    with open(ruta_archivo, encoding="utf-8") as archivo:
        csvFile = csv.DictReader(archivo)
        for linea in csvFile:
            if int(linea["pokemon_id"]) == id_buscado:
                tipo_id = int(linea["type_id"])
                nombre_tipo = nombres_tipos.get(tipo_id)
                debilidades = obtener_debilidades_por_tipo(tipo_id)
                tipos.append(
                    {"id": tipo_id, "nombre": nombre_tipo, "debilidades": debilidades}
                )

    return tipos
