from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from fastapi import Depends
from .config import settings

async_engine = create_async_engine(
    url=settings.connection_string
)

AsyncSessionGenerator = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


async def get_db():
    db = AsyncSessionGenerator()
    try:
        yield db
    except Exception as e:
        await db.rollback()
        raise e
    finally:
        await db.close()


class BaseORM(DeclarativeBase):
    pass

database = Annotated[AsyncSession, Depends(get_db)]