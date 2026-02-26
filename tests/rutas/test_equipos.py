from unittest.mock import ANY, MagicMock
from fastapi.testclient import TestClient
from fastapi import HTTPException
import pytest
from sqlmodel import Session
from database.database import Database
from dependencias.dependencias import get_database
from dependencias.dependencias_de_la_db import get_session
from main import app
from modelos.modelos import (
    Estadisticas,
    Generacion,
    Equipo,
    Integrante,
    PokemonIntegrante,
)
from tests.constantes.constantes import (
    MOCK_EQUIPO_ACTUALIZAR,
    MOCK_EQUIPO_CREAR1,
    MOCK_EQUIPO_CREAR2,
    MOCK_INTEGRANTE_ELIMINAR,
    MOCK_LISTA_EQUIPOS,
    MOCK_MOV_228,
    MOCK_MOV_229,
    MOCK_MOV_230,
    MOCK_MOV_231,
    MOCK_MOV_232,
    MOCK_MOV_MOSTRAR_228,
    MOCK_MOV_MOSTRAR_229,
    MOCK_MOV_MOSTRAR_230,
)
from modelos.modelos_de_la_db import EquipoTabla

client = TestClient(app)


@pytest.fixture
def mock_session():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_db():
    return MagicMock(spec=Database)


@pytest.fixture(autouse=True)
def override_dependencies(mock_session, mock_db):
    app.dependency_overrides[get_session] = lambda: mock_session
    app.dependency_overrides[get_database] = lambda: mock_db
    yield
    app.dependency_overrides.clear()


def test_listar_equipos_lista_con_equipos(mock_session, mock_db):
    equipo_mock = MOCK_LISTA_EQUIPOS
    mock_db.get_equipos.return_value = equipo_mock

    response = client.get("/api/equipos")

    assert response.status_code == 200
    content = response.json()
    assert content[0]["nombre"] == "los testeadores"
    assert content[0]["generacion"]["id"] == 8
    assert content[0]["cantidad_integrantes"] == 6
    assert content[1]["cantidad_integrantes"] == 2
    assert content[2]["cantidad_integrantes"] == 3
    mock_db.get_equipos.assert_called_once_with(mock_session)


def test_listar_equipos_lista_vacia(mock_session, mock_db):
    equipo_mock = []
    mock_db.get_equipos.return_value = equipo_mock

    response = client.get("/api/equipos")

    assert response.status_code == 200
    content = response.json()
    assert content == []
    mock_db.get_equipos.assert_called_once_with(mock_session)


def test_crear_equipos_generacion_y_nombre_validos(mock_session, mock_db):
    equipo_crear = {
        "nombre": "los testeadores 4 el test fantasma",
        "id_generacion": 8,
    }
    equipo_creado = MOCK_EQUIPO_CREAR2
    mock_db.create_equipo.return_value = equipo_creado

    response = client.post("/api/equipos", json=equipo_crear)

    assert response.status_code == 201
    content = response.json()
    assert content["id"] == 1
    assert content["generacion"]["nombre"] == "Generacion VIII"
    assert content["integrantes"] == []
    mock_db.create_equipo.assert_called_once_with(mock_session, ANY)


def test_crear_equipos_generacion_invalida(mock_session, mock_db):
    equipo_crear = {
        "nombre": "los testeadores 4 el test fantasma",
        "id_generacion": 98,
    }
    mock_db.create_equipo.side_effect = HTTPException(
        status_code=400, detail="La generación con id 98 no existe"
    )

    response = client.post("/api/equipos", json=equipo_crear)

    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "La generación con id 98 no existe"
    mock_db.create_equipo.assert_called_once_with(mock_session, ANY)


def test_obtener_equipo_id_valido(mock_session, mock_db):
    equipo_creado = MOCK_EQUIPO_CREAR2

    mock_db.get_equipo.return_value = equipo_creado

    response = client.get("/api/equipos/1")
    content = response.json()
    assert response.status_code == 200
    assert content["nombre"] == "los testeadores 4 el test fantasma"
    assert content["generacion"]["id"] == 8
    assert content["integrantes"] == []
    mock_db.get_equipo.assert_called_once_with(mock_session, ANY)


