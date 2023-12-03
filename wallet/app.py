from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from wallet.apps.auth.handlers import auth_router
from wallet.base.config import settings_factory
from wallet.stores.pg import get_pg_accessor


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    settings = settings_factory()
    pg_accessor = await get_pg_accessor(settings).setup()
    yield
    await pg_accessor.teardown()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
