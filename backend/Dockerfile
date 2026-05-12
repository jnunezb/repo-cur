# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Install Poetry
RUN pip install --no-cache-dir poetry==1.8.3

WORKDIR /app

# Copy dependency files first for layer caching
COPY pyproject.toml poetry.lock* ./

# Install production dependencies only (no virtualenv inside Docker)
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# Copy application source
COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
