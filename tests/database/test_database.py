import pytest
from database.database import Database
import pytest
from modelos.modelos import (
    EquipooUpsert,
    Integrante,
    IntegranteUpsert,
    Pokemon,
    Habilidades,
    Estadisticas,
    Generacion,
    Movimiento,
    Tipo,
    Evoluciones,
)
from fastapi import HTTPException
from constantes.constantes import EQUIPO1, EQUIPO2, GENERACIONES, POKEMON1, POKEMON2


@pytest.fixture
def db():
    return Database()


def test_cargar_y_obtener_pokemones(db: Database):
    p1 = POKEMON1
    p2 = POKEMON2

    db.cargar_pokemones([p1, p2])

    assert db.get(30) == p1
    assert db.get(2) == p2
    assert db.get(999) is None


def test_cargar_y_obtener_habilidades(db: Database):
    h1 = Habilidades(id=1, nombre="Una Habilidad God")
    h2 = Habilidades(id=2, nombre="una habilidad meh")

    db.cargar_habilidades({1: [h1], 2: [h2]})

    habilidades_1 = db.get_habilidades(1)
    habilidades_2 = db.get_habilidades(2)
    habilidades_desconocido = db.get_habilidades(999)

    assert habilidades_1 == [h1]
    assert habilidades_2 == [h2]
    assert habilidades_desconocido == []


def test_cargar_y_obtener_estadisticas(db: Database):
    e1 = Estadisticas(
        ataque=100,
        defensa=100,
        ataque_especial=100,
        defensa_especial=100,
        puntos_de_golpe=150,
        velocidad=50,
    )
    e2 = Estadisticas(
        ataque=20,
        defensa=20,
        ataque_especial=200,
        defensa_especial=99,
        puntos_de_golpe=200,
        velocidad=80,
    )
    db.cargar_estadisticas({1: [e1], 2: [e2]})

    estadisticas_1 = db.get_estadisticas(1)
    estadisticas_2 = db.get_estadisticas(2)
    estadisticas_desconocido = db.get_estadisticas(999)

    assert estadisticas_1 == [e1]
    assert estadisticas_2 == [e2]
    assert estadisticas_desconocido == None


def test_cargar_y_obtener_evoluciones(db: Database):
    evo1 = Evoluciones(id=500, nombre="Pikagod", imagen="una imagen")
    evo2 = Evoluciones(id=31, nombre="Nidoqueen", imagen="una imagen")
    db.cargar_evoluciones({1: [evo1], 2: [evo2]})

    evoluciones_1 = db.get_evoluciones(1)
    evoluciones_2 = db.get_evoluciones(2)
    evoluciones_desconocido = db.get_evoluciones(999)

    assert evoluciones_1 == [evo1]
    assert evoluciones_2 == [evo2]
    assert evoluciones_desconocido == []


def test_cargar_y_obtener_movimientos(db: Database):
    m1 = Movimiento(
        id=1,
        nombre="Destructor",
        generacion={"id": 1, "nombre": "Generación I"},
        tipo={"id": 1, "nombre": "Normal"},
        categoria="físico",
        potencia=40,
        precision=100,
        puntos_de_poder=35,
        efecto="Inflicts regular damage with no additional effect.",
    )
    m2 = Movimiento(
        id=2,
        nombre="Golpe Kárate",
        generacion={"id": 1, "nombre": "Generación I"},
        tipo={"id": 2, "nombre": "Lucha"},
        categoria="físico",
        potencia=50,
        precision=100,
        puntos_de_poder=25,
        efecto="Has an increased chance for a critical hit.",
    )
    db.cargar_movimientos([m1, m2])

    movimientos = db.obtener_movimientos()
    movi = db.obtener_movimiento_simple(1)
    movi2 = db.obtener_movimiento_simple(2)

    assert m1 in movimientos and m2 in movimientos
    assert movi.id == 1
    assert movi.nombre == "Destructor"
    assert movi2.id == 2
    assert movi2.nombre == "Golpe Kárate"

    with pytest.raises(HTTPException):
        db.obtener_movimiento_simple(999)


