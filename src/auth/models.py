from typing import Optional
from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
    __tablename__ = "auth_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(45), unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    name: Mapped[Optional[str]] = mapped_column(String(35))
    surname: Mapped[Optional[str]] = mapped_column(String(35))

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    is_active: Mapped[bool] = mapped_column(server_default="true")
    is_admin: Mapped[bool] = mapped_column(server_default="false")
    is_blocked: Mapped[bool] = mapped_column(server_default="false")
    is_verified: Mapped[bool] = mapped_column(server_default="false")


class RefreshToken(Base):
    __tablename__ = "auth_refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    refresh_token: Mapped[str] = mapped_column(unique=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("auth_users.id", ondelete="CASCADE")
    )

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    expires_at: Mapped[datetime]

    is_blocked: Mapped[bool] = mapped_column(server_default="false")
