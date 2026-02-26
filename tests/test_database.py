from modelos.modelos_de_la_db import (
    PokemonTabla,
    GeneracionTabla,
    MovimientoTabla,
    HabilidadesTabla,
    PokemonTipoTabla,
    PokemonHabilidadTabla,
    PokemonMovimientoAprendizajeTabla,
    PokemonGeneracionTabla,
    DebilidadTabla,
    EvolucionTabla,
    TipoTabla,
    EquipoTabla,
    IntegranteTabla,
)
from sqlmodel import select


def test_insertar_y_obtener_todas_las_generaciones(session):
    generaciones = [
        GeneracionTabla(id_generacion=1, nombre_generacion="Generacion I"),
        GeneracionTabla(id_generacion=2, nombre_generacion="Generacion II"),
        GeneracionTabla(id_generacion=3, nombre_generacion="Generacion III"),
        GeneracionTabla(id_generacion=4, nombre_generacion="Generacion IV"),
        GeneracionTabla(id_generacion=5, nombre_generacion="Generacion V"),
        GeneracionTabla(id_generacion=6, nombre_generacion="Generacion VI"),
        GeneracionTabla(id_generacion=7, nombre_generacion="Generacion VII"),
    ]
    session.add_all(generaciones)
    session.commit()
    results = session.exec(select(GeneracionTabla)).all()
    assert len(results) == 7
    nombres = [g.nombre_generacion for g in results]
    for i in range(1, 8):
        assert f"Generacion {['I','II','III','IV','V','VI','VII'][i-1]}" in nombres


def test_insertar_y_obtener_tipo(session):
    tipo = TipoTabla(id_tipo=1, nombre_tipo="Fuego")
    session.add(tipo)
    session.commit()
    result = session.get(TipoTabla, 1)
    assert result is not None
    assert result.nombre_tipo == "Fuego"


def test_insertar_y_obtener_debilidad(session):
    deb = DebilidadTabla(id_debilidad=1, nombre="Agua")
    session.add(deb)
    session.commit()
    result = session.get(DebilidadTabla, 1)
    assert result is not None
    assert result.nombre == "Agua"


def test_insertar_y_obtener_habilidad(session):
    hab = HabilidadesTabla(id_habilidad=1, nombre_habilidad="Electricidad")
    session.add(hab)
    session.commit()
    result = session.get(HabilidadesTabla, 1)
    assert result is not None
    assert result.nombre_habilidad == "Electricidad"


def test_insertar_y_obtener_pokemon(session):
    gen = GeneracionTabla(id_generacion=1, nombre_generacion="Gen I")
    tipo = TipoTabla(id_tipo=1, nombre_tipo="Eléctrico")
    hab = HabilidadesTabla(id_habilidad=1, nombre_habilidad="Electricidad")
    session.add_all([gen, tipo, hab])
    session.commit()
    poke = PokemonTabla(
        id_pokemon=1,
        nombre="Pikachu",
        imagen="img",
        altura=4,
        peso=60,
        ataque=55,
        defensa=40,
        ataque_especial=50,
        defensa_especial=50,
        puntos_de_golpe=35,
        velocidad=90,
    )
    session.add(poke)
    session.commit()
    # Relaciones
    session.add(PokemonGeneracionTabla(id_pokemon=1, id_generacion=1))
    session.add(PokemonTipoTabla(id_pokemon=1, id_tipo=1))
    session.add(PokemonHabilidadTabla(id_pokemon=1, id_habilidad=1))
    session.commit()
    result = session.get(PokemonTabla, 1)
    assert result is not None
    assert result.nombre == "Pikachu"


def test_insertar_y_obtener_movimiento(session):
    gen = GeneracionTabla(id_generacion=1, nombre_generacion="Gen I")
    tipo = TipoTabla(id_tipo=1, nombre_tipo="Eléctrico")
    session.add_all([gen, tipo])
    session.commit()
    mov = MovimientoTabla(
        id_movimiento=1,
        nombre="Impactrueno",
        id_generacion_del_movimiento=1,
        id_tipo_del_movimiento=1,
        clase_de_daño="especial",
        poder=40,
        precision=100,
        PP=30,
        efecto="Paraliza a veces",
    )
    session.add(mov)
    session.commit()
    result = session.get(MovimientoTabla, 1)
    assert result is not None
    assert result.nombre == "Impactrueno"


