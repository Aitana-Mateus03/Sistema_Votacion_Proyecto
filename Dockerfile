# Etapa 1: Construcción y dependencias (Builder)
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Etapa 2: Imagen final de producción segura y ligera
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev && rm -rf /var/lib/apt/lists/*

# Copiar dependencias compiladas desde el builder
COPY --from=builder /root/.local /home/appuser/.local
COPY . /app

# Crear usuario seguro no-root
RUN useradd -m appuser && chown -R appuser:appuser /app /home/appuser/.local
USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]