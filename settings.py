from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Anthropic API configuration
    anthropic_api_key: str
    anthropic_model: str = "claude-3-haiku-20240307"  # Lightweight model for renaming

    # Download configuration
    output_dir: str = r"D:\reel-slicer\data\videos"
    videos_file: str = "videos.txt"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


# Global settings instance
settings = Settings()
