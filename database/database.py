from sqlmodel import Session
from modelos.filtros import FiltrosMovimiento, FiltrosPokemon
from modelos.modelos import (
    Equipo,
    EquipoListado,
    EquipoUpsert,
    EquipooUpsert,
    Evoluciones,
    Generacion,
    Habilidades,
    Integrante,
    IntegranteUpsert,
    Movimiento,
    MovimientoDetallado,
    PokemonLista,
    Tipo,
)
from modelos.modelos_de_la_db import MovimientoTabla, PokemonTabla, TipoTabla
from repositorios.equipo_repositorio import EquipoRepositorio
from repositorios.generacion_repositorio import GeneracionRepositorio
from repositorios.movimiento_repositorio import MovimientoRepositorio
from repositorios.pokemon_repositorio import PokemonRepositorio


class Database:
    """Facade unificado de persistencia y consultas para la aplicación.
    
    Delega las operaciones en repositorios especializados por dominio:
    - PokemonRepositorio: Pokemones, habilidades, evoluciones, tipos.
    - MovimientoRepositorio: Movimientos y filtros asociados.
    - GeneracionRepositorio: Generaciones.
    - EquipoRepositorio: Equipos e integrantes.
    """

    def __init__(
        self,
        pokemon_repo: PokemonRepositorio | None = None,
        movimiento_repo: MovimientoRepositorio | None = None,
        generacion_repo: GeneracionRepositorio | None = None,
        equipo_repo: EquipoRepositorio | None = None,
    ):
        self.pokemon_repo = pokemon_repo or PokemonRepositorio()
        self.movimiento_repo = movimiento_repo or MovimientoRepositorio()
        self.generacion_repo = generacion_repo or GeneracionRepositorio()
        self.equipo_repo = equipo_repo or EquipoRepositorio()

    # --- Métodos de Pokémon ---

    def get_pokemon(self, session: Session, id: int) -> PokemonTabla:
        return self.pokemon_repo.get_pokemon(session, id)

    def get_habilidades(self, session: Session, id: int) -> list[Habilidades]:
        return self.pokemon_repo.get_habilidades(session, id)

    def get_evoluciones(self, session: Session, id: int) -> list[Evoluciones]:
        return self.pokemon_repo.get_evoluciones(session, id)

    def get_tipos_pokemon(self, session: Session, pokemon_id: int) -> list[TipoTabla]:
        return self.pokemon_repo.get_tipos_pokemon(session, pokemon_id)

    def get_pokemones(
        self, session: Session, filtros: FiltrosPokemon
    ) -> list[PokemonLista]:
        return self.pokemon_repo.get_pokemones(session, filtros)

    def get_movimientos_pokemon(self, session: Session, pokemon_id: int):
        return self.pokemon_repo.get_movimientos_pokemon(session, pokemon_id)

    # --- Métodos de Generaciones ---

    def get_generaciones(self, session: Session) -> list[Generacion]:
        return self.generacion_repo.get_generaciones(session)

    # --- Métodos de Movimientos ---

    def get_movimientos(
        self, session: Session, filtros: FiltrosMovimiento
    ) -> list[Movimiento]:
        return self.movimiento_repo.get_movimientos(session, filtros)

    def get_movimiento_simple(
        self, session: Session, movimiento_id: int
    ) -> MovimientoTabla:
        return self.movimiento_repo.get_movimiento_simple(session, movimiento_id)

    def get_movimiento(
        self, session: Session, movimiento_id: int
    ) -> MovimientoDetallado:
        return self.movimiento_repo.get_movimiento(session, movimiento_id)

    def mostrar_por_metodo_de_mov(self, mov: MovimientoTabla) -> Movimiento:
        return self.movimiento_repo.mostrar_por_metodo_de_mov(mov)

    # --- Métodos de Equipos e Integrantes ---

    def get_integrantes_equipo(
        self, session: Session, id_equipo: int
    ) -> list[Integrante]:
        return self.equipo_repo.get_integrantes_equipo(session, id_equipo)

    def get_equipo(self, session: Session, id: int) -> Equipo:
        return self.equipo_repo.get_equipo(session, id)

    def get_equipos(self, session: Session) -> list[EquipoListado]:
        return self.equipo_repo.get_equipos(session)

    def create_equipo(
        self, session: Session, equipo_a_crear: EquipooUpsert
    ) -> Equipo:
        return self.equipo_repo.create_equipo(session, equipo_a_crear)

    def delete_equipo(self, session: Session, id: int) -> Equipo:
        return self.equipo_repo.delete_equipo(session, id)

    def update_equipo(
        self, session: Session, id_equipo: int, datos_actualizados: EquipooUpsert
    ) -> Equipo:
        return self.equipo_repo.update_equipo(session, id_equipo, datos_actualizados)

    def add_integrante(
        self, session: Session, id_equipo: int, nuevo_integrante: IntegranteUpsert
    ) -> Integrante:
        return self.equipo_repo.add_integrante(session, id_equipo, nuevo_integrante)

    def delete_integrante(
        self, session: Session, id_equipo: int, integrante_id: int
    ) -> Integrante:
        return self.equipo_repo.delete_integrante(session, id_equipo, integrante_id)
