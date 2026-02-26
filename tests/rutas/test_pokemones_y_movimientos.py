from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from database.database import Database
from dependencias.dependencias import get_database
from main import app
from modelos.modelos import (
    Estadisticas,
    Generacion,
    Habilidades,
    Pokemon,
)

from constantes.constantes import MOCK_LISTA_MOVIMIENTOS, MOCK_LISTA_POKEMONES


client = TestClient(app)

mock_db = MagicMock(Database)
app.dependency_overrides[get_database] = lambda: mock_db


# ENDPOINTS POKEMON
# GET /api/pokemon/{id}
# CASOS DE ERROR
def test_get_pokemon_id_inexistente():
    mock_db.get.return_value = None

    response = client.get("/api/pokemon/9999")

    assert response.status_code == 404
    content = response.json()

    assert content["detail"] == "Pokemon no encontrado"


def test_obtener_pokemon_id_invalido_texto():
    response = client.get("/api/pokemon/abc")

    assert response.status_code == 422
    content = response.json()

    assert (
        content["detail"][0]["msg"]
        == "Input should be a valid integer, unable to parse string as an integer"
    )


def test_obtener_pokemon_id_invalido_negativo():
    response = client.get("/api/pokemon/-1")

    assert response.status_code == 422
    content = response.json()
    assert content["detail"] == "El ID no puede ser negativo"


#                   CASOS BORDE
def test_obtener_pokemon_id_minimo_valido():
    bulbasaur = Pokemon(
        id=1,
        nombre="bulbasaur",
        imagen="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
        altura=0.7,
        peso=6.9,
        generaciones=[],
        tipos=[],
    )

    estadisticas = Estadisticas(
        ataque=49,
        defensa=49,
        ataque_especial=65,
        defensa_especial=65,
        puntos_de_golpe=45,
        velocidad=45,
    )

    habilidades = [
        Habilidades(id=65, nombre="Clorofila"),
        Habilidades(id=34, nombre="Espesura"),
    ]
    movimientos_huevo = []
    movimientos_maquina = [
        {
            "id": 14,
            "nombre": "Danza Espada",
            "generacion": {"id": 1, "nombre": "Generación I"},
            "tipo": {"id": 1, "nombre": "Normal"},
            "categoria": "estado",
            "potencia": 0,
            "precision": 0,
            "puntos_de_poder": 0,
            "efecto": "Raises the user's Attack by two stages.",
        }
    ]
    movimientos_nivel = [
        {
            "id": 22,
            "nombre": "Látigo Cepa",
            "generacion": {"id": 1, "nombre": "Generación I"},
            "tipo": {"id": 12, "nombre": "Planta"},
            "categoria": "físico",
            "potencia": 45,
            "precision": 100,
            "puntos_de_poder": 25,
            "efecto": "Inflicts regular damage with no additional effect.",
        }
    ]

    mock_db.get.return_value = bulbasaur
    mock_db.get_estadisticas.return_value = estadisticas
    mock_db.get_habilidades.return_value = habilidades
    mock_db.get_evoluciones.return_value = []
    mock_db.obtener_movimientos_pokemon.return_value = (
        movimientos_huevo,
        movimientos_maquina,
        movimientos_nivel,
    )

    response = client.get("/api/pokemon/1")

    assert response.status_code == 200
    content = response.json()

    assert content["id"] == 1
    assert content["nombre"] == "bulbasaur"
    assert content["imagen"] == bulbasaur.imagen
    assert content["altura"] == 0.7
    assert content["peso"] == 6.9

    assert content["estadisticas"]["ataque"] == 49
    assert content["estadisticas"]["defensa"] == 49
    assert content["estadisticas"]["ataque_especial"] == 65
    assert content["estadisticas"]["defensa_especial"] == 65
    assert content["estadisticas"]["puntos_de_golpe"] == 45
    assert content["estadisticas"]["velocidad"] == 45

    assert len(content["habilidades"]) == 2
    assert content["habilidades"][0]["id"] == 65
    assert content["habilidades"][0]["nombre"] == "Clorofila"
    assert content["habilidades"][1]["id"] == 34
    assert content["habilidades"][1]["nombre"] == "Espesura"

    assert content["movimientos_huevo"] == []
    assert content["movimientos_maquina"][0]["id"] == 14
    assert content["movimientos_nivel"][0]["id"] == 22


