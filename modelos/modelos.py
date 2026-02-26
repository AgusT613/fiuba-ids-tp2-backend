from pydantic import BaseModel


class Generacion(BaseModel):
    id: int
    nombre: str


class Debilidad(BaseModel):
    id: int
    nombre: str


class Tipo(BaseModel):
    id: int
    nombre: str
    debilidades: list[Debilidad] = []


class TipoMovimiento(BaseModel):
    id: int
    nombre: str


class Evoluciones(BaseModel):
    id: int
    imagen: str
    nombre: str


class Habilidades(BaseModel):
    id: int
    nombre: str


class Estadisticas(BaseModel):
    ataque: int
    defensa: int
    ataque_especial: int
    defensa_especial: int
    puntos_de_golpe: int
    velocidad: int


class PokemonLista(BaseModel):
    id: int
    nombre: str
    imagen: str
    generaciones: list[Generacion]
    tipos: list[TipoMovimiento]


class PokemonIntegrante(BaseModel):
    id: int
    nombre: str
    imagen: str
    estadisticas: Estadisticas
    generaciones: list[Generacion]
    tipos: list[Tipo]


class Pokemon(BaseModel):
    id: int
    nombre: str
    imagen: str
    altura: float
    peso: float
    generaciones: list = []
    tipos: list = []


class PokemonMovimiento(BaseModel):
    id: int
    nombre: str
    imagen: str
    altura: float
    peso: float


class Movimiento(BaseModel):
    id: int
    nombre: str
    generacion: Generacion
    tipo: TipoMovimiento
    categoria: str
    potencia: int
    precision: int
    puntos_de_poder: int
    efecto: str


class PokemonPorId(BaseModel):
    id: int
    nombre: str
    imagen: str
    altura: float
    peso: float
    generaciones: list[Generacion] = []
    tipos: list[Tipo] = []
    habilidades: list = []
    estadisticas: Estadisticas
    evoluciones: list = []
    movimientos_huevo: list[Movimiento] = []
    movimientos_maquina: list[Movimiento] = []
    movimientos_nivel: list[Movimiento] = []


class MovimientoDetallado(Movimiento):
    pokemon_por_huevo: list[PokemonMovimiento] = []
    pokemon_por_nivel: list[PokemonMovimiento] = []
    pokemon_por_maquina: list[PokemonMovimiento] = []


class Integrante(BaseModel):
    id: int
    apodo: str
    pokemon: PokemonIntegrante
    movimientos: list[Movimiento] = []


class EquipoBase(BaseModel):
    id: int
    nombre: str
    generacion: Generacion


class Equipo(EquipoBase):
    integrantes: list[Integrante] = []


class EquipooUpsert(BaseModel):
    nombre: str
    id_generacion: int


class IntegranteUpsert(BaseModel):
    id_pokemon: int
    apodo: str


class IntegranteDeEquipoUpsert(BaseModel):
    apodo: str
    movimientos: list[int]


class MovimientoAIntegrante(BaseModel):
    id_movimiento: int


class EquipoListado(EquipoBase):
    cantidad_integrantes: int
