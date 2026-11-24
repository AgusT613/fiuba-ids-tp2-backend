import csv
from constantes.constantes import (
    RUTA_MOVE_DAMAGE_CLASS_PROSE_CSV,
    RUTA_MOVE_EFFECT_PROSE_CSV,
    ID_ESPANOL,
)


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
