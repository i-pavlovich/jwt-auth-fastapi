from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import auth.database as db
from config import settings
from auth.security import verify_password
from auth.models import User
from auth.schemas import UserAuthSchema, RefreshTokenSchema
from auth.database import get_user_by_email
from auth.utils import generate_sequence


async def authenticate_user(auth_data: UserAuthSchema, session: AsyncSession) -> User:
    user = await get_user_by_email(auth_data.email, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email",
        )
    if not verify_password(auth_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
        )
    return user


async def create_refresh_token(
    user_id: int,
    session: AsyncSession,
    expires_delta: timedelta = timedelta(days=settings.REFRESH_EXPIRE_DAYS),
) -> RefreshTokenSchema:
    refresh_token = RefreshTokenSchema(
        refresh_token=generate_sequence(32),
        user_id=user_id,
        expires_at=datetime.utcnow() + expires_delta,
    )
    await db.add_refresh_token(refresh_token, session)
    return refresh_token
