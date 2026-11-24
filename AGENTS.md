# Guía para Agentes y Desarrolladores — AGENTS.md

Este documento define la arquitectura, convenciones técnicas, restricciones y estándares de desarrollo para cualquier agente de IA o desarrollador que trabaje sobre el repositorio `fiuba-ids-tp2-backend`.

---

## 1. Contexto y Objetivos del Proyecto

- **Materia:** Introducción al Desarrollo de Software (FIUBA) — TP2 Parte 2.
- **Objetivo Principal:** Proveer una API REST para consultar datos de Pokémon y gestionar equipos competitivos persistidos en **SQLite** utilizando **FastAPI** y **SQLModel**.
- **Requisitos Académicos:** Consultar siempre [CONSIGNA.md](file:///home/agust613/Desktop/agus/projects/fiuba-ids-pokedex/fiuba-ids-tp2-backend/CONSIGNA.md) para verificar restricciones del trabajo práctico.

---

## 2. Restricciones Críticas y Reglas del Proyecto

> [!CAUTION]
> **Prohibido agregar dependencias externas sin autorización:** El archivo `Pipfile` sólo debe contener las librerías oficiales del curso (`fastapi`, `sqlmodel`, `alembic`, `pytest`). No agregar paquetes nuevos mediante pip/pipenv sin consulta explícita.

1. **Gestor de Paquetes:** Utilizar exclusivamente `pipenv` (`pipenv install`, `pipenv run ...`).
2. **Estilo de Código:** Cumplir con las convenciones de PEP 8 y lineamientos de `black`.
3. **Flujo de Base de Datos:**
   - La base de datos es SQLite (`database.db`).
   - Las modificaciones en las tablas deben realizarse **siempre** mediante migraciones de **Alembic** (`alembic revision -m "..."` y `alembic upgrade head`).
   - El script `seed.py` puebla los datos iniciales desde los archivos CSV ubicados en `/data`.
4. **Preservación de Archivos:** No eliminar ni renombrar [CONSIGNA.md](file:///home/agust613/Desktop/agus/projects/fiuba-ids-pokedex/fiuba-ids-tp2-backend/CONSIGNA.md).

---

## 3. Arquitectura y Organización del Código

El proyecto sigue una arquitectura en capas desacoplada:

```
rutas/              --> Controladores HTTP delgados (FastAPI APIRouter)
servicios/          --> Reglas de negocio y validaciones de dominio
database/database.py--> Facade unificado de persistencia
repositorios/       --> Capa de acceso a datos pura (SQLModel Sessions)
modelos/mappers.py  --> Mapeo unificado entre entidades ORM y esquemas Pydantic
modelos/modelos.py  --> DTOs y contratos Pydantic (Request/Response)
modelos/modelos_de_la_db.py --> Modelos de tablas relacionales (SQLModel)
config/settings.py  --> Configuración centralizada (CORS, URLs, Paths)
```

### Reglas por Capa:

- **Rutas (`rutas/`):**
  - No deben contener consultas directas a la base de datos (`session.exec`, `session.get`, `session.commit`).
  - Deben validar parámetros y delegar la operación en el servicio o repositorio correspondiente.
  - Retornar siempre modelos Pydantic (DTOs).

- **Servicios (`servicios/`):**
  - Contienen las reglas y restricciones de negocio:
    - Máximo 6 integrantes por equipo.
    - Máximo 4 movimientos por integrante.
    - Validación de movimientos no repetidos.
    - Validación de compatibilidad entre generación del Pokémon y del equipo.
    - Validación de nombres de equipo únicos.

- **Repositorios (`repositorios/`):**
  - Cada entidad agregada tiene su propio repositorio (`pokemon_repositorio.py`, `equipo_repositorio.py`, etc.).
  - Deben utilizar carga ansiosa (`selectinload` / `joinedload`) para relaciones foráneas a fin de evitar el antipatrón N+1 de consultas.

- **Mappers (`modelos/mappers.py`):**
  - Toda transformación de una entidad SQLModel a un modelo Pydantic debe centralizarse en los mappers (`map_integrante_tabla_to_dto`, `map_movimiento_tabla_to_dto`). No duplicar lógica de construcción de DTOs en controladores o repositorios.

---

## 4. Comandos de Desarrollo y Validación

```bash
# Iniciar servidor en modo desarrollo
pipenv run fastapi dev main.py

# Ejecutar la suite completa de tests
pipenv run pytest -v

# Ejecutar un archivo específico de tests
pipenv run pytest tests/rutas/test_equipos.py

# Aplicar migraciones de base de datos
pipenv run alembic upgrade head

# Generar nueva migración tras cambiar modelos_de_la_db.py
pipenv run alembic revision --autogenerate -m "descripcion_del_cambio"
```

---

## 5. Convenciones de Testing

- Todos los tests residen en `tests/`.
- Las fixtures comunes para pruebas de rutas (`client`, `mock_session`, `mock_db`, `override_dependencies`) están centralizadas en [tests/rutas/conftest.py](file:///home/agust613/Desktop/agus/projects/fiuba-ids-pokedex/fiuba-ids-tp2-backend/tests/rutas/conftest.py).
- No manipular `app.dependency_overrides` manualmente dentro de los tests; utilizar las fixtures provistas por pytest.
- **Cobertura requerida:** Mantener el 100% de tests pasando (mínimo exigido por la cátedra: 75%).
