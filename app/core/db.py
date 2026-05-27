from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings


async_engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    echo=settings.ENVIRONMENT == "DEV",
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)




async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise