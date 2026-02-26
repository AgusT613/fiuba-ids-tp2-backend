from fastapi import APIRouter
from rutas import movimientos, generaciones, pokemones, equipos

api_router = APIRouter()
api_router.include_router(pokemones.router, prefix="/api/pokemon")
api_router.include_router(generaciones.router, prefix="/api/generaciones")
api_router.include_router(movimientos.router, prefix="/api/movimientos")
api_router.include_router(equipos.router, prefix="/api/equipos")