def test_obtener_equipo_id_invalido(mock_session, mock_db):
    equipo_creado = MOCK_EQUIPO_CREAR2

    mock_db.get_equipo.return_value = equipo_creado
    mock_db.get_equipo.side_effect = HTTPException(
        status_code=404, detail="Equipo no encontrado"
    )
    response = client.get("/api/equipos/99")

    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Equipo no encontrado"
    mock_db.get_equipo.assert_called_once_with(mock_session, ANY)


def test_eliminar_equipo_id_valido(mock_session, mock_db):
    equipo_creado = MOCK_EQUIPO_CREAR2

    mock_db.delete_equipo.return_value = equipo_creado

    response = client.delete("/api/equipos/1")

    content = response.json()
    assert response.status_code == 200
    assert content["nombre"] == "los testeadores 4 el test fantasma"
    assert content["generacion"]["id"] == 8
    assert content["integrantes"] == []
    mock_db.delete_equipo.assert_called_once_with(mock_session, ANY)


def test_eliminar_equipo_id_invalido(mock_session, mock_db):
    equipo_creado = MOCK_EQUIPO_CREAR2

    mock_db.delete_equipo.return_value = equipo_creado
    mock_db.delete_equipo.side_effect = HTTPException(
        status_code=404, detail="Equipo no encontrado"
    )
    response = client.delete("/api/equipos/99")

    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Equipo no encontrado"
    mock_db.delete_equipo.assert_called_once_with(mock_session, ANY)


def test_agregar_integrante_valido(mock_session, mock_db):
    equipo_creado = MOCK_EQUIPO_CREAR2
    integrante_crear = {"id_pokemon": 30, "apodo": "perrito"}

    integrante_creado = Integrante(
        id=1,
        apodo="perrito",
        pokemon=PokemonIntegrante(
            id=30,
            nombre="nidorino",
            imagen="una imagen",
            estadisticas=Estadisticas(
                ataque=50,
                defensa=60,
                ataque_especial=90,
                defensa_especial=75,
                velocidad=50,
                puntos_de_golpe=100,
            ),
            generaciones=[],
            tipos=[],
        ),
        movimientos=[],
    )

    mock_db.create_equipo.return_value = equipo_creado
    mock_db.add_integrante.return_value = integrante_creado
    response = client.post("/api/equipos/1/integrantes", json=integrante_crear)

    assert response.status_code == 200
    content = response.json()
    assert content["id"] == 1
    assert content["pokemon"]["id"] == 30
    assert content["pokemon"]["nombre"] == "nidorino"
    assert content["movimientos"] == []
    mock_db.add_integrante.assert_called_once_with(mock_session, 1, ANY)


def test_agregar_integrante_equipo_no_encontrado(mock_session, mock_db):
    integrante_crear = {"id_pokemon": 30, "apodo": "perrito"}

    mock_db.add_integrante.side_effect = HTTPException(
        status_code=404, detail="Equipo de id 2 no encontrado"
    )

    response = client.post("/api/equipos/2/integrantes", json=integrante_crear)
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Equipo de id 2 no encontrado"
    mock_db.add_integrante.assert_called_once_with(mock_session, 2, ANY)


def test_agregar_integrante_id_pokemon_no_encontrado(mock_session, mock_db):
    integrante_crear = {"id_pokemon": 1000, "apodo": "perrote"}

    mock_db.add_integrante.side_effect = HTTPException(
        status_code=404, detail="Pokemon de id 1000 no encontrado"
    )

    response = client.post("/api/equipos/1/integrantes", json=integrante_crear)
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Pokemon de id 1000 no encontrado"
    mock_db.add_integrante.assert_called_once_with(mock_session, 1, ANY)


def test_agregar_integrante_generacion_del_integrante_no_valida(mock_session, mock_db):
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
    mock_db.add_integrante.assert_called_once_with(mock_session, 1, ANY)


