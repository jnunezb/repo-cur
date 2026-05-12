# JWT Auth Service

A lightweight **FastAPI** web API that implements a **JWT (JSON Web Token)** authentication use-case.  
Dependencies are managed with **Poetry** and the service can be deployed with **Docker / Docker Compose**.

---

## Table of Contents

1. [Features](#features)
2. [Project Structure](#project-structure)
3. [Requirements](#requirements)
4. [Local Development (without Docker)](#local-development-without-docker)
5. [Running with Docker Compose](#running-with-docker-compose)
6. [API Reference](#api-reference)
7. [Configuration](#configuration)

---

## Features

- `POST /auth/token` – authenticate with `username` / `password` and receive:
  - **access token** (expires in **300 seconds**)
  - **refresh token** (expires in 3600 seconds)
- `POST /auth/refresh` – exchange a valid refresh token for a new access token
- `GET  /health` – liveness probe
- Interactive Swagger UI available at `/docs`

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application entry-point
│   ├── config.py         # Settings (pydantic-settings)
│   └── auth/
│       ├── __init__.py
│       ├── router.py     # /auth endpoints
│       ├── schemas.py    # Pydantic request/response models
│       └── utils.py      # JWT helpers, password helpers
├── pyproject.toml        # Poetry project & dependencies
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Requirements

| Tool | Version |
|------|---------|
| Python | ≥ 3.11 |
| Poetry | ≥ 1.8 |
| Docker | ≥ 24 (optional) |
| Docker Compose | ≥ 2 (optional) |

---

## Local Development (without Docker)

### 1. Install dependencies

```bash
cd backend
poetry install
```

### 2. Start the development server

```bash
poetry run uvicorn app.main:app --reload --port 8000
```

The API will be available at <http://localhost:8000>.  
Interactive documentation: <http://localhost:8000/docs>

---

## Running with Docker Compose

```bash
cd backend
docker compose up --build
```

The service starts on port **8000**.  
Stop it with `docker compose down`.

### Override settings via environment variables

Create a `.env` file next to `docker-compose.yml` (it will be read automatically):

```dotenv
SECRET_KEY=my-super-secret-key
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
ACCESS_TOKEN_EXPIRE_SECONDS=300
```

---

## API Reference

### `POST /auth/token`

Authenticate and obtain JWT tokens.

**Request** (form data – `application/x-www-form-urlencoded`):

| Field | Value |
|-------|-------|
| `username` | `admin` |
| `password` | `admin123` |

**Example – cURL:**

```bash
curl -X POST http://localhost:8000/auth/token \
  -d "username=admin&password=admin123"
```

**Example – HTTPie:**

```bash
http --form POST http://localhost:8000/auth/token username=admin password=admin123
```

**Response `200 OK`:**

```json
{
  "access_token": "<JWT>",
  "refresh_token": "<JWT>",
  "token_type": "bearer",
  "expires_in": 300
}
```

**Error `401 Unauthorized`** – wrong credentials.

---

### `POST /auth/refresh`

Exchange a refresh token for a new access token.

**Request** (JSON body):

```json
{
  "refresh_token": "<refresh JWT>"
}
```

**Example – cURL:**

```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<your_refresh_token>"}'
```

**Response `200 OK`:**

```json
{
  "access_token": "<new JWT>",
  "token_type": "bearer",
  "expires_in": 300
}
```

**Error `401 Unauthorized`** – token invalid or expired.

---

### `GET /health`

Liveness probe used by Docker health-check.

```bash
curl http://localhost:8000/health
# {"status":"ok"}
```

---

## Configuration

All settings can be overridden with environment variables or a `.env` file in the `backend/` directory.

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `change-me-in-production-…` | HMAC-SHA256 signing key |
| `ALGORITHM` | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_SECONDS` | `300` | Access token TTL |
| `REFRESH_TOKEN_EXPIRE_SECONDS` | `3600` | Refresh token TTL |
| `ADMIN_USERNAME` | `admin` | Demo admin username |
| `ADMIN_PASSWORD` | `admin123` | Demo admin password |

> **Security note:** Always set a strong, unique `SECRET_KEY` in production and never commit credentials to version control.
