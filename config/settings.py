import os
from dataclasses import dataclass, field
from constantes.constantes import SQLITE_FILE_PATH


def _get_default_database_url() -> str:
    # Si DATABASE_URL está definida explícitamente, usarla
    env_db_url = os.getenv("DATABASE_URL")
    if env_db_url:
        # Normalizar prefijo postgres:// y postgresql:// a postgresql+psycopg2://
        if env_db_url.startswith("postgres://"):
            return env_db_url.replace("postgres://", "postgresql+psycopg2://", 1)
        if env_db_url.startswith("postgresql://") and not env_db_url.startswith("postgresql+"):
            return env_db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        return env_db_url

    # Si se especifican variables de PostgreSQL
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB", "pokemon_db")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"


@dataclass
class Settings:
    """Configuración centralizada de la aplicación."""

    app_title: str = "Pokemon API"
    sqlite_file_path: str = os.getenv("SQLITE_FILE_PATH", SQLITE_FILE_PATH)
    database_url: str = field(default_factory=_get_default_database_url)
    cors_origins: list[str] = field(
        default_factory=lambda: os.getenv("CORS_ORIGINS").split(",")
    )


settings = Settings()
