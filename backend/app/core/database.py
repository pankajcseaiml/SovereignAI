from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings

Base = declarative_base()

def init_engine():
    try:
        return create_async_engine(settings.ASYNC_DATABASE_URI, echo=False)
    except Exception:
        # Fallback to in-memory sqlite for testing / environments without asyncpg driver
        return create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

engine = init_engine()
AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
