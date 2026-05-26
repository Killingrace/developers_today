from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import cached_property
from pathlib import Path

BASE_PATH = Path(__file__).parent.parent

class Settings(BaseSettings):
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "db"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    EXTERNAL_API: str = "https://api.artic.edu/api/v1/artworks/"

    @cached_property
    def connection_string(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=BASE_PATH / ".env")

settings = Settings()
