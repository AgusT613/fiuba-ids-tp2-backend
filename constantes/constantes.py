import os

METODO_MOVIMIENTO = {"huevo": 2, "nivel": 1, "maquina": 4}

ID_ESPANOL = 7
RUTA_ABSOLUTA_PROYECTO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RUTA_DATA_CSV = os.path.join(RUTA_ABSOLUTA_PROYECTO, "data")
SQLITE_FILE_PATH = os.path.join(RUTA_ABSOLUTA_PROYECTO, "database.db")

RUTA_MOVES_CSV = os.path.join(RUTA_DATA_CSV, "moves.csv")
RUTA_MOVE_NAMES_CSV = os.path.join(RUTA_DATA_CSV, "move_names.csv")
RUTA_GENERATION_CSV = os.path.join(RUTA_DATA_CSV, "generation.csv")
RUTA_GENERATION_NAMES_CSV = os.path.join(RUTA_DATA_CSV, "generation_names.csv")
RUTA_POKEMON_GENERATIONS_CSV = os.path.join(RUTA_DATA_CSV, "pokemon_generations.csv")
RUTA_TYPE_NAMES_CSV = os.path.join(RUTA_DATA_CSV, "type_names.csv")
RUTA_MOVE_DAMAGE_CLASS_PROSE_CSV = os.path.join(
    RUTA_DATA_CSV, "move_damage_class_prose.csv"
)
RUTA_MOVE_EFFECT_PROSE_CSV = os.path.join(RUTA_DATA_CSV, "move_effect_prose.csv")
RUTA_POKEMON_MOVES_CSV = os.path.join(RUTA_DATA_CSV, "pokemon_moves.csv")
RUTA_POKEMON_CSV = os.path.join(RUTA_DATA_CSV, "pokemon.csv")
RUTA_POKEMON_TYPES_CSV = os.path.join(RUTA_DATA_CSV, "pokemon_types.csv")

RUTA_POKEMON_ABILITIES_CSV = os.path.join(RUTA_DATA_CSV, "pokemon_abilities.csv")
RUTA_ABILITY_NAMES_CSV = os.path.join(RUTA_DATA_CSV, "ability_names.csv")
RUTA_POKEMON_STATS_CSV = os.path.join(RUTA_DATA_CSV, "pokemon_stats.csv")
RUTA_STAT_NAMES_CSV = os.path.join(RUTA_DATA_CSV, "stat_names.csv")
RUTA_STATS_CSV = os.path.join(RUTA_DATA_CSV, "stats.csv")

RUTA_POKEMON_EVOLUTIONS_CSV = os.path.join(RUTA_DATA_CSV, "pokemon_evolutions.csv")
RUTA_TYPE_EFFICACY_CSV = os.path.join(RUTA_DATA_CSV, "type_efficacy.csv")
