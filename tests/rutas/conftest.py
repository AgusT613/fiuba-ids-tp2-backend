from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from database.database import Database
from dependencias.dependencias import get_database
from dependencias.dependencias_de_la_db import get_session
from main import app

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
