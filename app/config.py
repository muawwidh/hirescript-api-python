from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    INTERNAL_API_SECRET: str = "dev-secret-123"
    OPENAI_MODEL: str = "gpt-4o-mini"
    PROMPT_VERSION: str = "jd-generator-v1"
    RATE_LIMIT_PER_MINUTE: int = 60
    REQUEST_TIMEOUT_SECONDS: int = 30
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()