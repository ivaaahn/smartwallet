import asyncio
from asyncio import AbstractEventLoop
from collections.abc import AsyncIterator, Iterator

import asyncpg
import pytest
from asyncpg import Connection
from fastapi.testclient import TestClient

from wallet.app import app
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
