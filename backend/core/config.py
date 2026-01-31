"""
Configuración de la aplicación
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuración de la aplicación utilizando variables de entorno
    """

    # MongoDB
    MONGODB_URL: str = "mongodb://mongodb:27017"
    DATABASE_NAME: str = "books_db"

    # Security
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # API
    API_V1_PREFIX: str = "/api/v1"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