def test_obtener_pokemon_con_multiples_generaciones_y_tipos():
    charizard = Pokemon(
        id=6,
        nombre="charizard",
        imagen="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png",
        altura=1.7,
        peso=90.5,
        generaciones=[
            {"id": 1, "nombre": "Generación I"},
            {"id": 2, "nombre": "Generación II"},
            {"id": 3, "nombre": "Generación III"},
            {"id": 4, "nombre": "Generación IV"},
            {"id": 5, "nombre": "Generación V"},
            {"id": 6, "nombre": "Generación VI"},
            {"id": 7, "nombre": "Generación VII"},
            {"id": 8, "nombre": "Generación VIII"},
        ],
        tipos=[
            {"id": 10, "nombre": "Fuego"},
            {"id": 3, "nombre": "Volador"},
        ],
    )

    estadisticas = Estadisticas(
        ataque=84,
        defensa=78,
        ataque_especial=109,
        defensa_especial=85,
        puntos_de_golpe=78,
        velocidad=100,
    )

    habilidades = [
        Habilidades(id=66, nombre="Mar Llamas"),
        Habilidades(id=94, nombre="Poder Solar"),
    ]
    movimientos_huevo = []
    movimientos_maquina = [
        {
            "id": 5,
            "nombre": "Megapuño",
            "generacion": {"id": 1, "nombre": "Generación I"},
            "tipo": {"id": 1, "nombre": "Normal"},
            "categoria": "físico",
            "potencia": 80,
            "precision": 85,
            "puntos_de_poder": 20,
            "efecto": "Inflicts regular damage with no additional effect.",
        }
    ]
    movimientos_nivel = [
        {
            "id": 10,
            "nombre": "Arañazo",
            "generacion": {"id": 1, "nombre": "Generación I"},
            "tipo": {"id": 1, "nombre": "Normal"},
            "categoria": "físico",
            "potencia": 40,
            "precision": 100,
            "puntos_de_poder": 35,
            "efecto": "Inflicts regular damage with no additional effect.",
        }
    ]

    mock_db.get.return_value = charizard
    mock_db.get_estadisticas.return_value = estadisticas
    mock_db.get_habilidades.return_value = habilidades
    mock_db.obtener_movimientos_pokemon.return_value = (
        movimientos_huevo,
        movimientos_maquina,
        movimientos_nivel,
    )
    mock_db.get_evoluciones.return_value = []

    response = client.get("/api/pokemon/6")

    assert response.status_code == 200
    content = response.json()

    assert content["id"] == 6
    assert content["nombre"] == "charizard"
    assert len(content["generaciones"]) == 8
    assert len(content["tipos"]) == 2
    assert {"debilidades": [], "id": 10, "nombre": "Fuego"} in content["tipos"]
    assert {"debilidades": [], "id": 3, "nombre": "Volador"} in content["tipos"]
    assert content["estadisticas"]["ataque"] == 84
    assert content["habilidades"][0]["nombre"] == "Mar Llamas"
    assert content["habilidades"][1]["nombre"] == "Poder Solar"
    assert content["movimientos_huevo"] == []
    assert content["movimientos_maquina"][0]["id"] == 5
    assert content["movimientos_nivel"][0]["id"] == 10


### Pokemon con movimientos sólo de una categoría (por nivel, máquina o huevo).
### Pokemon sin movimientos de huevo / sin evoluciones / sin habilidades ocultas.


