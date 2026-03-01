from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # JWT
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # PostgreSQL
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/deepfake_db"

    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "deepfake_detection"

    # Security
    MAX_FILE_SIZE_MB: int = 100
    AUTO_DELETE_AFTER_HOURS: int = 24
    RATE_LIMIT_PER_MINUTE: int = 30

    # ML model paths (optional)
    IMAGE_MODEL_PATH: str = ""
    VIDEO_MODEL_PATH: str = ""
    AUDIO_MODEL_PATH: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
