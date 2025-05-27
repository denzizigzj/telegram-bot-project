from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config.config import DATABASE_URL

# Create async engine
engine = create_async_engine(
    DATABASE_URL, echo=False
)

# Create async session
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
) 