# CASOS GENERALES
def test_obtener_pokemon_con_un_tipo_y_una_evolucion():
    nidorina = Pokemon(
        id=30,
        nombre="nidorina",
        imagen="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/30.png",
        altura=0.8,
        peso=20,
        generaciones=[{"id": 1, "nombre": "Generación I"}],
        tipos=[{"id": 4, "nombre": "Veneno"}],
    )

    estadisticas = Estadisticas(
        ataque=62,
        defensa=67,
        ataque_especial=55,
        defensa_especial=55,
        puntos_de_golpe=70,
        velocidad=56,
    )

    habilidades = [
        Habilidades(id=38, nombre="Punto Tóxico"),
        Habilidades(id=79, nombre="Rivalidad"),
        Habilidades(id=55, nombre="Entusiasmo"),
    ]

    evoluciones = [{"id": 31, "nombre": "nidoqueen"}]

    movimientos_huevo = []
    movimientos_maquina = [
        {
            "id": 32,
            "nombre": "Perforador",
            "generacion": {"id": 1, "nombre": "Generación I"},
            "tipo": {"id": 1, "nombre": "Normal"},
            "categoria": "físico",
            "potencia": 0,
            "precision": 30,
            "puntos_de_poder": 5,
            "efecto": "Causes a one-hit KO.",
        },
    ]
    movimientos_nivel = [
        {
            "id": 10,
            "nombre": "Arañazo",
            "generacion": {"id": 1, "nombre": "Generación I"},
            "tipo": {"id": 1, "nombre": "Normal"},
            "categoria": "físico",
            "potencia": 40,
            "precision": 100,
            "puntos_de_poder": 35,
            "efecto": "Inflicts regular damage with no additional effect.",
        },
    ]

    mock_db.get.return_value = nidorina
    mock_db.get_estadisticas.return_value = estadisticas
    mock_db.get_habilidades.return_value = habilidades
    mock_db.get_evoluciones.return_value = evoluciones
    mock_db.obtener_movimientos_pokemon.return_value = (
        movimientos_huevo,
        movimientos_maquina,
        movimientos_nivel,
    )

    response = client.get("/api/pokemon/30")

    assert response.status_code == 200
    content = response.json()

    assert content["id"] == 30
    assert content["nombre"] == "nidorina"
    assert len(content["tipos"]) == 1
    assert content["tipos"][0]["nombre"] == "Veneno"
    assert len(content["evoluciones"]) == 1
    assert content["evoluciones"][0]["nombre"] == "nidoqueen"
    assert content["estadisticas"]["ataque"] == 62
    assert len(content["habilidades"]) == 3
    assert content["movimientos_huevo"] == []
    assert content["movimientos_maquina"][0]["id"] == 32
    assert content["movimientos_nivel"][0]["id"] == 10


