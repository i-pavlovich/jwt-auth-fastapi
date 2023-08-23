from datetime import datetime
from typing import Annotated

from fastapi import HTTPException, status, Depends, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

import auth.database as db
from database import get_session
from auth.jwt import decode_jwt_token
from auth.models import User, RefreshToken

_auth_scheme = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(_auth_scheme)],
) -> str:
    payload = decode_jwt_token(credentials.credentials)
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return username


def _is_active_refresh_token(refresh_token: RefreshToken) -> bool:
    return datetime.utcnow() <= refresh_token.expires_at


async def valid_refresh_token(
    refresh_token: str = Cookie(), session: AsyncSession = Depends(get_session)
) -> RefreshToken:
    db_refresh_token = await db.get_refresh_token(refresh_token, session)
    if not db_refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    if not _is_active_refresh_token(db_refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    return db_refresh_token


async def valid_refresh_token_user(
    refresh_token: RefreshToken = Depends(valid_refresh_token),
    session: AsyncSession = Depends(get_session),
) -> User:
    user = await db.get_user_by_id(refresh_token.user_id, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return user
