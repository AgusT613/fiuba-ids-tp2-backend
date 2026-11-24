from contextlib import asynccontextmanager
import os
import subprocess
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from dependencias.dependencias import inicializar_deps
from dependencias.dependencias_de_la_db import init_engine
from rutas.index import api_router
from seed import seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setea lo que se necesita antes de arrancar la aplicacion
    init_engine()
    inicializar_deps()

    if not os.path.exists(settings.sqlite_file_path):
        print("Realizando migraciones...")
        subprocess.run(["alembic", "upgrade", "head"])
        print("Migraciones realizadas!")
        print("Realizando seed de datos...")
        seed()
        print("Seed de datos realizado!")

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