def test_cargar_y_obtener_generaciones(db: Database):
    gen1 = Generacion(id=1, nombre="Generacion I")
    gen2 = Generacion(id=2, nombre="Generacion II")
    gen3 = Generacion(id=3, nombre="Generacion III")
    gen4 = Generacion(id=4, nombre="Generacion IV")

    db.cargar_generaciones([gen1, gen2, gen3, gen4])

    generaciones = db.obtener_generaciones()

    assert gen1 in generaciones and gen2 in generaciones
    assert gen3 in generaciones and gen4 in generaciones


def test_cargar_y_obtener_tipos(db: Database):
    p1 = Pokemon(
        id=1,
        nombre="Pikachu",
        imagen="una imagen",
        generaciones=[],
        tipos=[
            Tipo(id=12, nombre="Planta", debilidades=[]),
            Tipo(id=4, nombre="Veneno", debilidades=[]),
        ],
        altura=8,
        peso=9,
    )
    p2 = Pokemon(
        id=2,
        nombre="Charmander",
        imagen="una imagen",
        generaciones=[],
        tipos=[Tipo(id=10, nombre="Fuego", debilidades=[])],
        altura=10,
        peso=11,
    )
    t1 = Tipo(id=4, nombre="Veneno", debilidades=[])
    t2 = Tipo(id=12, nombre="Planta", debilidades=[])
    t3 = Tipo(id=10, nombre="Fuego", debilidades=[])
    db.cargar_tipos([t1, t2, t3])
    db.cargar_pokemones([p1, p2])
    tipos = db.obtener_tipos()
    assert t1 in tipos and t2 in tipos and t3 in tipos


def test_cargar_obtener_movimientos_pokemon(db: Database):
    m1 = Movimiento(
        id=1,
        nombre="Destructor",
        generacion={"id": 1, "nombre": "Generación I"},
        tipo={"id": 1, "nombre": "Normal"},
        categoria="físico",
        potencia=40,
        precision=100,
        puntos_de_poder=35,
        efecto="Inflicts regular damage with no additional effect.",
    )
    m2 = Movimiento(
        id=2,
        nombre="Golpe Kárate",
        generacion={"id": 1, "nombre": "Generación I"},
        tipo={"id": 2, "nombre": "Lucha"},
        categoria="físico",
        potencia=50,
        precision=100,
        puntos_de_poder=25,
        efecto="Has an increased chance for a critical hit.",
    )
    db.cargar_movimientos([m1, m2])
    db.cargar_pokemon_moves_csv(
        [
            {"linea_pokemon_id": 1, "linea_move_id": 1, "linea_move_method_id": 1},
            {"linea_pokemon_id": 1, "linea_move_id": 2, "linea_move_method_id": 2},
            {"linea_pokemon_id": 1, "linea_move_id": 1, "linea_move_method_id": 2},
        ]
    )
    movimientos_huevo, movimientos_maquina, movimientos_nivel = (
        db.obtener_movimientos_pokemon(1)
    )

    assert m2 in movimientos_huevo
    assert m1 in movimientos_nivel
    assert m1 in movimientos_huevo
    assert movimientos_maquina == []


def generaciones_validas():
    generaciones = [
        Generacion(id=1, nombre="Generacion I"),
        Generacion(id=2, nombre="Generacion II"),
        Generacion(id=3, nombre="Generacion III"),
        Generacion(id=4, nombre="Generacion IV"),
        Generacion(id=5, nombre="Generacion V"),
        Generacion(id=6, nombre="Generacion VI"),
        Generacion(id=7, nombre="Generacion VII"),
        Generacion(id=8, nombre="Generacion VIII"),
    ]
    return generaciones


def test_cargar_obtener_equipos_exitosos(db: Database):
    eq1 = EQUIPO1
    eq2 = EQUIPO2
    db.cargar_equipos([eq1, eq2])
    equipo_1 = db.obtener_equipo(1)
    equipo_2 = db.obtener_equipo(2)
    assert equipo_1.id == 1
    assert equipo_2.id == 2
    assert equipo_1.nombre == "404 not found"
    assert equipo_2.generacion.id == 3
    assert equipo_1.integrantes == []

    assert len(db.listar_equipos()) == 2
    equipo_a_crear = EquipooUpsert(nombre="los 404 fantasticos", id_generacion=8)
    db.cargar_generaciones(generaciones_validas())
    db.add(equipo_a_crear)
    assert len(db.listar_equipos()) == 3


