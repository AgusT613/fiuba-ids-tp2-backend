import csv
from dependencias.dependencias_de_la_db import Session, get_engine
from modelos.modelos_de_la_db import (
    PokemonTabla,
    GeneracionTabla,
    MovimientoTabla,
    HabilidadesTabla,
    PokemonTipoTabla,
    PokemonHabilidadTabla,
    PokemonMovimientoAprendizajeTabla,
    PokemonGeneracionTabla,
    TipoDebilidadTabla,
    DebilidadTabla,
    EvolucionTabla,
    TipoTabla,
    SeedDb,
)

from constantes.constantes import (
    RUTA_POKEMON_CSV,
    RUTA_GENERATION_CSV,
    RUTA_MOVES_CSV,
    RUTA_ABILITY_NAMES_CSV,
    RUTA_POKEMON_ABILITIES_CSV,
    RUTA_POKEMON_STATS_CSV,
    RUTA_POKEMON_TYPES_CSV,
    RUTA_POKEMON_MOVES_CSV,
    RUTA_STAT_NAMES_CSV,
    RUTA_POKEMON_GENERATIONS_CSV,
    RUTA_TYPE_NAMES_CSV,
    RUTA_POKEMON_EVOLUTIONS_CSV,
    RUTA_TYPE_EFFICACY_CSV,
)

from utils.generaciones import obtener_nombre_generacion
from utils.movimientos import obtener_nombre_movimiento
from utils.index import obtener_categoria, obtener_efecto
from utils.pokemones import obtener_imagen_pokemon
from sqlmodel import select


def seed_ya_hecho(session: Session) -> bool:
    query_db = select(SeedDb).where(SeedDb.id == 1)

    return session.exec(query_db).first().hecho == 1


def actualizar_estado_seed(session: Session, hecho: int = 1, id: int = 1):
    query_db = select(SeedDb).where(SeedDb.id == id)

    seed = session.exec(query_db).first()
    seed.hecho = hecho

    session.add(seed)
    session.commit()
    session.refresh(seed)


def seed():
    with Session(get_engine()) as session:
        if not seed_ya_hecho(session):
            cargar_generaciones(session, RUTA_GENERATION_CSV)
            cargar_pokemones(session, RUTA_POKEMON_CSV)
            cargar_movimientos(session, RUTA_MOVES_CSV)
            cargar_nombres_habilidades(session, RUTA_ABILITY_NAMES_CSV)
            cargar_pokemon_habilidades(session, RUTA_POKEMON_ABILITIES_CSV)
            cargar_nombres_tipos(session, RUTA_TYPE_NAMES_CSV)
            cargar_pokemon_tipos(session, RUTA_POKEMON_TYPES_CSV)
            cargar_pokemon_movimientos(session, RUTA_POKEMON_MOVES_CSV)
            cargar_estadisticas_pokemones(
                session, RUTA_POKEMON_STATS_CSV, RUTA_STAT_NAMES_CSV
            ),
            cargar_pokemon_generaciones(session, RUTA_POKEMON_GENERATIONS_CSV),
            cargar_debilidades(session, RUTA_TYPE_NAMES_CSV)
            cargar_tipo_debilidad(session, RUTA_TYPE_EFFICACY_CSV)
            cargar_evoluciones(session, RUTA_POKEMON_EVOLUTIONS_CSV, RUTA_POKEMON_CSV)

            actualizar_estado_seed(session)
        else:
            print("Los datos ya se cargaron en la db anteriormente")


def cargar_generaciones(session, ruta_archivo):
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        csv_file = csv.DictReader(archivo)
        generaciones = [
            GeneracionTabla(
                id_generacion=int(linea["generation_id"]),
                nombre_generacion=obtener_nombre_generacion(
                    int(linea["generation_id"])
                ),
            )
            for linea in csv_file
        ]
    session.add_all(generaciones)
    session.commit()


def cargar_pokemones(session, ruta_archivo):
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        csv_file = csv.DictReader(archivo)
        pokemones = [
            PokemonTabla(
                id_pokemon=int(linea["id"]),
                nombre=linea["identifier"],
                imagen=obtener_imagen_pokemon(int(linea["id"])),
                altura=float(linea["height"]) / 10,
                peso=float(linea["weight"]) / 10,
            )
            for linea in csv_file
        ]
    session.add_all(pokemones)
    session.commit()


def cargar_movimientos(session, ruta_archivo):
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        csv_file = csv.DictReader(archivo)
        movimientos = [
            MovimientoTabla(
                id_movimiento=int(linea["id"]),
                nombre=obtener_nombre_movimiento(int(linea["id"])),
                id_generacion_del_movimiento=int(linea["generation_id"]),
                id_tipo_del_movimiento=int(linea["type_id"]),
                clase_de_daño=obtener_categoria(int(linea["damage_class_id"])),
                poder=int(linea["power"]) if linea["power"].isdigit() else 0,
                precision=int(linea["accuracy"]) if linea["accuracy"].isdigit() else 0,
                PP=int(linea["pp"]) if linea["pp"].isdigit() else 0,
                efecto=obtener_efecto(int(linea["effect_id"])),
            )
            for linea in csv_file
        ]
    session.add_all(movimientos)
    session.commit()


def cargar_nombres_habilidades(session, ruta_archivo):
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        csv_file = csv.DictReader(archivo)
        habilidades = [
            HabilidadesTabla(
                id_habilidad=int(linea["ability_id"]),
                nombre_habilidad=linea["name"],
            )
            for linea in csv_file
            if linea["local_language_id"] == "7"
        ]
    session.add_all(habilidades)
    session.commit()


