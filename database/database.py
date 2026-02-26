from fastapi import HTTPException
from modelos.modelos import (
    Estadisticas,
    Evoluciones,
    Generacion,
    Habilidades,
    Movimiento,
    Pokemon,
    Equipo,
    EquipooUpsert,
    Integrante,
    IntegranteUpsert,
    Tipo,
    MovimientoDetallado,
)
from utils.movimientos import filtrar_pokemones
from constantes.constantes import METODO_MOVIMIENTO


class Database:
    def __init__(self):
        self.pokemones: list[Pokemon] = []
        self.movimientos: list[Movimiento] = []
        self.generaciones: list[Generacion] = []
        self.habilidades_por_pokemon: dict[int, list[Habilidades]] = {}
        self.estadisticas_por_pokemon: dict[int, Estadisticas] = {}
        self.evoluciones_por_pokemon = {}
        self.pokemon_moves_csv: list = []
        self.equipos: list[Equipo] = []
        self.integrantes: list[Integrante] = []

    def get(self, id: int) -> Pokemon | None:
        for pokemon in self.pokemones:
            if pokemon.id == id:
                return pokemon
        return None

    def get_habilidades(self, id: int) -> list[Habilidades]:
        return self.habilidades_por_pokemon.get(id, [])

    def get_estadisticas(self, id: int) -> Estadisticas | None:
        return self.estadisticas_por_pokemon.get(id)

    def cargar_evoluciones(self, evoluciones_por_pokemon):
        self.evoluciones_por_pokemon = evoluciones_por_pokemon

    def get_evoluciones(self, id: int) -> list[Evoluciones]:
        return self.evoluciones_por_pokemon.get(id, [])

    def cargar_pokemones(self, pokemones: list[Pokemon]):
        self.pokemones = pokemones

    def cargar_habilidades(self, habilidades_por_pokemon: dict[int, list[Habilidades]]):
        self.habilidades_por_pokemon = habilidades_por_pokemon

    def cargar_estadisticas(self, estadisticas_de_pokemon: dict[int, Estadisticas]):
        self.estadisticas_por_pokemon = estadisticas_de_pokemon

    def cargar_pokemon_moves_csv(self, lista_movimientos_csv: list):
        self.pokemon_moves_csv = lista_movimientos_csv

    def cargar_movimientos(self, lista_movimientos: list[Movimiento]):
        self.movimientos = lista_movimientos

    def obtener_movimientos(self) -> list[Movimiento]:
        return self.movimientos

    def obtener_movimiento_simple(self, movimiento_id: int) -> Movimiento:
        for movimiento in self.movimientos:
            if movimiento.id == movimiento_id:
                return Movimiento(
                    id=movimiento.id,
                    nombre=movimiento.nombre,
                    generacion=movimiento.generacion,
                    tipo=movimiento.tipo,
                    categoria=movimiento.categoria,
                    potencia=movimiento.potencia,
                    precision=movimiento.precision,
                    puntos_de_poder=movimiento.puntos_de_poder,
                    efecto=movimiento.efecto,
                )

        raise HTTPException(status_code=404, detail="Movimiento no encontrado")

    def obtener_movimiento(self, movimiento_id: int) -> MovimientoDetallado:
        for movimiento in self.movimientos:
            if movimiento.id == movimiento_id:
                pokemon_por_huevo, pokemon_por_nivel, pokemon_por_maquina = (
                    filtrar_pokemones(
                        movimiento_id, self.pokemones, self.pokemon_moves_csv
                    )
                )

                return MovimientoDetallado(
                    id=movimiento.id,
                    nombre=movimiento.nombre,
                    generacion=movimiento.generacion,
                    tipo=movimiento.tipo,
                    categoria=movimiento.categoria,
                    potencia=movimiento.potencia,
                    precision=movimiento.precision,
                    puntos_de_poder=movimiento.puntos_de_poder,
                    efecto=movimiento.efecto,
                    pokemon_por_huevo=pokemon_por_huevo,
                    pokemon_por_nivel=pokemon_por_nivel,
                    pokemon_por_maquina=pokemon_por_maquina,
                )

    def cargar_generaciones(self, lista_generaciones: list[Generacion]):
        self.generaciones = lista_generaciones

    def obtener_generaciones(self) -> list[Generacion]:
        return self.generaciones

    def cargar_tipos(self, lista_tipos: list[Tipo]):
        self.tipos = lista_tipos

    def obtener_tipos(self) -> list[Tipo]:
        return self.tipos

    def obtener_pokemones(self) -> list[Pokemon]:
        return self.pokemones

    def obtener_tipos_por_id(self, pokemon_id: int):
        tipos = []
        for tipo in self.tipos:
            if tipo.pokemon_id == pokemon_id:
                tipos.append(tipo)
        return tipos

    def obtener_movimientos_pokemon(
        self, pokemon_id: int
    ) -> tuple[list[Movimiento], list[Movimiento], list[Movimiento]]:
        movimientos_nivel = []
        movimientos_huevo = []
        movimientos_maquina = []

        for move in self.pokemon_moves_csv:
            if move["linea_pokemon_id"] == pokemon_id:
                movimiento = self.obtener_movimiento_simple(move["linea_move_id"])
                if move["linea_move_method_id"] == METODO_MOVIMIENTO["huevo"]:
                    movimientos_huevo.append(movimiento)

                elif move["linea_move_method_id"] == METODO_MOVIMIENTO["maquina"]:
                    movimientos_maquina.append(movimiento)

                elif move["linea_move_method_id"] == METODO_MOVIMIENTO["nivel"]:
                    movimientos_nivel.append(movimiento)

        return movimientos_huevo, movimientos_maquina, movimientos_nivel

    def obtener_equipo(self, id: int) -> Equipo:
        for equipo in self.equipos:
            if equipo.id == id:
                return equipo
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    def cargar_equipos(self, equipos: list[Equipo]):
        self.equipos = equipos

    def listar_equipos(self) -> list[Equipo]:
        return self.equipos

    def add(self, equipo_a_crear: EquipooUpsert) -> Equipo:
        for equipo in self.equipos:
            if equipo.nombre == equipo_a_crear.nombre:
                raise HTTPException(
                    status_code=400,
                    detail=f"Ya existe un equipo con ese nombre: {equipo.nombre}",
                )

        generacion_encontrada = None
        generaciones_validas = self.generaciones
        for g in generaciones_validas:
            if g.id == equipo_a_crear.id_generacion:
                generacion_encontrada = g
                break
        if generacion_encontrada is None:
            raise HTTPException(
                status_code=404,
                detail=f"La generación con id {equipo_a_crear.id_generacion} no existe",
            )

        _id = len(self.equipos) + 1

        nuevo_equipo = Equipo(
            id=_id,
            nombre=equipo_a_crear.nombre,
            generacion=generacion_encontrada,
            integrantes=[],
        )
        self.equipos.append(nuevo_equipo)
        return nuevo_equipo

    def delete(self, id) -> Equipo:
        equipo = self.obtener_equipo(id)
        self.equipos.remove(equipo)
        try:
            self.integrantes.remove(equipo.integrantes)
        except:
            pass
        return equipo

    def add_integrante(
        self, id_equipo: int, nuevo_integrante: IntegranteUpsert
    ) -> Integrante:
        equipo = self.obtener_equipo(id_equipo)
        equipo_encontrado = None
        for eq in self.equipos:
            if id_equipo == eq.id:
                equipo_encontrado = equipo
        if equipo_encontrado is None:
            raise HTTPException(
                status_code=404, detail=f"Equipo de id {id_equipo} no encontrado"
            )

        pokemon_encontrado = None
        for pokemon in self.pokemones:
            if pokemon.id == nuevo_integrante.id_pokemon:
                pokemon_encontrado = pokemon
        if pokemon_encontrado is None:
            raise HTTPException(
                status_code=404,
                detail=f"Pokemon de id {nuevo_integrante.id_pokemon} no encontrado",
            )
        generacion_valida = False
        for generacion in pokemon_encontrado.generaciones:
            for i in range(equipo_encontrado.generacion.id + 1):
                if generacion["id"] == i:
                    generacion_valida = True
        if generacion_valida is False:
            raise HTTPException(
                status_code=400,
                detail="Generación del pokemon no pertenece a la generación del equipo",
            )

        integrante_id = len(equipo_encontrado.integrantes) + 1

        if integrante_id > 6:
            raise HTTPException(
                status_code=400,
                detail="Se alcanzó la cantidad máxima de integrantes: 6",
            )

        integrante = Integrante(
            id=integrante_id,
            apodo=nuevo_integrante.apodo,
            pokemon=pokemon_encontrado,
            movimientos=[],
        )

        self.integrantes.append(integrante)
        equipo_encontrado.integrantes.append(integrante)
        return integrante

    def update_equipos(
        self, id_equipo: int, datos_actualizados: EquipooUpsert
    ) -> Equipo:
        equipo = self.obtener_equipo(id_equipo)
        for equipo_existente in self.equipos:
            if (
                equipo_existente.id != id_equipo
                and equipo_existente.nombre == datos_actualizados.nombre
            ):
                raise HTTPException(
                    status_code=400,
                    detail=f"Ya existe un equipo con ese nombre: {equipo_existente.nombre}",
                )

        generaciones = self.generaciones
        nueva_generacion = None
        for g in generaciones:
            if g.id == datos_actualizados.id_generacion:
                nueva_generacion = g
                break

        if nueva_generacion is None:
            raise HTTPException(
                status_code=404,
                detail=f"La generación con id {datos_actualizados.id_generacion} no existe",
            )

        ids_generaciones_pokemon = []
        # generacion_valida = False
        if equipo.integrantes:
            for integrante in equipo.integrantes:
                generaciones_pokemon = integrante.pokemon.generaciones
                ids_generaciones_pokemon = [g["id"] for g in generaciones_pokemon]
                for i in range(1, nueva_generacion.id + 1):
                    if i not in ids_generaciones_pokemon:
                        #    generacion_valida = True
                        # else:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Un Pokémon no es válido para la generación {nueva_generacion.id}",
                        )

        equipo.nombre = datos_actualizados.nombre
        equipo.generacion = nueva_generacion

        return equipo

    def delete_integrante(self, id_equipo: int, integrante_id: int) -> Integrante:
        equipo = self.obtener_equipo(id_equipo)
        equipo_encontrado = None
        integrante_encontrado = None
        for eq in self.equipos:
            if id_equipo == eq.id:
                equipo_encontrado = equipo
        for integrante in equipo_encontrado.integrantes:
            if integrante_id == integrante.id:
                integrante_encontrado = integrante
        if equipo_encontrado is None:
            raise HTTPException(
                status_code=404, detail=f"Equipo de id {id_equipo} no encontrado"
            )
        if integrante_encontrado is None:
            raise HTTPException(
                status_code=404,
                detail=f"Integrante de id {integrante_id} no encontrado en este equipo",
            )
        self.integrantes.remove(integrante_encontrado)
        equipo_encontrado.integrantes.remove(integrante_encontrado)
        return integrante_encontrado
