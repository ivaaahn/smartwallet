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

    async def setup(self) -> Self:
        if not self._pool or self._pool.is_closing():
            self._pool = await self.create_pool(self._dsn)
            self._logger.info("Connection pool created")
        return self

    async def teardown(self) -> None:
        if self._pool and not self._pool.is_closing():
            await self._pool.close()
            self._logger.info("Connection pool closed")


def get_pg_accessor(settings: SettingsFactoryDepends) -> PgAccessor:
    return _get_cached(settings.pg_dsn)


@cache
def _get_cached(dsn: str) -> PgAccessor:
    return PgAccessor(dsn)
