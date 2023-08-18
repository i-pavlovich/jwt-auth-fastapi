from typing import AsyncGenerator

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from config import settings


class Base(DeclarativeBase):
    pass


_engine = create_async_engine(settings.DATABASE_URL, echo=True)
sissionmaker = async_sessionmaker(_engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with sissionmaker() as session:
        yield session
