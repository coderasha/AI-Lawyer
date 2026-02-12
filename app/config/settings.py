from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Legal AI Platform"
    DEFAULT_MODE: str = "AUTO"
    MEMORY_PATH: str = "data/memory/learning_memory.json"
    CONFIDENCE_THRESHOLD: float = 0.6

    class Config:
        env_file = ".env"


settings = Settings()
