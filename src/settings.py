import os
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

# Load environment variables
try:
    load_dotenv()
except Exception:
    # Ignore errors for when standard environment variables are being set
    pass

class Settings(BaseSettings):
    """ Classify Incidents Configuration Settings """

    # OpenAI Endpoints
    OPENAI_BASE_URL: str = Field(
        default="http://localhost:11434/v1",
        json_schema_extra={
            "env": "OPENAI_BASE_URL",
            "description": "OpenAI Base URL",
            "example": "http://localhost:11434/v1",
        },
    )
    OPENAI_API_KEY: str = Field(
        default="not_provided",
        json_schema_extra={
            "env": "OPENAI_API_KEY",
            "description": "OpenAI Base URL",
        },
    )
    OPENAI_MODEL: str = Field(
        default="granite4",
        json_schema_extra={
            "env": "OPENAI_MODEL",
            "description": "OpenAI Model Name",
        },
    )

settings = Settings()
