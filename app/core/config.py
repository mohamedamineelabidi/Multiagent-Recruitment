"""
Application Configuration

This module handles all application settings using Pydantic Settings.
Configuration is loaded from environment variables or .env file.

Usage:
    from app.core.config import settings
    print(settings.DATABASE_URL)
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Attributes:
        DATABASE_URL: Database connection string (PostgreSQL or SQLite)
        AZURE_OPENAI_API_KEY: Azure OpenAI API authentication key
        AZURE_OPENAI_API_BASE: Azure OpenAI endpoint URL
        AZURE_OPENAI_API_VERSION: Azure OpenAI API version
        AZURE_OPENAI_DEPLOYMENT_NAME: GPT model deployment name
    """
    
    # Database Configuration
    DATABASE_URL: str = Field(
        ...,
        env="DATABASE_URL",
        description="Database connection URL"
    )

    # Azure OpenAI Configuration
    AZURE_OPENAI_API_KEY: str = Field(
        ...,
        env="AZURE_OPENAI_API_KEY",
        description="Azure OpenAI API Key"
    )
    AZURE_OPENAI_API_BASE: str = Field(
        ...,
        env="AZURE_OPENAI_API_BASE",
        description="Azure OpenAI Endpoint URL"
    )
    AZURE_OPENAI_API_VERSION: str = Field(
        ...,
        env="AZURE_OPENAI_API_VERSION",
        description="Azure OpenAI API Version"
    )
    AZURE_OPENAI_DEPLOYMENT_NAME: str = Field(
        ...,
        env="AZURE_OPENAI_DEPLOYMENT_NAME",
        description="Azure OpenAI Model Deployment Name"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Singleton instance
settings = Settings()