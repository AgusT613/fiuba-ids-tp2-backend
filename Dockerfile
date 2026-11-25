# Usar imagen base ligera oficial de Python 3.13
FROM python:3.13.3-slim

# Evitar escritura de bytecode y habilitar salida sin buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar curl para healthchecks del contenedor
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar pipenv
RUN pip install --no-cache-dir pipenv

# Copiar manifiesto de dependencias primero para optimizar el cache de capas
COPY Pipfile Pipfile.lock ./

# Instalar paquetes a nivel de sistema sin crear entorno virtual innecesario
RUN pipenv install --system --deploy

# Copiar el código fuente y los datos iniciales
COPY . .

# Exponer el puerto predeterminado de FastAPI
EXPOSE 8000

# Healthcheck para verificar disponibilidad de la API
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Comando de inicio de la aplicación en modo producción
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
