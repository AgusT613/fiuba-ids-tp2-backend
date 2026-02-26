from unittest.mock import MagicMock
from fastapi.testclient import TestClient
import pytest
from sqlmodel import Session
from database.database import Database
from dependencias.dependencias import get_database
from dependencias.dependencias_de_la_db import get_session
from main import app
from modelos.modelos import Generacion


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
