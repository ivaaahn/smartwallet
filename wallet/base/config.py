import os
from functools import cache
from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings

CONFIG_PATH = os.environ.get("CONFIG_PATH")
if not CONFIG_PATH:
    CONFIG_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        f"../etc/{os.environ.get("CONFIG_NAME", ".env.local")}",
    )


class Settings(BaseSettings):
    pg_dsn: str = ""
    secret: str = "fixme"
    alg: str = "HS256"
    access_token_exp_minutes: int = 1440

    class Config:
        env_file = CONFIG_PATH
        frozen = True


@cache
def settings_factory() -> Settings:
    return Settings()


SettingsFactoryDepends = Annotated[Settings, Depends(settings_factory)]
