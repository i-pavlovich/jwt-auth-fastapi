from typing import Annotated

from fastapi import Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from auth.security import get_password_hash
from auth.models import User, RefreshToken
from auth.schemas import UserCreateSchema, RefreshTokenSchema


async def add_user(
    user: UserCreateSchema, session: Annotated[AsyncSession, Depends(get_session)]
) -> int | None:
    user.password = get_password_hash(user.password)
    user_data = user.model_dump()
    stmt = insert(User).values(**user_data).returning(User.id)
    result = await session.execute(stmt)
    await session.commit()
    return result.scalars().first()


async def add_refresh_token(
    refresh_token: RefreshTokenSchema,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> int | None:
    refresh_token_data = refresh_token.model_dump()
    stmt = insert(RefreshToken).values(**refresh_token_data).returning(RefreshToken.id)
    result = await session.execute(stmt)
    await session.commit()
    return result.scalars().first()


async def get_user_by_username(
    username: str, session: Annotated[AsyncSession, Depends(get_session)]
) -> User | None:
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_user_by_email(
    email: str, session: Annotated[AsyncSession, Depends(get_session)]
) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_user_by_id(
    id: int, session: Annotated[AsyncSession, Depends(get_session)]
) -> User | None:
    stmt = select(User).where(User.id == id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_refresh_token(
    refresh_token: str, session: Annotated[AsyncSession, Depends(get_session)]
) -> RefreshToken | None:
    stmt = select(RefreshToken).where(RefreshToken.refresh_token == refresh_token)
    result = await session.execute(stmt)
    return result.scalars().first()
