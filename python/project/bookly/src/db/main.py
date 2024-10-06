from sqlmodel import create_engine, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from src.config.settings import ENV_CONFIG

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
        # Defined the Models to be created in this context
        from src.api.books.models import Book  # noqa: F401
        # from src.api.auth.models import User  # noqa: F401
        # scan any models that have created using SQLModel and create those tables.
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with Session() as session:
        yield session
