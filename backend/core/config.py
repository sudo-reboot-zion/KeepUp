from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, AnyHttpUrl, model_validator
from typing import List, Union
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "KEEP-UP API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    DATABASE_URL: str
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_RECYCLE: int = 3600
    COHERE_API_KEY: str
    DB_ECHO: bool = False
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    TAVILY_API_KEY: str

    GROQ_API_KEY: str | None = None
    OPIK_API_KEY: str | None = None
    OPIK_PROJECT_NAME: str = "KEEP-UP"
    OPIK_WORKSPACE: str = "default"
    WEATHER_API_KEY: str | None = None

    SIMPLE_AGENT_MODEL: str = "llama-3.2-70b-8192"
    MAX_REQUESTS_PER_MINUTE: int = 60

    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    CORS_ORIGINS: List[str] = [
        "https://keep-up-dun.vercel.app",  
        "https://keep-up-dun.vercel.app/",
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @model_validator(mode="after")
    def merge_cors_origins(self) -> "Settings":
        for origin in self.BACKEND_CORS_ORIGINS:
            if str(origin) not in self.CORS_ORIGINS:
                self.CORS_ORIGINS.append(str(origin))
        return self

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

settings = Settings()

@lru_cache()
def get_settings() -> Settings:
    return settings
