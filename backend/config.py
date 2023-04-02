import os
import secrets


def must_get_env(name: str) -> str:
    value = os.getenv(name)

    if value is None or len(value) == 0:
        raise KeyError(f"Environment variable {name} not set")

    return value


class Config:
    ROOT = "/api/v1"

    SECRET_KEY = secrets.token_hex(32)
    JWT_SECRET_KEY = secrets.token_hex(32)

    # needs to be set if we're not using https (e.g. on localhost)
    SESSION_COOKIE_SECURE = False

    _instance = None

    def __new__(cls) -> 'Config':
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.GOOGLE_AUTH_CLIENT_ID = must_get_env("GOOGLE_AUTH_CLIENT_ID")
        self.GOOGLE_AUTH_CLIENT_SECRET = must_get_env(
            "GOOGLE_AUTH_CLIENT_SECRET")
        self.FRONTEND_URL = must_get_env("FRONTEND_URL")
