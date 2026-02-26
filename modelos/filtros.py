from pydantic import BaseModel
from sqlmodel import Field


class BaseFiltro(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    nombre_parcial: str | None = None
    tipo: int | None = None


class FiltrosPokemon(BaseFiltro):
    pass


class FiltrosMovimiento(BaseFiltro):
    pass
