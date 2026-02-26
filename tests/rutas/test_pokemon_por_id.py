from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from database.database import Database
from dependencias.dependencias import get_database
from main import app
from modelos.modelos import Estadisticas, Habilidades, Pokemon

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


# CASOS BORDE
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

    mock_db.get.return_value = bulbasaur
    mock_db.get_estadisticas.return_value = estadisticas
    mock_db.get_habilidades.return_value = habilidades
    mock_db.get_evoluciones.return_value = []

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

    mock_db.get.return_value = charizard
    mock_db.get_estadisticas.return_value = estadisticas
    mock_db.get_habilidades.return_value = habilidades
    mock_db.get_evoluciones.return_value = []

    response = client.get("/api/pokemon/6")

    assert response.status_code == 200
    content = response.json()

    assert content["id"] == 6
    assert content["nombre"] == "charizard"
    assert len(content["generaciones"]) == 8
    assert len(content["tipos"]) == 2
    assert {"id": 10, "nombre": "Fuego"} in content["tipos"]
    assert {"id": 3, "nombre": "Volador"} in content["tipos"]
    assert content["estadisticas"]["ataque"] == 84
    assert content["habilidades"][0]["nombre"] == "Mar Llamas"
    assert content["habilidades"][1]["nombre"] == "Poder Solar"


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

    mock_db.get.return_value = nidorina
    mock_db.get_estadisticas.return_value = estadisticas
    mock_db.get_habilidades.return_value = habilidades
    mock_db.get_evoluciones.return_value = evoluciones

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

    mock_db.get.return_value = eevee
    mock_db.get_estadisticas.return_value = estadisticas
    mock_db.get_habilidades.return_value = habilidades
    mock_db.get_evoluciones.return_value = evoluciones

    response = client.get("/api/pokemon/133")

    assert response.status_code == 200
    content = response.json()

    assert content["id"] == 133
    assert content["nombre"] == "eevee"
    assert len(content["tipos"]) == 2
    assert len(content["habilidades"]) == 3
    assert len(content["evoluciones"]) == 8
    assert content["estadisticas"]["velocidad"] == 55


# Pokemon con todos los tipos de movimientos (nivel, huevo, máquina).
