"""
Configuration Management
Centralized settings with security best practices.
"""
import os
import secrets
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Application settings with secure defaults."""

    # Application
    APP_NAME: str = "AI Software Factory"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = Field(
        default="development",
        description="Environment: development, staging, production"
    )

    # API
    API_PREFIX: str = "/api"
    API_VERSION: str = "v1"

    # CORS - Restrict in production
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins"
    )
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "PATCH"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://factory:factory@localhost:5432/ai_factory",
        description="PostgreSQL connection string"
    )
    DATABASE_POOL_SIZE: int = 10
    DATABASE_POOL_OVERFLOW: int = 20
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_ECHO: bool = False

    # Redis
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection string"
    )
    REDIS_MAX_CONNECTIONS: int = 50
    REDIS_CACHE_TTL: int = 3600

    # ChromaDB
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8001
    CHROMA_PERSIST_DIR: str = "./chroma_data"
    CHROMA_COLLECTION_NAME: str = "ai_factory_memories"

    # LLM Providers
    OPENROUTER_API_KEY: Optional[str] = Field(
        default=None,
        description="OpenRouter API key for multi-model access"
    )
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1:latest"

    OPENAI_API_KEY: Optional[str] = Field(
        default=None,
        description="OpenAI API key for GPT models and embeddings"
    )
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"

    ANTHROPIC_API_KEY: Optional[str] = Field(
        default=None,
        description="Anthropic API key for Claude models"
    )
    ANTHROPIC_BASE_URL: str = "https://api.anthropic.com"

    # Default LLM Configuration
    DEFAULT_LLM_PROVIDER: str = Field(
        default="openrouter",
        description="Default LLM provider: openrouter, ollama, openai, anthropic"
    )
    DEFAULT_MODEL: str = Field(
        default="anthropic/claude-3.5-sonnet",
        description="Default model identifier"
    )
    DEFAULT_TEMPERATURE: float = 0.7
    DEFAULT_MAX_TOKENS: int = 4096

    # Agent Configuration
    MAX_AGENTS: int = 21
    AGENT_TIMEOUT: int = 300
    MAX_ITERATIONS: int = 10
    AGENT_VERBOSE: bool = False

    # Memory Configuration
    MEMORY_BACKEND: str = "chromadb"
    MEMORY_WINDOW_SIZE: int = 10
    MEMORY_RELEVANCE_THRESHOLD: float = 0.7

    # Project Configuration
    PROJECTS_DIR: str = "./projects"
    MAX_CONCURRENT_PROJECTS: int = 5
    PROJECT_ARCHIVE_DAYS: int = 90

    # Security
    SECRET_KEY: str = Field(
        default_factory=lambda: os.environ.get(
            "SECRET_KEY",
            secrets.token_urlsafe(64)
        ),
        description="Secret key for JWT and encryption - MUST be set in production"
    )
    ENCRYPTION_KEY: Optional[str] = Field(
        default=None,
        description="Fernet encryption key for API keys storage"
    )

    # JWT Configuration
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    JWT_ISSUER: str = "ai-software-factory"
    JWT_AUDIENCE: str = "ai-software-factory-api"

    # API Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/factory.log"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_MAX_SIZE: int = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT: int = 5

    # Monitoring
    METRICS_ENABLED: bool = True
    METRICS_PORT: int = 9090
    HEALTH_CHECK_INTERVAL: int = 30

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str, info) -> str:
        """Ensure SECRET_KEY meets minimum security requirements."""
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters")
        return v

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment value."""
        allowed = {"development", "staging", "production", "testing"}
        if v.lower() not in allowed:
            raise ValueError(f"ENVIRONMENT must be one of: {allowed}")
        return v.lower()

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Ensure database URL uses async driver."""
        if "asyncpg" not in v and "postgresql" in v:
            v = v.replace("postgresql://", "postgresql+asyncpg://")
        return v

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT == "development"

    def get_database_url_sync(self) -> str:
        """Get synchronous database URL for migrations."""
        return self.DATABASE_URL.replace("+asyncpg", "")

    class Config:
        env_file = "../config/.env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"


settings = Settings()