def test_obtener_pokemon_con_multiples_tipos_habilidades_y_evoluciones():
    eevee = Pokemon(
        id=133,
        nombre="eevee",
        imagen="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/133.png",
        altura=0.3,
        peso=6.5,
        generaciones=[{"id": 1, "nombre": "Generación I"}],
        tipos=[{"id": 1, "nombre": "Normal"}, {"id": 18, "nombre": "Hada"}],
    )

    estadisticas = Estadisticas(
        ataque=55,
        defensa=50,
        ataque_especial=45,
        defensa_especial=65,
        puntos_de_golpe=55,
        velocidad=55,
    )

    habilidades = [
        Habilidades(id=50, nombre="Fuga"),
        Habilidades(id=91, nombre="Adaptable"),
        Habilidades(id=99, nombre="Anticipación"),
    ]

    evoluciones = [
        {"id": 134, "nombre": "vaporeon"},
        {"id": 135, "nombre": "jolteon"},
        {"id": 136, "nombre": "flareon"},
        {"id": 196, "nombre": "espeon"},
        {"id": 197, "nombre": "umbreon"},
        {"id": 470, "nombre": "leafeon"},
        {"id": 471, "nombre": "glaceon"},
        {"id": 700, "nombre": "sylveon"},
    ]
    movimientos_huevo = []
    movimientos_maquina = [
        {
            "id": 34,
            "nombre": "Golpe Cuerpo",
            "generacion": {"id": 1, "nombre": "Generación I"},
            "tipo": {"id": 1, "nombre": "Normal"},
            "categoria": "físico",
            "potencia": 85,
            "precision": 100,
            "puntos_de_poder": 15,
            "efecto": "Has a $effect_chance% chance to [paralyze]{mechanic:paralysis} the target.",
        },
        {
            "id": 36,
            "nombre": "Derribo",
            "generacion": {"id": 1, "nombre": "Generación I"},
            "tipo": {"id": 1, "nombre": "Normal"},
            "categoria": "físico",
            "potencia": 90,
            "precision": 85,
            "puntos_de_poder": 20,
            "efecto": "User receives 1/4 the damage it inflicts in recoil.",
        },
    ]
    movimientos_nivel = [
        {
            "id": 28,
            "nombre": "Ataque Arena",
            "generacion": {"id": 1, "nombre": "Generación I"},
            "tipo": {"id": 5, "nombre": "Tierra"},
            "categoria": "estado",
            "potencia": 0,
            "precision": 0,
            "puntos_de_poder": 0,
            "efecto": "Lowers the target's accuracy by one stage.",
        },
        {
            "id": 33,
            "nombre": "Placaje",
            "generacion": {"id": 1, "nombre": "Generación I"},
            "tipo": {"id": 1, "nombre": "Normal"},
            "categoria": "físico",
            "potencia": 40,
            "precision": 100,
            "puntos_de_poder": 35,
            "efecto": "Inflicts regular damage with no additional effect.",
        },
        {
            "id": 36,
            "nombre": "Derribo",
            "generacion": {"id": 1, "nombre": "Generación I"},
            "tipo": {"id": 1, "nombre": "Normal"},
            "categoria": "físico",
            "potencia": 90,
            "precision": 85,
            "puntos_de_poder": 20,
            "efecto": "User receives 1/4 the damage it inflicts in recoil.",
        },
    ]

    mock_db.get.return_value = eevee
    mock_db.get_estadisticas.return_value = estadisticas
    mock_db.get_habilidades.return_value = habilidades
    mock_db.get_evoluciones.return_value = evoluciones
    mock_db.obtener_movimientos_pokemon.return_value = (
        movimientos_huevo,
        movimientos_maquina,
        movimientos_nivel,
    )

    response = client.get("/api/pokemon/133")

    assert response.status_code == 200
    content = response.json()

    assert content["id"] == 133
    assert content["nombre"] == "eevee"
    assert len(content["tipos"]) == 2
    assert len(content["habilidades"]) == 3
    assert len(content["evoluciones"]) == 8
    assert content["estadisticas"]["velocidad"] == 55
    assert content["movimientos_huevo"] == []
    assert content["movimientos_maquina"][0]["id"] == 34
    assert content["movimientos_nivel"][0]["id"] == 28


#               Pokemon con todos los tipos de movimientos (nivel, huevo, máquina).


############ TEST GENERACIONES ##########
# nota pasar esto y todos los test de abajo a us respectivos archivos aparte
# nota 2 pasar las ctes al archivo de ctes
# nota para nacho: decirles a los compañeros de que no podes acceder al archivo database bien por estar metido en otra carpeta


def test_generaciones():
    generaciones = [
        Generacion(id=1, nombre="Generación I"),
        Generacion(id=2, nombre="Generación II"),
        Generacion(id=3, nombre="Generación III"),
        Generacion(id=4, nombre="Generación IV"),
    ]
    mock_db.obtener_generaciones.return_value = generaciones
    response = client.get("/api/generaciones")
    assert response.status_code == 200
    content = response.json()
    assert content[0]["id"] == 1
    assert content[1]["id"] == 2
    assert content[2]["id"] == 3
    assert content[3]["id"] == 4


