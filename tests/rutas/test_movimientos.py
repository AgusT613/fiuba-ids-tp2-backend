from modelos.filtros import FiltrosMovimiento
from modelos.modelos import MovimientoDetallado, PokemonMovimiento
from tests.constantes.constantes import (
    MOCK_LISTA_MOVIMIENTOS,
    MOCK_LISTA_POKEMONES_DE_MOVIMIENTO,
)
from tests.rutas.conftest import client


def test_listar_movimientos(mock_session, mock_db):
    movimientos = MOCK_LISTA_MOVIMIENTOS
    mock_db.get_movimientos.return_value = movimientos
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
    mock_db.get_movimientos.assert_called_once_with(mock_session, FiltrosMovimiento())


def test_movimiento_id_existente_completo(mock_session, mock_db):
    mock_db.get_movimiento.return_value = MovimientoDetallado(
        id=3,
        nombre="Doble Bofetón",
        generacion={"id": 1, "nombre": "Generación I"},
        tipo={"id": 1, "nombre": "Normal"},
        categoria="físico",
        potencia=15,
        precision=85,
        puntos_de_poder=10,
        efecto="Hits 2-5 times in one turn.",
        pokemon_por_huevo=MOCK_LISTA_POKEMONES_DE_MOVIMIENTO,
        pokemon_por_maquina=[],
        pokemon_por_nivel=[
            PokemonMovimiento(
                id=5,
                nombre="charmeleon",
                imagen="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/5.png",
                altura=50.0,
                peso=10.0,
            )
        ],
    )

    response = client.get("/api/movimientos/3")

    assert response.status_code == 200
    content = response.json()

    assert content["id"] == 3
    assert content["tipo"]["id"] == 1
    assert content["generacion"]["nombre"] == "Generación I"
    assert content["tipo"]["id"] == 1
    assert len(content["pokemon_por_huevo"]) == 4
    assert len(content["pokemon_por_maquina"]) == 0
    assert len(content["pokemon_por_nivel"]) == 1

    mock_db.get_movimiento.assert_called_once_with(mock_session, 3)
