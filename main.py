from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from dependencias.dependencias import inicializar_deps
from dependencias.dependencias_de_la_db import init_engine
from rutas.index import api_router
from seed import seed

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setea lo que se necesita antes de arrancar la aplicacion
    init_engine()
    inicializar_deps()

    try:
        from alembic import command
        from alembic.config import Config

        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)
        command.upgrade(alembic_cfg, "head")

        seed()
    except Exception as e:
        logger.warning("Aviso durante inicialización o migraciones de base de datos: %s", e)

    yield


app = FastAPI(title=settings.app_title, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "Pokemon API"}