def test_agregar_integrante_con_equipo_lleno(mock_session, mock_db):
    integrante_crear = {"id_pokemon": 30, "apodo": "perrito"}

    mock_db.add_integrante.side_effect = HTTPException(
        status_code=400,
        detail="Se alcanzo la maxima cantidad de integrantes: 6",
    )

    response = client.post("/api/equipos/1/integrantes", json=integrante_crear)
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Se alcanzo la maxima cantidad de integrantes: 6"
    mock_db.add_integrante.assert_called_once_with(mock_session, 1, ANY)


def test_actuaizar_equipo_caso_valido(mock_session, mock_db):
    equipo_actualizar = {
        "nombre": "los testeadors 5 el test contraataca",
        "id_generacion": 8,
    }
    equipo_creado = MOCK_EQUIPO_CREAR1
    equipo_actualizado = MOCK_EQUIPO_ACTUALIZAR
    mock_db.create_equipo.return_value = equipo_creado
    mock_db.update_equipo.return_value = equipo_actualizado

    response = client.put("/api/equipos/1", json=equipo_actualizar)
    assert response.status_code == 200
    content = response.json()
    assert content["nombre"] == "los testeadors 5 el test contraataca"
    assert content["generacion"]["id"] == 8
    mock_db.update_equipo.assert_called_once_with(mock_session, 1, ANY)


def test_actuaizar_equipo_generacion_invalida(mock_session, mock_db):
    equipo_actualizar = {
        "nombre": "los testeadors 5 el test contraataca",
        "id_generacion": 98,
    }
    equipo_creado = MOCK_EQUIPO_CREAR1
    equipo_actualizado = MOCK_EQUIPO_ACTUALIZAR
    mock_db.create_equipo.return_value = equipo_creado
    mock_db.update_equipo.return_value = equipo_actualizado
    mock_db.update_equipo.side_effect = HTTPException(
        status_code=404,
        detail="La generación con id 98 no existe",
    )

    response = client.put("/api/equipos/1", json=equipo_actualizar)
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "La generación con id 98 no existe"
    mock_db.update_equipo.assert_called_once_with(mock_session, 1, ANY)