def test_insertar_y_obtener_evolucion(session):
    gen = GeneracionTabla(id_generacion=1, nombre_generacion="Gen I")
    session.add(gen)
    session.commit()
    poke = PokemonTabla(
        id_pokemon=1,
        nombre="Pikachu",
        imagen="img",
        altura=4,
        peso=60,
        ataque=55,
        defensa=40,
        ataque_especial=50,
        defensa_especial=50,
        puntos_de_golpe=35,
        velocidad=90,
    )
    session.add(poke)
    session.commit()
    evo = EvolucionTabla(
        fk_id_pokemon=1, id_evolucion=1, nombre_evolucion="Raichu", imagen="img"
    )
    session.add(evo)
    session.commit()
    result = session.get(EvolucionTabla, (1, 1))
    assert result is not None
    assert result.nombre_evolucion == "Raichu"


def test_insertar_y_obtener_equipo_e_integrante(session):
    gen = GeneracionTabla(id_generacion=1, nombre_generacion="Gen I")
    poke = PokemonTabla(
        id_pokemon=1,
        nombre="Pikachu",
        imagen="img",
        altura=4,
        peso=60,
        ataque=55,
        defensa=40,
        ataque_especial=50,
        defensa_especial=50,
        puntos_de_golpe=35,
        velocidad=90,
    )
    equipo = EquipoTabla(
        id_equipo=1, nombre_equipo="Equipo1", id_generacion_del_equipo=1
    )
    session.add_all([gen, poke, equipo])
    session.commit()
    integrante = IntegranteTabla(
        id_integrante_dentro_del_grupo=1, apodo="Pika", id_pokemon=1, id_equipo=1
    )
    session.add(integrante)
    session.commit()
    result = session.get(IntegranteTabla, 1)
    assert result is not None
    assert result.apodo == "Pika"


def test_db_get_pokemon(db, session):
    gen = GeneracionTabla(id_generacion=1, nombre_generacion="Gen I")
    tipo = TipoTabla(id_tipo=1, nombre_tipo="Eléctrico")
    session.add_all([gen, tipo])
    session.commit()
    poke = PokemonTabla(
        id_pokemon=1,
        nombre="Pikachu",
        imagen="img",
        altura=4,
        peso=60,
        ataque=55,
        defensa=40,
        ataque_especial=50,
        defensa_especial=50,
        puntos_de_golpe=35,
        velocidad=90,
    )
    session.add(poke)
    session.commit()
    session.add(PokemonGeneracionTabla(id_pokemon=1, id_generacion=1))
    session.add(PokemonTipoTabla(id_pokemon=1, id_tipo=1))
    session.commit()
    result = db.get_pokemon(session, 1)
    assert result is not None
    assert result[0].id_pokemon == 1
    assert result[0].nombre == "Pikachu"


def test_db_get_habilidades(db, session):
    hab = HabilidadesTabla(id_habilidad=1, nombre_habilidad="Electricidad")
    poke = PokemonTabla(
        id_pokemon=1,
        nombre="Pikachu",
        imagen="img",
        altura=4,
        peso=60,
        ataque=55,
        defensa=40,
        ataque_especial=50,
        defensa_especial=50,
        puntos_de_golpe=35,
        velocidad=90,
    )
    session.add_all([hab, poke])
    session.commit()
    session.add(PokemonHabilidadTabla(id_pokemon=1, id_habilidad=1))
    session.commit()
    habilidades = db.get_habilidades(session, 1)
    assert len(habilidades) == 1
    assert habilidades[0].nombre == "Electricidad"


def test_db_get_evoluciones(db, session):
    poke = PokemonTabla(
        id_pokemon=1,
        nombre="Pikachu",
        imagen="img",
        altura=4,
        peso=60,
        ataque=55,
        defensa=40,
        ataque_especial=50,
        defensa_especial=50,
        puntos_de_golpe=35,
        velocidad=90,
    )
    evo = EvolucionTabla(
        fk_id_pokemon=1, id_evolucion=1, nombre_evolucion="Raichu", imagen="img"
    )
    session.add_all([poke, evo])
    session.commit()
    evoluciones = db.get_evoluciones(session, 1)
    assert len(evoluciones) == 1
    assert evoluciones[0].nombre == "Raichu"


