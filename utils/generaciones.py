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
