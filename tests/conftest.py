import asyncio
from asyncio import AbstractEventLoop
from collections.abc import AsyncIterator, Iterator

import asyncpg
import httpx
import pytest
from asyncpg import Connection
from asyncpg.pool import PoolConnectionProxy
from fastapi.testclient import TestClient

from wallet.app import app
from wallet.apps.auth.entities import UserDC
from wallet.base.config import Settings, settings_factory

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def event_loop() -> Iterator[AbstractEventLoop]:
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def settings() -> Settings:
    return settings_factory()


@pytest.fixture(autouse=True)
async def conn(settings: Settings) -> AsyncIterator[Connection]:
    conn = await asyncpg.connect(dsn=settings.pg_dsn)
    yield conn

    tables = await conn.fetch(
        "SELECT tablename FROM pg_tables WHERE schemaname = 'public' and tablename != 'schema_migrations'"
    )
    for table in tables:
        await conn.execute(
            f"TRUNCATE {table["tablename"]} RESTART IDENTITY CASCADE"
        )
    await conn.close()


@pytest.fixture
async def user(conn: PoolConnectionProxy) -> UserDC:
    # INFO: pwd: 123456
    user = UserDC(
        name="Вася",
        email="vvv@mail.ru",
        hashed_password="$2b$12$Y/NpUBfgqDUm8026j1FHPOK9dVcoSgi974LIc1FNBy5NC5wl/0iye",
    )
    await conn.execute(
        "INSERT INTO users (name, email, password) VALUES ($1, $2, $3)",
        user.name,
        user.email,
        user.hashed_password,
    )
    return user


class BearerAuth:
    def __init__(self, token: str) -> None:
        self._token = token

    def __call__(self, request: httpx.Request) -> httpx.Request:
        request.headers["Authorization"] = f"Bearer {self._token}"
        return request
