from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_MINUTES: int

    REFRESH_EXPIRE_DAYS: int

    model_config = SettingsConfigDict(env_file=".env")


settings = Config()
