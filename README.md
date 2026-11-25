# IntroDex Backend — PokeAPI

Backend RESTful desarrollado en Python para la gestión, consulta y armado de equipos Pokémon (IntroDex). Proyecto correspondiente al Trabajo Práctico 2 (Parte 2) de la materia **Introducción al Desarrollo de Software (FIUBA)**.

---

## 🛠️ Tecnologías y Requisitos

- **Lenguaje:** Python 3.13+
- **Framework Web:** [FastAPI](https://fastapi.tiangolo.com/) (con Starlette y Pydantic v2)
- **Base de Datos y ORM:** PostgreSQL / SQLite y [SQLModel](https://sqlmodel.tiangolo.com/) (SQLAlchemy core con driver `psycopg2`)
- **Migraciones:** [Alembic](https://alembic.sqlalchemy.org/)
- **Entorno Virtual y Paquetes:** [Pipenv](https://pipenv.pypa.io/)
- **Contenedores:** Docker Compose (PostgreSQL 16)
- **Testing:** [Pytest](https://docs.pytest.org/) con `TestClient`

---

## 🐳 Ejecución con Docker (Recomendada)

Puedes levantar todo el entorno (Base de datos PostgreSQL + API de FastAPI) con un solo comando gracias a Docker Compose:

### 1. Configurar variables de entorno
Copia la plantilla de variables si aún no lo hiciste:
```bash
cp .env.example .env
```
*(Todas las credenciales, puertos y URLs se configuran en `.env` como única fuente de verdad).*

### 2. Construir e iniciar los contenedores
```bash
docker compose up -d --build
```
> [!NOTE]
> La API espera automáticamente a que el contenedor de PostgreSQL esté saludable (`healthy`). Luego, ejecuta las migraciones pendientes de Alembic y corre el seed inicial de datos desde `/data`.

### 3. Verificar el estado
```bash
# Ver estado de los contenedores
docker compose ps

# Ver logs en tiempo real
docker compose logs -f api
```

La API quedará disponible en `http://localhost:8000` (docs en `http://localhost:8000/docs`).

### 4. Detener o limpiar el entorno
```bash
# Detener los contenedores
docker compose down

# Detener y eliminar volúmenes (reiniciar base de datos limpia)
docker compose down -v

# Limpieza total (contenedores, volúmenes e imágenes construidas)
docker compose down -v --rmi all
```

---

## 💻 Desarrollo Local (Sin Docker para la API)

### 1. Clonar el repositorio y configurar el entorno
Asegúrate de contar con Python 3.13 y `pipenv` instalados:

```bash
# Instalar dependencias del Pipfile
pipenv install

# Configurar variables de entorno
cp .env.example .env
```

### 2. Base de Datos (PostgreSQL o SQLite)

#### Opción A: Solo PostgreSQL con Docker Compose
Si quieres correr únicamente la base de datos en Docker y la aplicación en tu máquina local:

```bash
docker compose up -d db
```

#### Opción B: SQLite Local
Si prefieres utilizar SQLite localmente sin Docker:
```bash
export DATABASE_URL="sqlite:///database.db"
```

### 3. Migraciones y Seed de Datos
Al iniciar la aplicación, el ciclo de vida de FastAPI (`lifespan`) aplica automáticamente las migraciones pendientes con Alembic y realiza el seed de datos si la base se encuentra vacía.

Si deseas ejecutar manualmente las migraciones:

```bash
pipenv run alembic upgrade head
```

Para poblar manualmente la base de datos (opcional):

```bash
pipenv run python -c "from seed import seed; seed()"
```

### 4. Iniciar el Servidor de Desarrollo

```bash
pipenv run fastapi dev main.py
```

La API quedará disponible en:
- **URL Base:** `http://localhost:8000`
- **Documentación Interactiva (Swagger/OpenAPI):** `http://localhost:8000/docs`
- **Documentación Alternativa (ReDoc):** `http://localhost:8000/redoc`

---

## 🧪 Ejecución de Pruebas

La suite de pruebas unitarias e integración cuenta con 60 tests que validan todas las rutas, repositorios, reglas de negocio y restricciones de base de datos.

```bash
# Ejecutar todos los tests
pipenv run pytest

# Ejecutar tests con salida detallada
pipenv run pytest -v
```

---

## 🏗️ Arquitectura del Proyecto

El proyecto implementa una **arquitectura en capas desacoplada** con separación de responsabilidades:

```
├── alembic/                # Historial y scripts de migraciones de base de datos
├── bruno/                  # Colección de peticiones HTTP para el cliente Bruno
├── config/                 # Configuración centralizada de variables de entorno y CORS
│   └── settings.py
├── constantes/             # Constantes del proyecto y rutas a archivos CSV
├── data/                   # Archivos CSV con catálogos oficiales de Pokémon
├── database/               # Facade de persistencia y conexión
│   └── database.py
├── dependencias/           # Inyección de dependencias de FastAPI (sesión, repositorios)
├── modelos/                # Esquemas y contratos de datos
│   ├── filtros.py          # Modelos de validación de filtros y paginación
│   ├── mappers.py          # Mappers de entidades ORM a DTOs de respuesta
│   ├── modelos.py          # DTOs y esquemas Pydantic
│   └── modelos_de_la_db.py # Modelos relacionales SQLModel (tablas)
├── repositorios/           # Capa de acceso a datos (Data Access Layer)
│   ├── equipo_repositorio.py
│   ├── generacion_repositorio.py
│   ├── movimiento_repositorio.py
│   └── pokemon_repositorio.py
├── rutas/                  # Controladores y endpoints HTTP (FastAPI APIRouter)
│   ├── equipos.py
│   ├── generaciones.py
│   ├── index.py
│   ├── movimientos.py
│   └── pokemones.py
├── servicios/              # Capa de lógica y reglas de negocio
│   └── equipo_servicio.py
├── tests/                  # Suite de pruebas unitarias e integración
│   ├── conftest.py
│   ├── rutas/              # Tests de endpoints HTTP
│   └── test_database.py    # Tests directos de base de datos
├── utils/                  # Utilidades auxiliares (cálculo de imágenes, filtros)
├── CONSIGNA.md             # Enunciado y requerimientos originales del TP
├── main.py                 # Punto de entrada de la aplicación FastAPI
└── seed.py                 # Script de carga inicial de datos desde CSV
```

---

## 📡 Resumen de Endpoints de la API

### 🐾 Pokémon (`/api/pokemon`)
- `GET /api/pokemon` — Listado paginado de Pokémon. Admite filtros por query params:
  - `limit` (int, default 100, max 100)
  - `offset` (int, default 0)
  - `nombre_parcial` (string)
  - `tipo` (int)
- `GET /api/pokemon/{id}` — Detalle exhaustivo de un Pokémon (estadísticas, tipos con debilidades, generaciones, habilidades, evoluciones y movimientos por nivel, máquina y huevo).

### ⚔️ Movimientos (`/api/movimientos`)
- `GET /api/movimientos` — Listado paginado y filtrable de movimientos (`nombre_parcial`, `tipo`, `limit`, `offset`).
- `GET /api/movimientos/{id}` — Detalle de un movimiento y listas de Pokémon que lo aprenden categorizados por método (huevo, nivel, máquina).

### 🌍 Generaciones (`/api/generaciones`)
- `GET /api/generaciones` — Listado de todas las generaciones disponibles.

### 🛡️ Equipos e Integrantes (`/api/equipos`)
- `GET /api/equipos` — Lista todos los equipos creados junto a su cantidad de integrantes.
- `GET /api/equipos/{id}` — Obtiene un equipo por ID con todos sus integrantes y estadísticas completas.
- `POST /api/equipos` — Crea un nuevo equipo (`nombre`, `id_generacion`).
- `PUT /api/equipos/{id}` — Actualiza el nombre o la generación del equipo.
- `DELETE /api/equipos/{id}` — Elimina un equipo y sus integrantes.
- `POST /api/equipos/{id_equipo}/integrantes` — Agrega un Pokémon al equipo (máximo 6 integrantes por equipo).
- `PUT /api/equipos/{id_equipo}/integrantes/{id_integrante}` — Actualiza el apodo o la lista de hasta 4 movimientos de un integrante.
- `POST /api/equipos/{id_equipo}/integrantes/{id_integrante}/movimientos` — Asigna un movimiento individual a un integrante.
- `DELETE /api/equipos/{id_equipo}/integrantes/{id_integrante}` — Elimina un integrante del equipo.

---

## 📬 Colección de Peticiones Bruno

El directorio `/bruno` incluye una colección completa de solicitudes listas para importar en el cliente [Bruno](https://www.usebruno.com/), organizadas por dominio (`pokemon`, `movimientos`, `generaciones`, `equipos`) con entornos locales preconfigurados.
