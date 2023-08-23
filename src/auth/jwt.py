from typing import Any
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import jwt

from config import settings
from auth.schemas import UserJWTSchema


def create_jwt_token(
    user_data: UserJWTSchema,
    expires_delta: timedelta = timedelta(minutes=settings.JWT_EXPIRE_MINUTES),
) -> str:
    """Generate a JWT token from the passed data.

    Args:
        user_data (UserJWTSchema): The user data for the token.
        expires_delta (timedelta, optional): The token lifetime. Defaults to the value from the project settings.

    Returns:
        str: A JWT token.
    """

    jwt_data = user_data.model_dump(by_alias=True)
    jwt_data.update(
        {
            "exp": datetime.utcnow() + expires_delta,
            "iss": "auth-service",
        }
    )
    token = jwt.encode(
        claims=jwt_data, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return token


def decode_jwt_token(token: str) -> dict[str, Any]:
    """Decode the passed JWT token.

    Args:
        token (str): The JWT token to be decoded.

    Raises:
        HTTPException: Raised if the token is invalid or cannot be decoded.

    Returns:
        dict[str, Any]: A token payload.
    """

    try:
        payload = jwt.decode(
            token=token, key=settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM
        )
        return payload
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