def cargar_pokemon_habilidades(session, ruta_archivo):
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        csv_file = csv.DictReader(archivo)
        pokemon_habilidades = [
            PokemonHabilidadTabla(
                id_pokemon=int(linea["pokemon_id"]),
                id_habilidad=int(linea["ability_id"]),
            )
            for linea in csv_file
        ]
    session.add_all(pokemon_habilidades)
    session.commit()


def cargar_nombres_tipos(session, ruta_archivo):
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        csv_file = csv.DictReader(archivo)
        tipos = [
            TipoTabla(
                nombre_tipo=(linea["name"]),
                id_tipo=int(linea["type_id"]),
            )
            for linea in csv_file
            if linea["local_language_id"] == "7"
        ]
    session.add_all(tipos)
    session.commit()


def cargar_pokemon_tipos(session, ruta_archivo):
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        csv_file = csv.DictReader(archivo)
        pokemon_tipos = [
            PokemonTipoTabla(
                id_pokemon=int(linea["pokemon_id"]),
                id_tipo=int(linea["type_id"]),
            )
            for linea in csv_file
        ]
    session.add_all(pokemon_tipos)
    session.commit()


def cargar_pokemon_movimientos(session, ruta_archivo):
    nueva_combi = set()
    pokemon_movimientos = []
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        csv_file = csv.DictReader(archivo)
        for linea in csv_file:
            id_pokemon = int(linea["pokemon_id"])
            id_movimiento = int(linea["move_id"])
            metodo_de_aprendizaje = int(linea["pokemon_move_method_id"])

            combinacion = (id_pokemon, id_movimiento, metodo_de_aprendizaje)

            if combinacion not in nueva_combi:
                nueva_combi.add(combinacion)
                pokemon_movimientos.append(
                    PokemonMovimientoAprendizajeTabla(
                        id_pokemon=int(linea["pokemon_id"]),
                        id_movimiento=int(linea["move_id"]),
                        metodo_de_aprendizaje=int(linea["pokemon_move_method_id"]),
                    )
                )
    session.add_all(pokemon_movimientos)
    session.commit()


def cargar_estadisticas_pokemones(session, ruta_archivo, ruta_nombres):
    nombres_estadisticas = cargar_nombres_estadisticas(ruta_nombres)

    with open(ruta_archivo, "r", encoding="utf-8") as f:
        csv_file = csv.DictReader(f)
        estadisticas = []

        for linea in csv_file:
            id_pokemon = int(linea["pokemon_id"])
            stat_id = int(linea["stat_id"])
            base_stat = int(linea["base_stat"])

            stat_name = nombres_estadisticas.get(stat_id, "")
            if stat_name:
                estadisticas.append(
                    {
                        "id_pokemon": id_pokemon,
                        stat_name: base_stat,
                    }
                )

        # Inserta las estadísticas en la base de datos
        for stat in estadisticas:
            pokemon = session.get(PokemonTabla, stat["id_pokemon"])
            if pokemon:
                for key, value in stat.items():
                    if key != "id_pokemon":
                        setattr(pokemon, key, value)
        session.commit()


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


def cargar_pokemon_generaciones(session, ruta_archivo):
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        csv_file = csv.DictReader(archivo)
        relaciones = [
            PokemonGeneracionTabla(
                id_pokemon=int(linea["pokemon_id"]),
                id_generacion=int(linea["generation_id"]),
            )
            for linea in csv_file
        ]
    session.add_all(relaciones)
    session.commit()


def cargar_debilidades(session, ruta_type_names):
    with open(ruta_type_names, "r", encoding="utf-8") as archivo:
        csv_file = csv.DictReader(archivo)
        debilidades = [
            DebilidadTabla(id_debilidad=int(linea["type_id"]), nombre=linea["name"])
            for linea in csv_file
            if linea["local_language_id"] == "7"
        ]
    session.add_all(debilidades)
    session.commit()


def cargar_tipo_debilidad(session, ruta_type_efficacy):
    with open(ruta_type_efficacy, "r", encoding="utf-8") as archivo:
        csv_file = csv.DictReader(archivo)
        relaciones = [
            TipoDebilidadTabla(
                fk_id_tipo=int(linea["target_type_id"]),
                fk_id_debilidad=int(linea["damage_type_id"]),
            )
            for linea in csv_file
            if int(linea["damage_factor"]) > 100
        ]
    session.add_all(relaciones)
    session.commit()


def cargar_evoluciones(session, ruta_evoluciones, ruta_pokemon):
    nombres = {}
    with open(ruta_pokemon, "r", encoding="utf-8") as archivo:
        csv_file = csv.DictReader(archivo)
        for linea in csv_file:
            nombres[int(linea["id"])] = linea["identifier"]

    with open(ruta_evoluciones, "r", encoding="utf-8") as archivo:
        csv_file = csv.DictReader(archivo)
        evoluciones = [
            EvolucionTabla(
                fk_id_pokemon=int(linea["id"]),
                id_evolucion=int(linea["evolution_id"]),
                nombre_evolucion=nombres.get(int(linea["evolution_id"]), ""),
                imagen=obtener_imagen_pokemon(int(linea["evolution_id"])),
            )
            for linea in csv_file
        ]
    session.add_all(evoluciones)
    session.commit()
