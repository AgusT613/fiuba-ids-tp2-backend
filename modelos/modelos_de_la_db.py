from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class PokemonGeneracionTabla(SQLModel, table=True):
    __tablename__ = "relacion_pokemon_generacion"
    id_pokemon: int = Field(foreign_key="pokemones.id_pokemon", primary_key=True)
    id_generacion: int = Field(
        foreign_key="generaciones.id_generacion", primary_key=True
    )


class PokemonTipoTabla(SQLModel, table=True):
    __tablename__ = "relacion_pokemon_tipo"
    id_pokemon: int = Field(foreign_key="pokemones.id_pokemon", primary_key=True)
    id_tipo: int = Field(foreign_key="tipos.id_tipo", primary_key=True)


class PokemonHabilidadTabla(SQLModel, table=True):
    __tablename__ = "relacion_pokemon_habilidad"
    id_pokemon: int = Field(foreign_key="pokemones.id_pokemon", primary_key=True)
    id_habilidad: int = Field(foreign_key="habilidades.id_habilidad", primary_key=True)


class PokemonMovimientoAprendizajeTabla(SQLModel, table=True):
    __tablename__ = "pokemones_que_pueden_aprender_un_movimiento"
    id_pokemon: int = Field(foreign_key="pokemones.id_pokemon", primary_key=True)
    id_movimiento: int = Field(
        foreign_key="movimientos.id_movimiento", primary_key=True
    )
    metodo_de_aprendizaje: int


class TipoDebilidadTabla(SQLModel, table=True):
    __tablename__ = "debilidades_del_tipo"
    fk_id_tipo: int = Field(foreign_key="tipos.id_tipo", primary_key=True)
    fk_id_debilidad: int = Field(
        foreign_key="debilidades.id_debilidad", primary_key=True
    )


class IntegranteMovimientoTabla(SQLModel, table=True):
    __tablename__ = "relacion_integrante_movimiento"
    id_integrante: int = Field(foreign_key="integrante.id_integrante", primary_key=True)
    id_movimiento: int = Field(foreign_key="movimientos.id_movimiento")


class GeneracionTabla(SQLModel, table=True):
    __tablename__ = "generaciones"
    id_generacion: int = Field(primary_key=True)
    nombre_generacion: str

    pokemones_de_esa_generacion: list["PokemonTabla"] = Relationship(
        back_populates="generaciones", link_model=PokemonGeneracionTabla
    )
    movimientos: list["MovimientoTabla"] = Relationship(back_populates="generacion")
    equipos: list["EquipoTabla"] = Relationship(back_populates="generacion")


class TipoTabla(SQLModel, table=True):
    __tablename__ = "tipos"
    id_tipo: int = Field(primary_key=True)
    nombre_tipo: str
    debilidades: list["DebilidadTabla"] = Relationship(
        back_populates="tipos_con_esa_debilidad", link_model=TipoDebilidadTabla
    )
    pokemones_de_ese_tipo: list["PokemonTabla"] = Relationship(
        back_populates="tipos", link_model=PokemonTipoTabla
    )
    movimientos: list["MovimientoTabla"] = Relationship(back_populates="tipo")


class DebilidadTabla(SQLModel, table=True):
    __tablename__ = "debilidades"
    id_debilidad: int = Field(primary_key=True)
    nombre: str
    tipos_con_esa_debilidad: list["TipoTabla"] = Relationship(
        back_populates="debilidades", link_model=TipoDebilidadTabla
    )


class HabilidadesTabla(SQLModel, table=True):
    __tablename__ = "habilidades"
    id_habilidad: int = Field(primary_key=True)
    nombre_habilidad: str
    pokemones_con_esa_habilidad: list["PokemonTabla"] = Relationship(
        back_populates="habilidades", link_model=PokemonHabilidadTabla
    )


class EvolucionTabla(SQLModel, table=True):
    __tablename__ = "evoluciones"
    fk_id_pokemon: int = Field(foreign_key="pokemones.id_pokemon", primary_key=True)
    id_evolucion: int = Field(primary_key=True)
    nombre_evolucion: str
    imagen: str
    pokemon_base: Optional["PokemonTabla"] = Relationship(back_populates="evoluciones")


class MovimientoTabla(SQLModel, table=True):
    __tablename__ = "movimientos"
    id_movimiento: int = Field(primary_key=True)
    nombre: str
    id_generacion_del_movimiento: int = Field(foreign_key="generaciones.id_generacion")
    id_tipo_del_movimiento: int = Field(foreign_key="tipos.id_tipo")
    clase_de_daño: str
    poder: int
    precision: int
    PP: int
    efecto: str
    generacion: "GeneracionTabla" = Relationship(back_populates="movimientos")
    tipo: "TipoTabla" = Relationship(back_populates="movimientos")
    pokemones: list["PokemonTabla"] = Relationship(
        back_populates="movimientos", link_model=PokemonMovimientoAprendizajeTabla
    )
    integrantes_que_tienen_ese_mov: list["IntegranteTabla"] = Relationship(
        back_populates="movimientos_del_integrante",
        link_model=IntegranteMovimientoTabla,
    )


class PokemonTabla(SQLModel, table=True):
    __tablename__ = "pokemones"
    id_pokemon: int = Field(primary_key=True)
    nombre: str
    imagen: str
    altura: float
    peso: float
    generaciones: list[GeneracionTabla] = Relationship(
        back_populates="pokemones_de_esa_generacion", link_model=PokemonGeneracionTabla
    )
    tipos: list[TipoTabla] = Relationship(
        back_populates="pokemones_de_ese_tipo", link_model=PokemonTipoTabla
    )
    habilidades: list[HabilidadesTabla] = Relationship(
        back_populates="pokemones_con_esa_habilidad", link_model=PokemonHabilidadTabla
    )
    evoluciones: list["EvolucionTabla"] = Relationship(back_populates="pokemon_base")
    ataque: int
    defensa: int
    ataque_especial: int
    defensa_especial: int
    puntos_de_golpe: int
    velocidad: int
    movimientos: list["MovimientoTabla"] = Relationship(
        back_populates="pokemones", link_model=PokemonMovimientoAprendizajeTabla
    )
    integrantes: list["IntegranteTabla"] = Relationship(back_populates="pokemon")


class EquipoTabla(SQLModel, table=True):
    __tablename__ = "equipos"
    id_equipo: int = Field(primary_key=True)
    nombre_equipo: str
    id_generacion_del_equipo: int = Field(foreign_key="generaciones.id_generacion")

    integrantes: Optional[list["IntegranteTabla"]] = Relationship(
        back_populates="equipo"
    )
    generacion: GeneracionTabla = Relationship(back_populates="equipos")


class IntegranteTabla(SQLModel, table=True):
    __tablename__ = "integrante"
    id_integrante: int = Field(primary_key=True)
    id_integrante_dentro_del_grupo: int
    apodo: str
    id_pokemon: int = Field(foreign_key="pokemones.id_pokemon")
    id_equipo: int = Field(foreign_key="equipos.id_equipo")
    equipo: EquipoTabla = Relationship(back_populates="integrantes")
    pokemon: PokemonTabla = Relationship(back_populates="integrantes")
    movimientos_del_integrante: list["MovimientoTabla"] = Relationship(
        back_populates="integrantes_que_tienen_ese_mov",
        link_model=IntegranteMovimientoTabla,
    )


class SeedDb(SQLModel, table=True):
    __tablename__ = "seed_db"
    id: int = Field(primary_key=True)
    hecho: int = Field(unique=True, default=0)
