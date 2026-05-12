from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError

from app.auth.schemas import AccessTokenResponse, RefreshRequest, TokenResponse
from app.auth.utils import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/token",
    response_model=TokenResponse,
    summary="Login and obtain JWT tokens",
    description=(
        "Authenticate with **username** and **password** (form fields). "
        "Returns an access token (valid for 300 s) and a refresh token."
    ),
)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    subject = {"sub": form_data.username}
    access_token = create_access_token(subject)
    refresh_token = create_refresh_token(subject)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_SECONDS,
    )


@router.post(
    "/refresh",
    response_model=AccessTokenResponse,
    summary="Refresh the access token",
    description="Exchange a valid **refresh token** for a new access token.",
)
def refresh_token(body: RefreshRequest):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(body.refresh_token)
        if payload.get("type") != "refresh":
            raise credentials_exception
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    new_access_token = create_access_token({"sub": username})
    return AccessTokenResponse(
        access_token=new_access_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_SECONDS,
    )
