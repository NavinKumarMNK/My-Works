import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI, status

from src.api.books.routes import book_router
from src.api.auth.routes import auth_router
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


@app.get("/", status_code=status.HTTP_200_OK, tags=["Default"])
async def entry() -> dict:
    return {"message": "Rest API service is on /api/v1"}


@app.get(f"{API_VERSION_PREFIX}/health", status_code=status.HTTP_200_OK, tags=["Default"])
async def health_check() -> dict:
    return {"message": "Health is fine"}


app.include_router(
    book_router, prefix=f"{API_VERSION_PREFIX}/books", tags=["Books"],
)
app.include_router(
    auth_router, prefix=f"{API_VERSION_PREFIX}/auth", tags=["Auth"],
)
