import asyncio
import logging
from functools import cache
from typing import Self

import asyncpg

from wallet.base.config import SettingsFactoryDepends


class PgAccessor:
    def __init__(self, dsn: str) -> None:
        self._pool: asyncpg.Pool | None = None
        self._dsn = dsn
        self._logger = logging.getLogger("PgAccessor")
        self._logger.setLevel("INFO")

    @property
    def pool(self) -> asyncpg.Pool:
        assert self._pool, "Pool not set"
        return self._pool

    @staticmethod
    async def create_pool(dsn: str) -> asyncpg.Pool | None:
        return await asyncpg.create_pool(dsn=dsn)

    async def establish_connection(self, retries_count: int = 5, delay_sec: int = 5) -> None:
        for _ in range(retries_count):
            try:
                await self._make_ping_request()
            except:
                await asyncio.sleep(delay_sec)
            else:
                break

    async def setup(self) -> Self:
        if not self._pool or self._pool.is_closing():
            self._logger.info("Creating connection pool with dsn: %s", self._dsn)
            self._pool = await self.create_pool(self._dsn)
            self._logger.info("Connection pool created")

        return self

    async def teardown(self) -> None:
        if self._pool and not self._pool.is_closing():
            await self._pool.close()
            self._logger.info("Connection pool closed")

    async def _make_ping_request(self):
        async with self._pool.acquire() as conn:
            await conn.execute("SELECT 2+2;")


def get_pg_accessor(settings: SettingsFactoryDepends) -> PgAccessor:
    return _get_cached(settings.pg_dsn)


@cache
def _get_cached(dsn: str) -> PgAccessor:
    return PgAccessor(dsn)
