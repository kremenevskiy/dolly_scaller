from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src import database
from src.config import settings
from src.model.router import model_router
from src.subscription_details.router import subscription_router
from src.user.router import user_router
from src.user_profile.router import user_profile_router


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # Startup
    await database.DatabaseManager.init_pool()
    print('✅ Database connection pool initialized')
    yield
    # Shutdown


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'),
    allow_headers=settings.CORS_HEADERS,
)


app.include_router(user_router)
app.include_router(model_router)
app.include_router(subscription_router)
app.include_router(user_profile_router)


@app.get('/healthcheck', include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {'status': 'ok'}
