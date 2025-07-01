"""Application configuration."""

from typing import Any, Dict, List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # Application
    DEBUG: bool = Field(default=False, description="Debug mode")
    SECRET_KEY: str = Field(default="dev-secret-key", description="Secret key")
    ALLOWED_ORIGINS: List[str] = Field(default=["http://localhost:3000"], description="CORS allowed origins")

    # Database
    DATABASE_URL: str = Field(
        default="postgresql://postgres:password@localhost:5432/data_lens",
        description="Database URL",
    )
    REDIS_URL: str = Field(default="redis://localhost:6379", description="Redis URL")

    # LLM Providers
    OPENAI_API_KEY: str = Field(default="", description="OpenAI API key")
    ANTHROPIC_API_KEY: str = Field(default="", description="Anthropic API key")

    # LLM Configuration
    @property
    def LLM_CONFIG(self) -> Dict[str, Any]:
        """LLM configuration dictionary."""
        return {
            "providers": {
                "primary": {
                    "provider": "openai",
                    "model": "gpt-4-turbo-preview",
                    "temperature": 0.1,
                    "max_tokens": 4000,
                    "api_key": self.OPENAI_API_KEY,
                },
                "fallback": [
                    {
                        "provider": "anthropic",
                        "model": "claude-3-sonnet-20240229",
                        "temperature": 0.1,
                        "max_tokens": 4000,
                        "api_key": self.ANTHROPIC_API_KEY,
                    }
                ],
                "specialized": {
                    "sql_generation": {
                        "provider": "openai",
                        "model": "gpt-4",
                        "temperature": 0.0,
                        "api_key": self.OPENAI_API_KEY,
                    },
                    "ui_generation": {
                        "provider": "anthropic",
                        "model": "claude-3-sonnet-20240229",
                        "temperature": 0.7,
                        "api_key": self.ANTHROPIC_API_KEY,
                    },
                },
            },
            "agent_config": {
                "max_iterations": 10,
                "parallel_agents": 5,
                "timeout_seconds": 30,
            },
        }


settings = Settings()
