from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from fastapi import HTTPException

from database.database import Database
from dependencias.dependencias import get_database
from main import app
from modelos.modelos import (
    Generacion,
    Equipo,
    Integrante,
    Pokemon,
)
from constantes.constantes import (
    MOCK_EQUIPO_ACTUALIZAR,
    MOCK_EQUIPO_CREAR1,
    MOCK_EQUIPO_CREAR2,
    MOCK_INTEGRANTE_ELIMINAR,
    MOCK_LISTA_EQUIPOS,
)

client = TestClient(app)

mock_db = MagicMock(Database)
app.dependency_overrides[get_database] = lambda: mock_db


############ TEST EQUIPOS #############


def test_listar_equipos_lista_con_equipos():
    equipo_mock = MOCK_LISTA_EQUIPOS
    mock_db.listar_equipos.return_value = equipo_mock

    response = client.get("/api/equipos")

    assert response.status_code == 200
    content = response.json()
    assert content[0]["nombre"] == "los testeadores"
    assert content[0]["generacion"]["id"] == 8
    assert content[0]["integrantes"] == []


def test_listar_equipos_lista_vacia():
    equipo_mock = []
    mock_db.listar_equipos.return_value = equipo_mock

    response = client.get("/api/equipos")

    assert response.status_code == 200
    content = response.json()
    assert content == []


def test_crear_equipos_generacion_y_nombre_validos():
    equipo_crear = {
        "nombre": "los testeadores 4 el test fantasma",
        "id_generacion": 8,
    }
    equipo_creado = MOCK_EQUIPO_CREAR2
    mock_db.add.return_value = equipo_creado

    response = client.post("/api/equipos", json=equipo_crear)

    assert response.status_code == 201
    content = response.json()
    assert content["id"] == 1
    assert content["generacion"]["nombre"] == "Generacion VIII"
    assert content["integrantes"] == []


def test_crear_equipos_generacion_invalida():
    mock_db = MagicMock(Database)
    app.dependency_overrides[get_database] = lambda: mock_db

    equipo_crear = {
        "nombre": "los testeadores 4 el test fantasma",
        "id_generacion": 98,
    }
    mock_db.add.side_effect = HTTPException(
        status_code=400, detail="La generación con id 98 no existe"
    )

    response = client.post("/api/equipos", json=equipo_crear)

    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "La generación con id 98 no existe"


def test_obtener_equipo_id_valido():
    mock_db = MagicMock(Database)
    app.dependency_overrides[get_database] = lambda: mock_db

    equipo_creado = MOCK_EQUIPO_CREAR2

    mock_db.obtener_equipo.return_value = equipo_creado

    response = client.get("/api/equipos/1")
    content = response.json()
    assert response.status_code == 200
    assert content["nombre"] == "los testeadores 4 el test fantasma"
    assert content["generacion"]["id"] == 8
    assert content["integrantes"] == []


def test_obtener_equipo_id_invalido():
    mock_db = MagicMock(Database)
    app.dependency_overrides[get_database] = lambda: mock_db

    equipo_creado = MOCK_EQUIPO_CREAR2

    mock_db.obtener_equipo.return_value = equipo_creado
    mock_db.obtener_equipo.side_effect = HTTPException(
        status_code=404, detail="Equipo no encontrado"
    )
    response = client.get("/api/equipos/99")

    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Equipo no encontrado"


def test_eliminar_equipo_id_valido():
    mock_db = MagicMock(Database)
    app.dependency_overrides[get_database] = lambda: mock_db

    equipo_creado = MOCK_EQUIPO_CREAR2

    mock_db.delete.return_value = equipo_creado

    response = client.delete("/api/equipos/1")

    content = response.json()
    assert response.status_code == 200
    assert content["nombre"] == "los testeadores 4 el test fantasma"
    assert content["generacion"]["id"] == 8
    assert content["integrantes"] == []


def test_eliminar_equipo_id_invalido():
    mock_db = MagicMock(Database)
    app.dependency_overrides[get_database] = lambda: mock_db

    equipo_creado = MOCK_EQUIPO_CREAR2

    mock_db.delete.return_value = equipo_creado
    mock_db.delete.side_effect = HTTPException(
        status_code=404, detail="Equipo no encontrado"
    )
    response = client.delete("/api/equipos/99")

    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Equipo no encontrado"


