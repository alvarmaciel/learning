FROM python:3.13-slim
    LABEL org.opencontainers.image.authors="Alvar Maciel <alvarmaciel@gmail.com>"
# Install uv
RUN pip install uv

WORKDIR /app

# Copy dependenciy files first (layer cacching)
COPY pyproject.toml .
COPY uv.lock* .

# Install dependencies
RUN uv sync

# Copy source code

COPY src/ src/
COPY tests/ tests/
COPY alembic/ alembic/
COPY alembic.ini .

ENV PYTHONPATH=/app/src

CMD ["uv", "run", "uvicorn", "ecommerce.application.main:app", "--host", "0.0.0.0", "--port", "8000"]
