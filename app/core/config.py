from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """
    Application settings loaded from the .env file.
    """
    # Database Configuration
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    # Azure OpenAI Configuration
    AZURE_OPENAI_API_KEY: str = Field(..., env="AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_API_BASE: str = Field(..., env="AZURE_OPENAI_API_BASE")
    AZURE_OPENAI_API_VERSION: str = Field(..., env="AZURE_OPENAI_API_VERSION")
    AZURE_OPENAI_DEPLOYMENT_NAME: str = Field(..., env="AZURE_OPENAI_DEPLOYMENT_NAME")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create a single instance of the settings to be imported across the application
settings = Settings()