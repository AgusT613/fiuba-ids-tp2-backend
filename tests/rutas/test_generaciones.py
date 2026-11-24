from modelos.modelos import Generacion
from tests.rutas.conftest import client


def test_generaciones(mock_session, mock_db):
    generaciones = [
        Generacion(id=1, nombre="Generación I"),
        Generacion(id=2, nombre="Generación II"),
        Generacion(id=3, nombre="Generación III"),
        Generacion(id=4, nombre="Generación IV"),
    ]
    mock_db.get_generaciones.return_value = generaciones
    response = client.get("/api/generaciones")
    assert response.status_code == 200
    content = response.json()
    assert content[0]["id"] == 1
    assert content[1]["id"] == 2
    assert content[2]["id"] == 3
    assert content[3]["id"] == 4
    mock_db.get_generaciones.assert_called_once_with(mock_session)
