import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.api.books.routes import book_router
from src.config.settings import PROJECT_CONFIG, APP_CONFIG
from src.db.main import init_db

# Logger
logger = logging.getLogger('uvicorn')  # Get the logger from uvicorn
logger.setLevel(logging.INFO)


# Coroutine Life Span
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan for the FastAPI Server"""
    logger.info("Server Started!")
    await init_db()
    yield
    logger.info("Server Stopped!")


# Configurations

VERSION = APP_CONFIG.app.version
API_VERSION_PREFIX = f"/api/{VERSION}"

# Application
app = FastAPI(
    title=PROJECT_CONFIG.project.name,
    version=VERSION,
    description=PROJECT_CONFIG.project.description,
    docs_url=f"{API_VERSION_PREFIX}/docs",
    redoc_url=f"{API_VERSION_PREFIX}/redoc",
    openapi_url=f"{API_VERSION_PREFIX}/openapi.json",
    lifespan=lifespan,
)


app.include_router(
    book_router, prefix=f"{API_VERSION_PREFIX}/books", tags=["Books"],
)
