from typing import Annotated

from fastapi import APIRouter, Response, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

import auth.database as db
from database import get_session
from auth.schemas import (
    UserCreateSchema,
    UserAuthSchema,
    UserJWTSchema,
    AccessTokenResponseSchema,
)
from auth.models import User, RefreshToken
from auth.services import authenticate_user, create_refresh_token
from auth.jwt import create_jwt_token
from auth.dependencies import (
    get_current_user,
    valid_refresh_token,
    valid_refresh_token_user,
)
from auth.cookies import get_refresh_token_settings

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register")
async def create_user(
    register_data: Annotated[UserCreateSchema, Body()],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> int | None:
    new_user_id = await db.add_user(register_data, session)
    return new_user_id


@router.post("/tokens")
async def auth_user(
    auth_data: Annotated[UserAuthSchema, Body()],
    session: Annotated[AsyncSession, Depends(get_session)],
    response: Response,
):
    user = await authenticate_user(auth_data, session)

    refresh_token = await create_refresh_token(user.id, session)
    response.set_cookie(**get_refresh_token_settings(refresh_token.refresh_token))
    user_jwt_data = UserJWTSchema(
        username=user.username,
    )
    return AccessTokenResponseSchema(
        access_token=create_jwt_token(user_jwt_data),
        refresh_token=refresh_token.refresh_token,
    )


@router.put("/tokens")
async def refresh_tokens(
    session: Annotated[AsyncSession, Depends(get_session)],
    response: Response,
    refresh_token: RefreshToken = Depends(valid_refresh_token),
    user: User = Depends(valid_refresh_token_user),
):
    refresh_token = await create_refresh_token(refresh_token.user_id, session)
    response.set_cookie(**get_refresh_token_settings(refresh_token.refresh_token))

    user_jwt_data = UserJWTSchema(
        username=user.username,
    )
    return AccessTokenResponseSchema(
        access_token=create_jwt_token(user_jwt_data),
        refresh_token=refresh_token.refresh_token,
    )


@router.delete("/tokens")
async def logout_user(
    response: Response,
    refresh_token: RefreshToken = Depends(valid_refresh_token),
) -> None:
    response.delete_cookie(
        **get_refresh_token_settings(refresh_token.refresh_token, True)
    )


@router.get("/account")
async def profile(
    current_user: Annotated[str, Depends(get_current_user)],
):
    return {"Hello": current_user}
