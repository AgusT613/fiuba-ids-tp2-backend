import os
from dataclasses import dataclass, field
from constantes.constantes import SQLITE_FILE_PATH


@dataclass
class Settings:
    """Configuración centralizada de la aplicación."""

    app_title: str = "Pokemon API"
    sqlite_file_path: str = os.getenv("SQLITE_FILE_PATH", SQLITE_FILE_PATH)
    database_url: str = f"sqlite:///{os.getenv('SQLITE_FILE_PATH', SQLITE_FILE_PATH)}"
    cors_origins: list[str] = field(
        default_factory=lambda: os.getenv(
            "CORS_ORIGINS", "http://localhost:5173"
        ).split(",")
    )


settings = Settings()
