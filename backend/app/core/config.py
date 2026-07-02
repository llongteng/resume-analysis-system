from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "ai-resume-analyzer"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    # AI Model
    AI_PROVIDER: str = "openai_compatible"
    AI_API_KEY: str = ""
    AI_BASE_URL: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    AI_MODEL_NAME: str = "qwen-plus"
    AI_TIMEOUT: int = 30

    # Cache
    CACHE_ENABLED: bool = True
    REDIS_URL: str = "redis://localhost:6379/0"

    # Storage
    STORAGE_DRIVER: str = "local"
    UPLOAD_DIR: str = "./storage/uploads"

    # Database
    DATABASE_URL: str = "sqlite:///./storage/app.db"

    # CORS
    CORS_ALLOW_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ALLOW_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