############ TEST LISTA POKEMON ##########


def test_listar_pokemones_valido():
    pokemones = MOCK_LISTA_POKEMONES
    mock_db.obtener_pokemones.return_value = pokemones
    response = client.get("/api/pokemon")
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert content[0]["id"] == 1
    assert content[1]["id"] == 6
    assert content[2]["id"] == 30
    assert len(content[2]["generaciones"]) == 8
    assert len(content[2]["tipos"]) == 2
    assert content[2]["tipos"][0]["id"] == 4


def test_listar_pokemones_parametro_tipo_valido_para_un_solo_individuo():
    pokemones = MOCK_LISTA_POKEMONES
    mock_db.obtener_pokemones.return_value = pokemones
    response = client.get("/api/pokemon?tipo=12")
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert content[0]["id"] == 30
    assert len(content[0]["generaciones"]) == 8
    assert len(content[0]["tipos"]) == 2
    assert content[0]["tipos"][0]["id"] == 4


def test_listar_pokemones_parametro_tipo_valido_para_dos_individuos():
    pokemones = MOCK_LISTA_POKEMONES
    mock_db.obtener_pokemones.return_value = pokemones
    response = client.get("/api/pokemon?tipo=4")
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) == 2
    assert len(content[0]["generaciones"]) == 8
    assert len(content[0]["tipos"]) == 1
    assert content[0]["tipos"][0]["id"] == 4


def test_listar_pokemones_parametro_nombre_valido_para_un_individuo():
    pokemones = MOCK_LISTA_POKEMONES
    mock_db.obtener_pokemones.return_value = pokemones
    response = client.get("/api/pokemon?nombre_parcial=nid")
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) == 1
    assert len(content[0]["generaciones"]) == 8
    assert len(content[0]["tipos"]) == 2


def test_listar_pokemones_parametro_nombre_valido_para_dos_individuos():
    pokemones = MOCK_LISTA_POKEMONES
    mock_db.obtener_pokemones.return_value = pokemones
    response = client.get("/api/pokemon?nombre_parcial=char")
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) == 2
    assert content[0]["nombre"] == "charizard"
    assert content[1]["nombre"] == "charmeleon"
    assert len(content[0]["generaciones"]) == 8
    assert len(content[0]["tipos"]) == 1


def test_listar_pokemones_ambos_parametros_validos():
    pokemones = MOCK_LISTA_POKEMONES
    mock_db.obtener_pokemones.return_value = pokemones
    response = client.get("/api/pokemon?tipo=4&nombre_parcial=char")
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) == 1
    assert content[0]["nombre"] == "charizard"
    assert len(content[0]["generaciones"]) == 8
    assert len(content[0]["tipos"]) == 1


############ TEST LISTA MOVIMIENTOS ##########


def test_listar_movimientos():
    movimientos = MOCK_LISTA_MOVIMIENTOS
    mock_db.obtener_movimientos.return_value = movimientos
    response = client.get("/api/movimientos")
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) == 4
    assert content[0]["nombre"] == "Destructor"
    assert content[1]["nombre"] == "Golpe Kárate"
    assert content[2]["nombre"] == "Doble Bofetón"
    assert content[3]["nombre"] == "Puño Cometa"
    assert content[0]["id"] == 1
    assert content[1]["id"] == 2
    assert content[2]["id"] == 3
    assert content[3]["id"] == 4
    assert content[1]["generacion"]["id"] == 1
    assert content[1]["categoria"] == "físico"
    assert content[1]["efecto"] == "Has an increased chance for a critical hit."


############ TEST MOVIMIENTO ESPECIFICO POR ID ##########


def test_movimiento_id_inexistente():
    mock_db.obtener_movimiento.return_value = None

    response = client.get("/api/movimientos/9999")

    assert response.status_code == 404
    content = response.json()

    assert content["detail"] == "Movimiento no encontrado"
