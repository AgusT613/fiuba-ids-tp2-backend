from fastapi import FastAPI
from rutas.index import api_router
from dependencias.dependencias import inicializar_deps
from seed import seed


def main():
    inicializar_deps()
    seed()


app = FastAPI()
app.include_router(api_router)

main()


@app.get("/")
def root():
    return {"message": "Pokemon API"}
