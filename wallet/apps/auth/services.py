from datetime import datetime, timedelta

import tzlocal
from fastapi import Depends
from jose import JWTError, jwt
from passlib.context import CryptContext

from wallet.base.config import SettingsFactoryDepends
from wallet.stores.pg import get_pg_accessor

from .entities import AccessTokenDC, AccessTokenPayloadDC, UserDC
from .errors import AccessTokenError, IncorrectPasswordError
from .repo import AuthUserRepo

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenHandler:
    def __init__(self, settings: SettingsFactoryDepends) -> None:
        self.secret: str = settings.secret
        self.alg: str = settings.alg
        self.exp: timedelta = timedelta(
            minutes=settings.access_token_exp_minutes
        )

    @staticmethod
    def _get_current_datetime() -> datetime:
        return datetime.now(tzlocal.get_localzone())

    def decode(self, token: str) -> AccessTokenPayloadDC:
        """
        Exceptions:
            – AccessTokenError
        """
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.alg])
        except JWTError as err:
            raise AccessTokenError from err

        email = payload.get("sub")
        if not email:
            raise AccessTokenError

        exp = payload.get("exp")
        if not exp:
            raise AccessTokenError

        exp_datetime = datetime.fromtimestamp(exp, tz=tzlocal.get_localzone())
        if exp_datetime < self._get_current_datetime():
            raise AccessTokenError

        return AccessTokenPayloadDC(email=email)

    def encode(self, payload: AccessTokenPayloadDC) -> AccessTokenDC:
        access_token = jwt.encode(
            claims={
                "sub": payload.email,
                "exp": (self._get_current_datetime() + self.exp).timestamp(),
            },
            key=self.secret,
            algorithm=self.alg,
        )
        return AccessTokenDC(access_token)


class AuthService:
    def __init__(
        self,
        settings: SettingsFactoryDepends,
        repo: AuthUserRepo = Depends(),
        token_handler: TokenHandler = Depends(),
    ) -> None:
        self.pool = get_pg_accessor(settings).pool
        self.repo = repo
        self.token_handler = token_handler

    async def get_current_user(self, token: str) -> UserDC:
        """
        Exceptions:
            UserNotFoundError
            TokenError
        """
        token_payload = self.token_handler.decode(token)
        async with self.pool.acquire() as conn:
            return await self.repo.get_by_email(conn, token_payload.email)

    async def login(self, email: str, password: str) -> AccessTokenDC:
        """
        Exceptions:
            UserNotFoundError
            IncorrectPasswordError
        """

        async with self.pool.acquire() as conn:
            user = await self.repo.get_by_email(conn, email)

        if not pwd_context.verify(password, user.hashed_password):
            raise IncorrectPasswordError

        return self.token_handler.encode(AccessTokenPayloadDC(email=user.email))
