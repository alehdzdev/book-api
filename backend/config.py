# Third Party
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # MongoDB
    MONGODB_URL: str
    DATABASE_NAME: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # API
    API_V1_PREFIX: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