def test_cargar_obtener_equipos_casos_borde(db: Database):
    db.cargar_generaciones(generaciones_validas())
    eq1 = EQUIPO1
    eq2 = EQUIPO2
    db.cargar_equipos([eq1, eq2])
    with pytest.raises(HTTPException) as excepcion:
        db.obtener_equipo(10)
    assert excepcion.value.status_code == 404

    equipo_a_crear = EquipooUpsert(nombre="los 404 fantasticos", id_generacion=99)
    with pytest.raises(HTTPException) as excepcion:
        db.add(equipo_a_crear)
    assert excepcion.value.status_code == 404

    equipo_a_crear = EquipooUpsert(nombre="los 4 fantasticos", id_generacion=3)
    with pytest.raises(HTTPException) as excepcion:
        db.add(equipo_a_crear)
    assert excepcion.value.status_code == 400

    assert len(db.listar_equipos()) == 2


def test_eliminar_equipos_casos_validos_y_borde(db: Database):
    db.cargar_generaciones(generaciones_validas())
    eq1 = EQUIPO1
    eq2 = EQUIPO2
    db.cargar_equipos([eq1, eq2])
    with pytest.raises(HTTPException) as excepcion:
        db.delete(10)
    assert excepcion.value.status_code == 404

    assert len(db.listar_equipos()) == 2
    db.delete(1)
    assert len(db.listar_equipos()) == 1


def test_agregar_integrante_casos_validos(db: Database):
    db.cargar_generaciones(generaciones_validas())
    p1 = POKEMON1
    p2 = Pokemon(
        id=2,
        nombre="Charmander",
        imagen="una imagen",
        generaciones=GENERACIONES,
        tipos=[],
        altura=10,
        peso=11,
    )
    db.cargar_pokemones([p1, p2])
    eq1 = EQUIPO1
    eq2 = EQUIPO2
    integrante_upsert = IntegranteUpsert(id_pokemon=30, apodo="capicuy")
    integrante = Integrante(
        id=1,
        apodo="capicuy",
        pokemon=Pokemon(
            id=30,
            nombre="Nidoran",
            imagen="una imagen",
            generaciones=GENERACIONES,
            tipos=[],
            altura=8,
            peso=9,
        ),
        movimientos=[],
    )
    db.cargar_equipos([eq1, eq2])
    db.add_integrante(eq1.id, integrante_upsert)
    assert eq1.integrantes == [integrante]
    assert integrante.apodo == integrante_upsert.apodo
    assert integrante.pokemon.id == integrante_upsert.id_pokemon
    db.delete_integrante(eq1.id, integrante.id)


def test_agregar_integrante_casos_borde(db: Database):
    db.cargar_generaciones(generaciones_validas())
    p1 = POKEMON1
    p2 = POKEMON2
    db.cargar_pokemones([p1, p2])
    eq1 = EQUIPO1
    eq2 = EQUIPO2
    integrante_upsert = IntegranteUpsert(id_pokemon=30, apodo="capicuy")

    db.cargar_equipos([eq1, eq2])
    with pytest.raises(HTTPException) as excepcion:
        db.add_integrante(50, integrante_upsert)
    assert excepcion.value.status_code == 404
    integrante_upsert = IntegranteUpsert(id_pokemon=0, apodo="capimaligno")
    with pytest.raises(HTTPException) as excepcion:
        db.add_integrante(eq1.id, integrante_upsert)
    assert excepcion.value.status_code == 404

    integrante_upsert = IntegranteUpsert(id_pokemon=2, apodo="rex_de_octava_generacion")
    with pytest.raises(HTTPException) as excepcion:
        db.add_integrante(eq1.id, integrante_upsert)
    assert excepcion.value.status_code == 400

    integrante_upsert = IntegranteUpsert(id_pokemon=30, apodo="vale_por_6")
    for i in range(6):
        db.add_integrante(eq1.id, integrante_upsert)
    with pytest.raises(HTTPException) as excepcion:
        db.add_integrante(eq1.id, integrante_upsert)
    assert excepcion.value.status_code == 400
    for i in range(6):
        db.delete_integrante(eq1.id, i + 1)


