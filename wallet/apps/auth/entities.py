from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UserDC:
    name: str
    email: str
    hashed_password: str


@dataclass(frozen=True, slots=True)
class AccessTokenDC:
    access_token: str
    token_type: str = "bearer"


@dataclass(frozen=True, slots=True)
class AccessTokenPayloadDC:
    email: str
