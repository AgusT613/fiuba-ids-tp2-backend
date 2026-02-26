import csv
from constantes.constantes import RUTA_GENERATION_NAMES_CSV, ID_ESPANOL


def obtener_nombre_generacion(id: int) -> str:
    """
    Busca el nombre de la generacion dentro del archivo "generation_names.csv"
    """
    nombre = ""

    with open(RUTA_GENERATION_NAMES_CSV, encoding="utf-8") as f:
        archivo_csv = csv.DictReader(f)

        for linea in archivo_csv:
            linea_generation_id = int(linea["generation_id"])
            linea_lang_id = int(linea["local_language_id"])

            if linea_generation_id == id and linea_lang_id == ID_ESPANOL:
                nombre = linea["name"]
                break

    return nombre


def obtener_generacion_por_pokemon(ruta_archivo, id_buscado):
    """
    Devuelve una lista de generaciones (id y nombre) a las que pertenece un Pokémon dado su ID.
    """
    generaciones = []

    with open(ruta_archivo) as archivo:
        csvFile = csv.DictReader(archivo)

        for linea in csvFile:
            pokemon_id = int(linea["pokemon_id"])
            generation_id = int(linea["generation_id"])

            if pokemon_id == id_buscado:
                generaciones.append(
                    {
                        "id": generation_id,
                        "nombre": obtener_nombre_generacion(generation_id),
                    }
                )

    return generaciones
