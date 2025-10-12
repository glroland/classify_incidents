""" Configuration Management for application. """
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

# Load environment variables
try:
    load_dotenv()
except Exception:   # pylint: disable=broad-except
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

    # ServiceNow Configuration
    SERVICE_NOW_INSTANCE: str = Field(
        default=None,
        json_schema_extra={
            "env": "SERVICE_NOW_INSTANCE",
            "description": "Service Now Instance ID",
        },
    )
    SERVICE_NOW_USERNAME: str = Field(
        default=None,
        json_schema_extra={
            "env": "SERVICE_NOW_USERNAME",
            "description": "Service Now Username",
        },
    )
    SERVICE_NOW_PASSWORD: str = Field(
        default=None,
        json_schema_extra={
            "env": "SERVICE_NOW_PASSWORD",
            "description": "Service Now Password",
        },
    )
    SERVICE_NOW_TIMEOUT: str = Field(
        default=60,
        json_schema_extra={
            "env": "SERVICE_NOW_TIMEOUT",
            "description": "Service Now Request Timeout",
        },
    )

settings = Settings()
