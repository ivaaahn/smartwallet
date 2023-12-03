from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from freezegun import freeze_time
from jose import jwt

from tests.conftest import BearerAuth
from wallet.app import app
from wallet.apps.auth.entities import UserDC
from wallet.base.config import Settings


@pytest.mark.usefixtures("user")
@freeze_time("2024-01-01T15:00:00")
def test_success(settings: Settings) -> None:
    """Проверяет корректность выданного токена"""
    with TestClient(app) as cli:
        response = cli.post(
            "/auth/tokens/access",
            data={
                "username": "vvv@mail.ru",
                "password": "123456",
            },
        )

    data: dict = response.json()
    decoded = jwt.decode(
        data["access_token"], settings.secret, algorithms=[settings.alg]
    )

    assert response.status_code == 200
    assert data["token_type"] == "bearer"
    assert decoded == {
        "exp": datetime.fromisoformat("2024-01-02T15:00:00").timestamp(),
        "sub": "vvv@mail.ru",
    }


@pytest.mark.usefixtures("user")
@freeze_time("2024-01-01T15:00:00")
@pytest.mark.parametrize(
    "username,password",
    [
        ("vvv@mail.ru", "1234567"),  # incorrect password
        ("vvvv@mail.ru", "123456"),  # incorrect email
        ("vvvv@mail.ru", "1234567"),  # incorrect both
    ],
)
def test_when_incorrect_credentials_get_401(
    username: str, password: str
) -> None:
    """Проверяет корректность выданного токена"""
    with TestClient(app) as cli:
        response = cli.post(
            "/auth/tokens/access",
            data={"username": username, "password": password},
        )

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect credentials"}


@freeze_time("2024-01-01T15:00:00")
def test_when_token_fresh_get_current_user(
    user: UserDC, settings: Settings
) -> None:
    """Проверяет корректность выданного токена"""
    # Fresh token
    token = jwt.encode(
        claims={
            "sub": user.email,
            "exp": datetime(2024, 1, 1, 15, 15, 0).timestamp(),
        },
        key=settings.secret,
        algorithm=settings.alg,
    )

    with TestClient(app) as cli:
        response = cli.get("/auth/me", auth=BearerAuth(token))

    assert response.status_code == 200
    assert response.json() == {"email": user.email, "name": user.name}


@freeze_time("2024-01-01T15:00:00")
def test_when_token_expired_get_401(user: UserDC, settings: Settings) -> None:
    """Проверяет корректность выданного токена"""
    # Expired token
    token = jwt.encode(
        claims={
            "sub": user.email,
            "exp": datetime(2024, 1, 1, 14, 0, 0).timestamp(),
        },
        key=settings.secret,
        algorithm=settings.alg,
    )

    with TestClient(app) as cli:
        response = cli.get("/auth/me", auth=BearerAuth(token))

    assert response.status_code == 401
    assert response.json() == {"detail": "Access token not valid"}


@freeze_time("2024-01-01T15:00:00")
def test_when_email_unknown_get_401(settings: Settings) -> None:
    """Проверяет корректность выданного токена"""
    # Fresh token
    token = jwt.encode(
        claims={
            "sub": "unknown_email@gmail.com",
            "exp": datetime(2024, 1, 1, 16, 0, 0).timestamp(),
        },
        key=settings.secret,
        algorithm=settings.alg,
    )

    with TestClient(app) as cli:
        response = cli.get("/auth/me", auth=BearerAuth(token))

    assert response.status_code == 401
    assert response.json() == {"detail": "Access token not valid"}