def test_db_obtener_generaciones(db, session):
    gen1 = GeneracionTabla(id_generacion=1, nombre_generacion="Gen I")
    gen2 = GeneracionTabla(id_generacion=2, nombre_generacion="Gen II")
    session.add_all([gen1, gen2])
    session.commit()
    generaciones = db.get_generaciones(session)
    assert any(g.nombre == "Gen I" for g in generaciones)
    assert any(g.nombre == "Gen II" for g in generaciones)


def test_db_obtener_movimientos(db, session):
    gen = GeneracionTabla(id_generacion=1, nombre_generacion="Gen I")
    tipo = TipoTabla(id_tipo=1, nombre_tipo="Eléctrico")
    mov = MovimientoTabla(
        id_movimiento=1,
        nombre="Impactrueno",
        id_generacion_del_movimiento=1,
        id_tipo_del_movimiento=1,
        clase_de_daño="especial",
        poder=40,
        precision=100,
        PP=30,
        efecto="Paraliza a veces",
    )
    session.add_all([gen, tipo, mov])
    session.commit()
    filtros = type(
        "Filtros", (), {"nombre_parcial": None, "tipo": None, "limit": 10, "offset": 0}
    )()
    movimientos = db.get_movimientos(session, filtros)
    assert any(m.nombre == "Impactrueno" for m in movimientos)


def test_insertar_multiples_tipos_y_relaciones(session):
    # Insertar tipos
    tipo1 = TipoTabla(id_tipo=1, nombre_tipo="Eléctrico")
    tipo2 = TipoTabla(id_tipo=2, nombre_tipo="Volador")
    session.add_all([tipo1, tipo2])
    session.commit()

    # Insertar Pokémon con dos tipos
    poke = PokemonTabla(
        id_pokemon=1,
        nombre="Pikachu",
        imagen="img",
        altura=4,
        peso=60,
        ataque=55,
        defensa=40,
        ataque_especial=50,
        defensa_especial=50,
        puntos_de_golpe=35,
        velocidad=90,
    )
    session.add(poke)
    session.commit()

    # Insertar relaciones de tipo
    session.add(PokemonTipoTabla(id_pokemon=1, id_tipo=1))
    session.add(PokemonTipoTabla(id_pokemon=1, id_tipo=2))
    session.commit()

    # Verificar que el Pokémon tiene ambos tipos
    tipos = session.exec(
        select(PokemonTipoTabla).where(PokemonTipoTabla.id_pokemon == 1)
    ).all()
    assert len(tipos) == 2

    # Verificar que los tipos son los correctos
    tipos_ids = [t.id_tipo for t in tipos]
    assert 1 in tipos_ids and 2 in tipos_ids


def test_filtrar_pokemon_por_tipo(session):
    # Insertar tipos
    tipo1 = TipoTabla(id_tipo=1, nombre_tipo="Eléctrico")
    tipo2 = TipoTabla(id_tipo=2, nombre_tipo="Fuego")
    session.add_all([tipo1, tipo2])
    session.commit()

    # Insertar Pokémon de diferentes tipos
    poke1 = PokemonTabla(
        id_pokemon=1,
        nombre="Pikachu",
        imagen="img",
        altura=4,
        peso=60,
        ataque=55,
        defensa=40,
        ataque_especial=50,
        defensa_especial=50,
        puntos_de_golpe=35,
        velocidad=90,
    )
    poke2 = PokemonTabla(
        id_pokemon=2,
        nombre="Charmander",
        imagen="img",
        altura=6,
        peso=85,
        ataque=52,
        defensa=43,
        ataque_especial=60,
        defensa_especial=50,
        puntos_de_golpe=39,
        velocidad=65,
    )
    session.add_all([poke1, poke2])
    session.commit()

    # Asignar tipos
    session.add(PokemonTipoTabla(id_pokemon=1, id_tipo=1))
    session.add(PokemonTipoTabla(id_pokemon=2, id_tipo=2))
    session.commit()

    # Filtrar Pokémon por tipo
    electric_pokemon = session.exec(
        select(PokemonTabla).join(PokemonTipoTabla).where(PokemonTipoTabla.id_tipo == 1)
    ).all()

    assert len(electric_pokemon) == 1
    assert electric_pokemon[0].nombre == "Pikachu"


