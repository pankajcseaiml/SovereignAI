from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "SovereignAI"
    API_V1_STR: str = "/api/v1"
    APP_ENV: str = "development"
    
    # Postgres / Database
    DATABASE_URL: Optional[str] = None
    POSTGRES_HOST: str = "postgres"
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "sovereignai"
    POSTGRES_PORT: str = "5432"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    
    # Qdrant
    QDRANT_HOST: str = "qdrant"
    QDRANT_PORT: int = 6333
    
    # URLs & Paths
    AI_ENGINE_URL: str = "http://ai-engine:9000"
    MODEL_SERVER_URL: str = "http://ollama:11434"
    STORAGE_PATH: str = "/storage"
    
    # Security & Backup
    JWT_SECRET: str = "supersecretkey_change_in_production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    BACKUP_ENCRYPTION_KEY: Optional[str] = None
    LOG_LEVEL: str = "INFO"
    
    @property
    def ASYNC_DATABASE_URI(self) -> str:
        if self.DATABASE_URL:
            url = self.DATABASE_URL
            if url.startswith("postgresql://"):
                url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
            elif url.startswith("sqlite://") and not url.startswith("sqlite+aiosqlite://"):
                url = url.replace("sqlite://", "sqlite+aiosqlite://", 1)
            return url
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

settings = Settings()
