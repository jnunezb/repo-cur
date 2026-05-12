# repo-cur

Proyecto con una Web API en **Python + FastAPI** para un caso de uso JWT.

## Estructura

```text
.
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── Dockerfile
│   └── pyproject.toml
└── docker-compose.yml
```

## Requisitos funcionales implementados

- Endpoint de autenticación con credenciales:
  - `username: admin`
  - `password: admin123`
- Retorna un `access_token` JWT con expiración de **300 segundos**.
- Endpoint para refrescar token usando `refresh_token`.

## Endpoints

### `GET /health`

Verifica estado del servicio.

### `POST /auth/token`

Solicita token JWT.

Request:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Response (ejemplo):

```json
{
  "access_token": "<jwt>",
  "refresh_token": "<jwt>",
  "token_type": "bearer",
  "expires_in": 300
}
```

### `POST /auth/refresh`

Refresca el `access_token` usando el `refresh_token`.

Request:

```json
{
  "refresh_token": "<jwt>"
}
```

Response (ejemplo):

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "expires_in": 300
}
```

## Uso con Poetry (local)

```bash
cd backend
poetry install
export JWT_SECRET='cambia-este-secreto'
export AUTH_USERNAME='admin'
export AUTH_PASSWORD='admin123'
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Uso con Docker

Desde la raíz del proyecto:

```bash
export JWT_SECRET='cambia-este-secreto'
docker compose up --build
```

La API quedará en: `http://localhost:8000`

## Ejemplos con curl

Obtener token:

```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

Refrescar token:

```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"<jwt>"}'
```
