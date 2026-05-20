"""
Configuration module with Pydantic validation.
Handles all environment variables, constants, and configuration.
"""

from typing import Dict

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Application configuration with validation."""

    # Telegram
    telegram_bot_token: str
    telegram_payment_provider_token: str = ""

    # OpenRouter API
    openrouter_api_key: str
    openrouter_url: str = "https://openrouter.ai/api/v1"
    openrouter_timeout: int = 60

    # Database
    database_path: str = "users.db"

    # Models
    available_models: Dict[str, str] = {
        "gpt4o": "openai/gpt-4o",
        "gpt41": "openai/gpt-4.1-turbo-preview",
        "claude_sonnet": "anthropic/claude-3.5-sonnet",
        "free": "openai/gpt-oss-120b:free",
    }
    default_model: str = "free"

    # Payment
    stars_per_package: Dict[str, int] = {
        "small": 10,
        "medium": 50,
        "large": 100,
    }
    questions_per_star: int = 10
    questions_per_package: Dict[str, int] = {
        "small": 100,
        "medium": 500,
        "large": 1000,
    }

    # Telegram message limits
    message_char_limit: int = 4096
    caption_char_limit: int = 1024

    # Logging
    log_level: str = "INFO"

    # API Retry
    max_retries: int = 3
    retry_delay: float = 1.0

    # Rate limiting (per user)
    rate_limit_questions: int = 10  # questions per minute
    rate_limit_callbacks: int = 5  # callback clicks per second
    rate_limit_window: int = 60  # seconds

    # Typing action refresh
    typing_refresh_interval: int = 4  # seconds
    typing_max_duration: int = 120  # max seconds before timeout

    # Request timeout
    ai_request_timeout: int = 120  # seconds for AI requests

    # Input validation
    max_prompt_length: int = 4000
    min_prompt_length: int = 1

    class Config:
        """Pydantic config."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def get_model_by_key(self, model_key: str) -> str:
        """
        Get model name by key.

        Args:
            model_key: Model identifier key

        Returns:
            Full model name from OpenRouter

        Raises:
            ValueError: If model key is invalid
        """
        if model_key not in self.available_models:
            raise ValueError(
                f"Invalid model '{model_key}'. "
                f"Available: {', '.join(self.available_models.keys())}"
            )
        return self.available_models[model_key]

    def get_questions_for_package(self, package: str) -> int:
        """Get questions count for a package."""
        return self.questions_per_package.get(package, 0)

    def get_stars_for_package(self, package: str) -> int:
        """Get stars count for a package."""
        return self.stars_per_package.get(package, 0)


# Global config instance with validation
try:
    config = Config()
except Exception as e:
    raise RuntimeError(f"Failed to load configuration: {e}") from e

