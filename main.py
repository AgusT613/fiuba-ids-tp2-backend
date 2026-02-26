from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dependencias.dependencias_de_la_db import init_engine
from rutas.index import api_router
from dependencias.dependencias import inicializar_deps
from seed import seed
from contextlib import asynccontextmanager
import subprocess
import os
from constantes.constantes import SQLITE_FILE_PATH


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setea lo que se necesita antes de arrancar la aplicacion
    init_engine()
    inicializar_deps()

    if not os.path.exists(SQLITE_FILE_PATH):
        print("Realizando migraciones...")
        subprocess.run(["alembic", "upgrade", "head"])
        print(f"Migraciones realizadas!")
        print("Realizando seed de datos...")
        seed()
        print("Seed de datos realizado!")

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "Pokemon API"}