def test_actualizar_equipo_casos_validos(db: Database):
    db.cargar_generaciones(generaciones_validas())
    p1 = POKEMON1
    p2 = POKEMON2
    db.cargar_pokemones([p1, p2])
    eq1 = EQUIPO1
    eq2 = EQUIPO2
    integrante_upsert = IntegranteUpsert(id_pokemon=30, apodo="capicuy")
    equipo_upsert = EquipooUpsert(nombre="los 404 fantasticos", id_generacion=8)
    db.cargar_equipos([eq1, eq2])

    db.add_integrante(eq1.id, integrante_upsert)
    db.update_equipos(eq1.id, equipo_upsert)
    assert len(db.listar_equipos()) == 2
    assert eq1.nombre == equipo_upsert.nombre
    assert eq1.generacion.id == equipo_upsert.id_generacion


def test_actualizar_equipo_casos_borde(db: Database):
    db.cargar_generaciones(generaciones_validas())
    p1 = POKEMON1
    p2 = POKEMON2
    db.cargar_pokemones([p1, p2])
    eq1 = EQUIPO1
    eq2 = EQUIPO2
    equipo_upsert = EquipooUpsert(nombre="los 4 fantasticos", id_generacion=8)
    db.cargar_equipos([eq1, eq2])
    with pytest.raises(HTTPException) as excepcion:
        db.update_equipos(eq1.id, equipo_upsert)
    assert excepcion.value.status_code == 400

    equipo_upsert = EquipooUpsert(nombre="los 404 fantasticos", id_generacion=99)
    with pytest.raises(HTTPException) as excepcion:
        db.update_equipos(eq1.id, equipo_upsert)
    assert excepcion.value.status_code == 404

    integrante_upsert = IntegranteUpsert(id_pokemon=2, apodo="capicuy de fuego")
    equipo_upsert = EquipooUpsert(nombre="los 404 fantasticos", id_generacion=2)
    db.add_integrante(eq1.id, integrante_upsert)
    with pytest.raises(HTTPException) as excepcion:
        db.update_equipos(eq1.id, equipo_upsert)
    assert excepcion.value.status_code == 400
    db.delete_integrante(eq1.id, 2)
    assert len(db.listar_equipos()) == 2


def test_eliminar_integrante_casos_validos(db: Database):
    db.cargar_generaciones(generaciones_validas())
    p1 = POKEMON1
    p2 = POKEMON2
    db.cargar_pokemones([p1, p2])
    eq1 = EQUIPO1
    eq2 = EQUIPO2
    integrante_upsert = IntegranteUpsert(id_pokemon=30, apodo="capicuy")
    equipo_upsert = EquipooUpsert(nombre="los 404 fantasticos", id_generacion=8)
    db.cargar_equipos([eq1, eq2])

    db.add_integrante(eq1.id, integrante_upsert)
    db.update_equipos(eq1.id, equipo_upsert)
    assert len(db.listar_equipos()) == 2
    assert eq1.nombre == equipo_upsert.nombre
    assert eq1.generacion.id == equipo_upsert.id_generacion


def test_eliminar_integrante_casos_borde(db: Database):
    db.cargar_generaciones(generaciones_validas())
    p1 = POKEMON1
    p2 = POKEMON2
    db.cargar_pokemones([p1, p2])
    eq1 = EQUIPO1
    eq2 = EQUIPO2
    equipo_upsert = EquipooUpsert(nombre="los 4 fantasticos", id_generacion=8)
    db.cargar_equipos([eq1, eq2])

    integrante_upsert = IntegranteUpsert(id_pokemon=2, apodo="capicuy de fuego")
    db.add_integrante(eq1.id, integrante_upsert)
    with pytest.raises(HTTPException) as excepcion:
        db.delete_integrante(20, equipo_upsert)
    assert excepcion.value.status_code == 404
    with pytest.raises(HTTPException) as excepcion:
        db.delete_integrante(
            eq1.id, IntegranteUpsert(id_pokemon=20, apodo="capicuy de fuego")
        )
    assert excepcion.value.status_code == 404