def test_agregar_integrante_valido():
    mock_db = MagicMock(Database)
    app.dependency_overrides[get_database] = lambda: mock_db
    equipo_creado = MOCK_EQUIPO_CREAR2
    integrante_crear = {"id_pokemon": 30, "apodo": "perrito"}
    integrante_creado = Integrante(
        id=1,
        apodo="perrito",
        pokemon=Pokemon(
            id=30,
            nombre="nidorino",
            imagen="una imagen",
            altura=10,
            peso=10,
            generaciones=[],
            tipos=[],
        ),
        movimientos=[],
    )

    mock_db.add.return_value = equipo_creado
    mock_db.add_integrante.return_value = integrante_creado
    response = client.post("/api/equipos/1/integrantes", json=integrante_crear)

    assert response.status_code == 200
    content = response.json()
    assert content["id"] == 1
    assert content["pokemon"]["id"] == 30
    assert content["pokemon"]["nombre"] == "nidorino"
    assert content["movimientos"] == []


def test_agregar_integrante_equipo_no_encontrado():
    mock_db = MagicMock(Database)
    app.dependency_overrides[get_database] = lambda: mock_db
    integrante_crear = {"id_pokemon": 30, "apodo": "perrito"}

    mock_db.add_integrante.side_effect = HTTPException(
        status_code=404, detail="Equipo de id 2 no encontrado"
    )

    response = client.post("/api/equipos/2/integrantes", json=integrante_crear)
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Equipo de id 2 no encontrado"


def test_agregar_integrante_id_pokemon_no_encontrado():
    mock_db = MagicMock(Database)
    app.dependency_overrides[get_database] = lambda: mock_db
    integrante_crear = {"id_pokemon": 1000, "apodo": "perrote"}

    mock_db.add_integrante.side_effect = HTTPException(
        status_code=404, detail="Pokemon de id 1000 no encontrado"
    )

    response = client.post("/api/equipos/1/integrantes", json=integrante_crear)
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Pokemon de id 1000 no encontrado"


def test_agregar_integrante_generacion_del_integrante_no_valida():
    mock_db = MagicMock(Database)
    app.dependency_overrides[get_database] = lambda: mock_db
    integrante_crear = {"id_pokemon": 30, "apodo": "perrito"}

    mock_db.add_integrante.side_effect = HTTPException(
        status_code=400,
        detail="Generacion del pokemon no pertenece a la generacion del equipo",
    )

    response = client.post("/api/equipos/1/integrantes", json=integrante_crear)
    assert response.status_code == 400
    content = response.json()
    assert (
        content["detail"]
        == "Generacion del pokemon no pertenece a la generacion del equipo"
    )


def test_agregar_integrante_con_equipo_lleno():
    mock_db = MagicMock(Database)
    app.dependency_overrides[get_database] = lambda: mock_db
    integrante_crear = {"id_pokemon": 30, "apodo": "perrito"}

    mock_db.add_integrante.side_effect = HTTPException(
        status_code=400,
        detail="Se alcanzo la maxima cantidad de integrantes: 6",
    )

    response = client.post("/api/equipos/1/integrantes", json=integrante_crear)
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Se alcanzo la maxima cantidad de integrantes: 6"


def test_actuaizar_equipo_caso_valido():
    mock_db = MagicMock(Database)
    app.dependency_overrides[get_database] = lambda: mock_db
    equipo_actualizar = {
        "nombre": "los testeadors 5 el test contraataca",
        "id_generacion": 8,
    }
    equipo_creado = MOCK_EQUIPO_CREAR1
    equipo_actualizado = MOCK_EQUIPO_ACTUALIZAR
    mock_db.add.return_value = equipo_creado
    mock_db.update_equipos.return_value = equipo_actualizado

    response = client.put("/api/equipos/1", json=equipo_actualizar)
    assert response.status_code == 200
    content = response.json()
    assert content["nombre"] == "los testeadors 5 el test contraataca"
    assert content["generacion"]["id"] == 8


