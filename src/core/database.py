from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

DATABASE_URL = "sqlite+aiosqlite:///./app.db"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

class Base(MappedAsDataclass, DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session: # pragma: no cover
        yield session # pragma: no cover
            
DBSession = Annotated[AsyncSession, Depends(get_db)]