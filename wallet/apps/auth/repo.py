from asyncpg.pool import PoolConnectionProxy

from .entities import UserDC
from .errors import UserNotFoundError


class AuthUserRepo:
    @classmethod
    async def get_by_email(
        cls, conn: PoolConnectionProxy, email: str
    ) -> UserDC:
        row = await conn.fetchrow("SELECT * FROM users WHERE email = $1", email)
        if not row:
            raise UserNotFoundError

        return UserDC(
            email=row["email"],
            hashed_password=row["password"],
            name=row["name"],
        )