def test_actuaizar_equipo_nombre_equipo_repetido(mock_session, mock_db):
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

    mock_db.create_equipo.side_effect = [equipo_creado, equipo_creado2]
    mock_db.update_equipo.side_effect = HTTPException(
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
    mock_db.update_equipo.assert_called_once_with(mock_session, 1, ANY)


def test_actuaizar_equipo_nombre_equipo_repetido(mock_session, mock_db):
    equipo_actualizar = {
        "nombre": "los testeadors 5 el test contraataca",
        "id_generacion": 2,
    }
    equipo_creado = MOCK_EQUIPO_CREAR1
    mock_db.create_equipo.return_value = equipo_creado
    mock_db.update_equipo.side_effect = HTTPException(
        status_code=400,
        detail="Un pokemon no es valido para la generacion 2",
    )

    response = client.put("/api/equipos/1", json=equipo_actualizar)
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Un pokemon no es valido para la generacion 2"
    mock_db.update_equipo.assert_called_once_with(mock_session, 1, ANY)


def test_eliminar_integrante_caso_valido(mock_session, mock_db):
    equipo_creado = MOCK_EQUIPO_CREAR1
    integrante_eliminado = MOCK_INTEGRANTE_ELIMINAR
    mock_db.create_equipo.return_value = equipo_creado
    mock_db.add_integrante.return_value = integrante_eliminado
    mock_db.delete_integrante.return_value = integrante_eliminado
    response = client.delete("/api/equipos/1/integrantes/1")
    assert response.status_code == 200
    content = response.json()
    assert content["apodo"] == "perrito"
    assert content["pokemon"]["nombre"] == "nidorina"
    assert content["movimientos"] == []
    mock_db.delete_integrante.assert_called_once_with(mock_session, 1, 1)


def test_eliminar_integrante_id_equipo_no_encontrado(mock_session, mock_db):
    equipo_creado = MOCK_EQUIPO_CREAR1
    integrante = MOCK_INTEGRANTE_ELIMINAR
    mock_db.create_equipo.return_value = equipo_creado
    mock_db.add_integrante.return_value = integrante
    mock_db.delete_integrante.side_effect = HTTPException(
        status_code=404,
        detail="El equipo de id 10 no fue encontrado",
    )
    response = client.delete("/api/equipos/10/integrantes/1")
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "El equipo de id 10 no fue encontrado"
    mock_db.delete_integrante.assert_called_once_with(mock_session, 10, 1)


def test_eliminar_integrante_id_integrante_no_encontrado(mock_session, mock_db):
    equipo_creado = MOCK_EQUIPO_CREAR1
    integrante = MOCK_INTEGRANTE_ELIMINAR
    mock_db.create_equipo.return_value = equipo_creado
    mock_db.add_integrante.return_value = integrante
    mock_db.delete_integrante.side_effect = HTTPException(
        status_code=404,
        detail="Integrante de id 2 no encontrado en este equipo",
    )
    response = client.delete("/api/equipos/1/integrantes/2")
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Integrante de id 2 no encontrado en este equipo"
    mock_db.delete_integrante.assert_called_once_with(mock_session, 1, 2)


def test_actualizar_integrante_caso_valido(mock_session, mock_db):
    integrante = MagicMock()
    integrante.id_integrante_dentro_del_grupo = 1
    integrante.id_pokemon = 30
    integrante.movimientos = []
    integrante_actualizado = {
        "apodo": "el champion",
        "movimientos": [228, 229],
    }
    equipo_creado = MagicMock()
    equipo_creado.integrantes = [integrante]
    movimiento1 = MagicMock(MOCK_MOV_228)
    movimiento2 = MagicMock(MOCK_MOV_229)

    movimiento_mostrar_1 = MOCK_MOV_MOSTRAR_228
    movimiento_mostrar_2 = MOCK_MOV_MOSTRAR_229

    pokemon_integrante = MagicMock()
    pokemon_integrante.id = 30
    pokemon_integrante.nombre = "nidorina"
    pokemon_integrante.imagen = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/30.png"
    pokemon_integrante.altura = 0.8
    pokemon_integrante.peso = 20
    mock_generacion1 = MagicMock()
    mock_generacion1.id_generacion = 1
    mock_generacion1.nombre_generacion = "Generación I"

    mock_generacion2 = MagicMock()
    mock_generacion2.id_generacion = 2
    mock_generacion2.nombre_generacion = "Generación II"

    pokemon_integrante.generaciones = [
        mock_generacion1,
        mock_generacion2,
    ]
    mock_tipo1 = MagicMock()
    mock_tipo1.id_tipo = 4
    mock_tipo1.nombre_tipo = "Veneno"

    mock_tipo2 = MagicMock()
    mock_tipo2.id_tipo = 1
    mock_tipo2.nombre_tipo = "Normal"

    pokemon_integrante.tipos = [
        mock_tipo1,
        mock_tipo2,
    ]

    mock_session.get.side_effect = [equipo_creado, pokemon_integrante]
    mock_db.get_movimiento_simple.side_effect = [movimiento1, movimiento2]
    mock_db.mostrar_por_metodo_de_mov.side_effect = [
        movimiento_mostrar_1,
        movimiento_mostrar_2,
    ]

    response = client.put("/api/equipos/1/integrantes/1", json=integrante_actualizado)
    assert response.status_code == 200
    content = response.json()
    assert content["apodo"] == "el champion"
    assert content["pokemon"]["nombre"] == "nidorina"
    assert len(content["movimientos"]) == 2
    assert content["movimientos"][0]["id"] == 228
    mock_session.get.assert_any_call(EquipoTabla, 1)
    mock_db.get_movimiento_simple.assert_any_call(mock_session, ANY)
    mock_db.mostrar_por_metodo_de_mov.assert_any_call(ANY)
    mock_session.commit.assert_called_once()


def test_actualizar_integrante_caso_excedido_max_movimientos(mock_session, mock_db):
    integrante = MagicMock()
    integrante.id_integrante_dentro_del_grupo = 1
    integrante.id_pokemon = 30
    integrante.movimientos = []

    integrante_actualizado = {
        "apodo": "el champion",
        "movimientos": [228, 229, 230, 231, 232],
    }
    equipo_creado = MagicMock()
    equipo_creado.integrantes = [integrante]

    mock_session.get.return_value = equipo_creado

    response = client.put("/api/equipos/1/integrantes/1", json=integrante_actualizado)
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Maximo 4 movimientos"
    mock_db.get_movimiento_simple.assert_not_called()


def test_actualizar_integrante_caso_movimiento_repetido(mock_session, mock_db):
    integrante = MagicMock()
    integrante.id_integrante_dentro_del_grupo = 1
    integrante.id_pokemon = 30
    integrante.movimientos = []

    integrante_actualizado = {
        "apodo": "el champion",
        "movimientos": [228, 228, 229, 230],
    }
    equipo_creado = MagicMock()
    equipo_creado.integrantes = [integrante]
    movimiento1 = MagicMock(MOCK_MOV_228)
    movimiento2 = MagicMock(MOCK_MOV_229)
    movimiento3 = MagicMock(MOCK_MOV_230)
    movimiento4 = movimiento1

    movimiento_mostrar_1 = MOCK_MOV_MOSTRAR_228
    movimiento_mostrar_2 = MOCK_MOV_MOSTRAR_229
    movimiento_mostrar_3 = MOCK_MOV_MOSTRAR_230
    movimiento_mostrar_4 = movimiento_mostrar_1

    mock_session.get.return_value = equipo_creado
    mock_db.get_movimiento_simple.side_effect = [
        movimiento4,
        movimiento1,
        movimiento2,
        movimiento3,
    ]
    mock_db.mostrar_por_metodo_de_mov.side_effect = [
        movimiento_mostrar_4,
        movimiento_mostrar_1,
        movimiento_mostrar_2,
        movimiento_mostrar_3,
    ]
    response = client.put("/api/equipos/1/integrantes/1", json=integrante_actualizado)
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Un movimiento esta repetido"
    mock_db.get_movimiento_simple.assert_any_call(mock_session, 228)
    mock_db.mostrar_por_metodo_de_mov.assert_called_once_with(ANY)


def test_actualizar_integrante_caso_movimiento_no_encontrado(mock_session, mock_db):
    integrante = MagicMock()
    integrante.id_integrante_dentro_del_grupo = 1
    integrante.id_pokemon = 30
    integrante.movimientos = []

    integrante_actualizado = {
        "apodo": "el champion",
        "movimientos": [9000, 228, 229, 230],
    }
    equipo_creado = MagicMock()
    equipo_creado.integrantes = [integrante]
    movimiento1 = MagicMock(MOCK_MOV_228)
    movimiento2 = MagicMock(MOCK_MOV_229)
    movimiento3 = MagicMock(MOCK_MOV_230)
    movimiento4 = None

    movimiento_mostrar_1 = MOCK_MOV_MOSTRAR_228
    movimiento_mostrar_2 = MOCK_MOV_MOSTRAR_229
    movimiento_mostrar_3 = MOCK_MOV_MOSTRAR_230
    movimiento_mostrar_4 = None

    mock_session.get.return_value = equipo_creado
    mock_db.get_movimiento_simple.side_effect = [
        movimiento4,
        movimiento1,
        movimiento2,
        movimiento3,
    ]
    mock_db.mostrar_por_metodo_de_mov.side_effect = [
        movimiento_mostrar_4,
        movimiento_mostrar_1,
        movimiento_mostrar_2,
        movimiento_mostrar_3,
    ]
    response = client.put("/api/equipos/1/integrantes/1", json=integrante_actualizado)
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Movimiento no encontrado"
    mock_db.get_movimiento_simple.assert_called_once_with(mock_session, 9000)
    mock_db.mostrar_por_metodo_de_mov.assert_not_called()


def test_agregar_movimiento_a_integrante_caso_valido(mock_session, mock_db):
    #    integrante = MagicMock()
    #    integrante.id_integrante_dentro_del_grupo = 1
    #    integrante.id_pokemon = 30
    #    integrante.movimientos = []
    #
    #    equipo_creado = MagicMock()
    #    equipo_creado.integrantes = [integrante]
    #
    #    movimiento1 = MagicMock(MOCK_MOV_228)
    #    movimiento1.generacion = MagicMock(
    #        id_generacion=2, nombre_generacion="Generación II"
    #    )
    #    movimiento1.tipo = MagicMock(id=1, nombre="Normal")
    #
    #    mock_session.get.return_value = equipo_creado
    #    mock_db.get_movimiento_simple.return_value = movimiento1
    #
    #    response = client.post(
    #        "/api/equipos/1/integrantes/1/movimientos", json={"id_movimiento": 228}
    #    )
    #    assert response.status_code == 200
    #    content = response.json()
    #    assert content["id"] == 228
    #    assert content["nombre"] == "Destructor"
    #    assert content["generacion"]["nombre"] == "Generación II"
    #    assert content["tipo"]["nombre"] == "Normal"
    #
    #    mock_session.commit.assert_called_once()
    #    mock_db.get_movimiento_simple.assert_called_once_with(mock_session, 228)
    pass


def test_agregar_movimiento_integrante_caso_movimiento_inexistente(
    mock_session, mock_db
):
    integrante = MagicMock()
    integrante.id_integrante_dentro_del_grupo = 1
    integrante.id_pokemon = 30
    integrante.movimientos = []

    equipo_creado = MagicMock()
    equipo_creado.integrantes = [integrante]
    integrante.movimientos_del_integrante = []

    mock_session.get.return_value = equipo_creado
    mock_db.get_movimiento_simple.return_value = None

    response = client.post(
        "/api/equipos/1/integrantes/1/movimientos", json={"id_movimiento": 9999}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Movimiento no encontrado"
    mock_session.get.assert_called_once_with(EquipoTabla, 1)
    mock_db.get_movimiento_simple.assert_called_once_with(mock_session, 9999)
    mock_session.commit.assert_not_called()


def test_agregar_movimiento_integrante_caso_mas_de_cuatro_movimientos(
    mock_session, mock_db
):
    integrante = MagicMock()
    integrante.id_integrante_dentro_del_grupo = 1
    integrante.id_pokemon = 30
    integrante.movimientos = []

    equipo_creado = MagicMock()
    equipo_creado.integrantes = [integrante]
    integrante.movimientos_del_integrante = []

    movimiento_nuevo = MOCK_MOV_232
    movimiento_nuevo.generacion = MagicMock(
        id_generacion=2, nombre_generacion="Generación II"
    )
    movimiento_nuevo.tipo = MagicMock(id_tipo=2, nombre_tipo="A-normal")

    integrante.movimientos_del_integrante = [
        MOCK_MOV_228,
        MOCK_MOV_229,
        MOCK_MOV_230,
        MOCK_MOV_231,
    ]
    mock_session.get.return_value = equipo_creado
    mock_db.get_movimiento_simple.return_value = movimiento_nuevo

    response = client.post(
        "/api/equipos/1/integrantes/1/movimientos", json={"id_movimiento": 232}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Maximo 4 movimientos"
    mock_session.get.assert_called_once_with(EquipoTabla, 1)
    mock_db.get_movimiento_simple.assert_any_call(mock_session, 232)
    mock_session.commit.assert_not_called()


def test_agregar_movimiento_integrante_caso_movimiento_repetido(mock_session, mock_db):
    integrante = MagicMock()
    integrante.id_integrante_dentro_del_grupo = 1
    integrante.id_pokemon = 30
    integrante.movimientos = []

    equipo_creado = MagicMock()
    equipo_creado.integrantes = [integrante]
    integrante.movimientos_del_integrante = []

    movimiento_nuevo = MOCK_MOV_231
    movimiento_nuevo.generacion = MagicMock(
        id_generacion=1, nombre_generacion="Generación I"
    )
    movimiento_nuevo.tipo = MagicMock(id_tipo=1, nombre_tipo="Normal")

    integrante.movimientos_del_integrante = [
        MOCK_MOV_231,
    ]
    mock_session.get.return_value = equipo_creado
    mock_db.get_movimiento_simple.return_value = movimiento_nuevo

    response = client.post(
        "/api/equipos/1/integrantes/1/movimientos", json={"id_movimiento": 231}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Movimiento Repetido"
    mock_session.get.assert_called_once_with(EquipoTabla, 1)
    mock_db.get_movimiento_simple.assert_any_call(mock_session, 231)
    mock_session.commit.assert_not_called()
