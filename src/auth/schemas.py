import re
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, validator


_password_pattern = re.compile(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[\d])[\w@$!%*#?&]{6,}$")


class UserAuthSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

    @validator("password")
    def valid_password(cls, password: str) -> str:
        if not re.match(_password_pattern, password):
            raise ValueError(
                "Password must contain at least one lower character, one upper character and one digit"
            )
        return password


class UserCreateSchema(UserAuthSchema):
    username: str = Field(min_length=3, max_length=45)


class UserJWTSchema(BaseModel):
    username: str = Field(serialization_alias="sub")


class RefreshTokenSchema(BaseModel):
    refresh_token: str
    user_id: int
    expires_at: datetime


class AccessTokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
