from datetime import datetime, timedelta, timezone
import os

import jwt
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


ACCESS_TOKEN_EXPIRE_SECONDS = 300
REFRESH_TOKEN_EXPIRE_SECONDS = 600
JWT_SECRET = os.getenv("JWT_SECRET", "change-me-in-production")
JWT_ALGORITHM = "HS256"
VALID_USERNAME = "admin"
VALID_PASSWORD = "admin123"

app = FastAPI(title="JWT FastAPI Demo", version="1.0.0")


class LoginRequest(BaseModel):
    username: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


def create_token(subject: str, token_type: str, expires_in: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=expires_in)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/auth/token")
def get_token(payload: LoginRequest) -> dict[str, str | int]:
    if payload.username != VALID_USERNAME or payload.password != VALID_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_token(
        subject=payload.username,
        token_type="access",
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
    )
    refresh_token = create_token(
        subject=payload.username,
        token_type="refresh",
        expires_in=REFRESH_TOKEN_EXPIRE_SECONDS,
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_SECONDS,
    }


@app.post("/auth/refresh")
def refresh_token(payload: RefreshRequest) -> dict[str, str | int]:
    try:
        decoded = jwt.decode(
            payload.refresh_token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        ) from exc

    if decoded.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    subject = decoded.get("sub")
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    new_access_token = create_token(
        subject=subject,
        token_type="access",
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
    )
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_SECONDS,
    }