def test_insertar_movimientos_maximos(session):
    # Insertar generación y tipo
    gen = GeneracionTabla(id_generacion=1, nombre_generacion="Gen I")
    tipo = TipoTabla(id_tipo=1, nombre_tipo="Eléctrico")
    session.add_all([gen, tipo])
    session.commit()

    # Insertar Pokémon
    poke = PokemonTabla(
        id_pokemon=1,
        nombre="Pikachu",
        imagen="img",
        altura=4,
        peso=60,
        ataque=55,
        defensa=40,
        ataque_especial=50,
        defensa_especial=50,
        puntos_de_golpe=35,
        velocidad=90,
    )
    session.add(poke)
    session.commit()

    # Insertar 4 movimientos
    for i in range(1, 5):
        mov = MovimientoTabla(
            id_movimiento=i,
            nombre=f"Mov{i}",
            id_generacion_del_movimiento=1,
            id_tipo_del_movimiento=1,
            clase_de_daño="especial",
            poder=40,
            precision=100,
            PP=30,
            efecto="",
        )
        session.add(mov)
        session.add(
            PokemonMovimientoAprendizajeTabla(
                id_pokemon=1, id_movimiento=i, metodo_de_aprendizaje=1
            )
        )
    session.commit()

    # Verificar que tiene exactamente 4 movimientos
    movimientos = session.exec(
        select(PokemonMovimientoAprendizajeTabla).where(
            PokemonMovimientoAprendizajeTabla.id_pokemon == 1
        )
    ).all()
    assert len(movimientos) == 4


def test_fallar_insertar_movimiento_duplicado(session):
    # Insertar generación y tipo
    gen = GeneracionTabla(id_generacion=1, nombre_generacion="Gen I")
    tipo = TipoTabla(id_tipo=1, nombre_tipo="Eléctrico")
    session.add_all([gen, tipo])
    session.commit()

    # Insertar Pokémon
    poke = PokemonTabla(
        id_pokemon=1,
        nombre="Pikachu",
        imagen="img",
        altura=4,
        peso=60,
        ataque=55,
        defensa=40,
        ataque_especial=50,
        defensa_especial=50,
        puntos_de_golpe=35,
        velocidad=90,
    )
    session.add(poke)
    session.commit()

    # Insertar movimiento
    mov = MovimientoTabla(
        id_movimiento=1,
        nombre="Impactrueno",
        id_generacion_del_movimiento=1,
        id_tipo_del_movimiento=1,
        clase_de_daño="especial",
        poder=40,
        precision=100,
        PP=30,
        efecto="",
    )
    session.add(mov)
    session.add(
        PokemonMovimientoAprendizajeTabla(
            id_pokemon=1, id_movimiento=1, metodo_de_aprendizaje=1
        )
    )
    session.commit()

    # Intentar insertar el mismo movimiento otra vez
    try:
        session.add(
            PokemonMovimientoAprendizajeTabla(
                id_pokemon=1, id_movimiento=1, metodo_de_aprendizaje=1
            )
        )
        session.commit()
        assert False, "Debería haber fallado al insertar movimiento duplicado"
    except Exception as e:
        assert "UNIQUE constraint failed" in str(e)


def test_actualizar_pokemon_stats(session):
    # Insertar Pokémon
    poke = PokemonTabla(
        id_pokemon=1,
        nombre="Pikachu",
        imagen="img",
        altura=4,
        peso=60,
        ataque=55,
        defensa=40,
        ataque_especial=50,
        defensa_especial=50,
        puntos_de_golpe=35,
        velocidad=90,
    )
    session.add(poke)
    session.commit()

    # Actualizar stats
    poke.ataque = 70
    poke.defensa = 55
    poke.puntos_de_golpe = 45
    session.commit()

    # Verificar que los cambios se guardaron
    updated_poke = session.get(PokemonTabla, 1)
    assert updated_poke.ataque == 70
    assert updated_poke.defensa == 55
    assert updated_poke.puntos_de_golpe == 45