def test_actuaizar_equipo_generacion_invalida():
    mock_db = MagicMock(Database)
    app.dependency_overrides[get_database] = lambda: mock_db
    equipo_actualizar = {
        "nombre": "los testeadors 5 el test contraataca",
        "id_generacion": 98,
    }
    equipo_creado = MOCK_EQUIPO_CREAR1
    equipo_actualizado = MOCK_EQUIPO_ACTUALIZAR
    mock_db.add.return_value = equipo_creado
    mock_db.update_equipos.return_value = equipo_actualizado
    mock_db.update_equipos.side_effect = HTTPException(
        status_code=404,
        detail="La generación con id 98 no existe",
    )

    response = client.put("/api/equipos/1", json=equipo_actualizar)
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "La generación con id 98 no existe"


def test_actuaizar_equipo_nombre_equipo_repetido():
    mock_db = MagicMock(Database)
    app.dependency_overrides[get_database] = lambda: mock_db
    equipo_actualizar = {
        "nombre": "los testeadors 5 el test contraataca",
        "id_generacion": 98,
    }
    equipo_creado = MOCK_EQUIPO_CREAR1
    equipo_creado2 = Equipo(
        id=2,
        nombre="los testeadores 5 el test contraataca",
        generacion=Generacion(id=5, nombre="Generacion V"),
        integrantes=[],
    )

    mock_db.add.side_effect = [equipo_creado, equipo_creado2]
    mock_db.update_equipos.side_effect = HTTPException(
        status_code=400,
        detail="Ya existe un equipo con ese nombre: los testeadors 5 el test contraataca",
    )

    response = client.put("/api/equipos/1", json=equipo_actualizar)
    assert response.status_code == 400
    content = response.json()
    assert (
        content["detail"]
        == "Ya existe un equipo con ese nombre: los testeadors 5 el test contraataca"
    )


def test_actuaizar_equipo_nombre_equipo_repetido():
    mock_db = MagicMock(Database)
    app.dependency_overrides[get_database] = lambda: mock_db
    equipo_actualizar = {
        "nombre": "los testeadors 5 el test contraataca",
        "id_generacion": 2,
    }
    equipo_creado = MOCK_EQUIPO_CREAR1
    mock_db.add.return_value = equipo_creado
    mock_db.update_equipos.side_effect = HTTPException(
        status_code=400,
        detail="Un pokemon no es valido para la generacion 2",
    )

    response = client.put("/api/equipos/1", json=equipo_actualizar)
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Un pokemon no es valido para la generacion 2"


def test_eliminar_integrante_caso_valido():
    mock_db = MagicMock(Database)
    app.dependency_overrides[get_database] = lambda: mock_db
    equipo_creado = MOCK_EQUIPO_CREAR1
    integrante_eliminado = MOCK_INTEGRANTE_ELIMINAR
    mock_db.add.return_value = equipo_creado
    mock_db.add_integrante.return_value = integrante_eliminado
    mock_db.delete_integrante.return_value = integrante_eliminado
    response = client.delete("/api/equipos/1/integrantes/1")
    assert response.status_code == 200
    content = response.json()
    assert content["apodo"] == "perrito"
    assert content["pokemon"]["nombre"] == "nidorina"
    assert content["movimientos"] == []


def test_eliminar_integrante_id_equipo_no_encontrado():
    mock_db = MagicMock(Database)
    app.dependency_overrides[get_database] = lambda: mock_db
    equipo_creado = MOCK_EQUIPO_CREAR1
    integrante = MOCK_INTEGRANTE_ELIMINAR
    mock_db.add.return_value = equipo_creado
    mock_db.add_integrante.return_value = integrante
    mock_db.delete_integrante.side_effect = HTTPException(
        status_code=404,
        detail="El equipo de id 10 no fue encontrado",
    )
    response = client.delete("/api/equipos/10/integrantes/1")
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "El equipo de id 10 no fue encontrado"


def test_eliminar_integrante_id_integrante_no_encontrado():
    mock_db = MagicMock(Database)
    app.dependency_overrides[get_database] = lambda: mock_db
    equipo_creado = MOCK_EQUIPO_CREAR1
    integrante = MOCK_INTEGRANTE_ELIMINAR
    mock_db.add.return_value = equipo_creado
    mock_db.add_integrante.return_value = integrante
    mock_db.delete_integrante.side_effect = HTTPException(
        status_code=404,
        detail="Integrante de id 2 no encontrado en este equipo",
    )
    response = client.delete("/api/equipos/1/integrantes/2")
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Integrante de id 2 no encontrado en este equipo"
