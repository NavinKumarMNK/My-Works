from sqlmodel import create_engine, text as sql_text
from sqlalchemy.ext.asyncio import AsyncEngine

from src.config.settings import ENV_CONFIG

ENV_CONFIG

# wrap the sql engine with AsyncEngine to use it as async
engine = AsyncEngine(
    create_engine(
        url=ENV_CONFIG.DATABASE_URL,
        echo=True,
    )
)


async def init_db():
    """Creates the Database connections"""
    async with engine.begin() as conn:
        _statement = sql_text(
            "SELECT 'hello';"
        )

        result = await conn.execute(_statement)
        
