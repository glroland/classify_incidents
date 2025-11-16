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

    # MCP Servers
    AUTOMATE_AGENT_URL: str = Field(
        default="",
        json_schema_extra={
            "env": "AUTOMATE_AGENT_URL",
            "description": "Automation Agent URL",
        },
    )

    # ServiceNow Configuration
    SERVICE_NOW_INSTANCE: str = Field(
        default="",
        json_schema_extra={
            "env": "SERVICE_NOW_INSTANCE",
            "description": "Service Now Instance ID",
        },
    )
    SERVICE_NOW_USERNAME: str = Field(
        default="",
        json_schema_extra={
            "env": "SERVICE_NOW_USERNAME",
            "description": "Service Now Username",
        },
    )
    SERVICE_NOW_PASSWORD: str = Field(
        default="",
        json_schema_extra={
            "env": "SERVICE_NOW_PASSWORD",
            "description": "Service Now Password",
        },
    )

    # API Timeout
    API_TIMEOUT: int = Field(
        default=60,
        json_schema_extra={
            "env": "API_TIMEOUT",
            "description": "REST API Request Timeout",
        },
    )

    # prompt source location
    PROMPTS_LOCATION: str = Field(
        default="./prompts/",
        json_schema_extra={
            "env": "PROMPTS_LOCATION",
            "description": "Location where prompts are stored",
        },
    )

    # object storage connection info
    OBJECT_STORAGE_URL: str = Field(
        default="",
        json_schema_extra={
            "env": "OBJECT_STORAGE_URL",
            "description": "Object Storage URL",
        },
    )
    OBJECT_STORAGE_ACCESS_KEY: str = Field(
        default="",
        json_schema_extra={
            "env": "OBJECT_STORAGE_ACCESS_KEY",
            "description": "Object Storage Access Key",
        },
    )
    OBJECT_STORAGE_SECRET_KEY: str = Field(
        default="",
        json_schema_extra={
            "env": "OBJECT_STORAGE_SECRET_KEY",
            "description": "Object Storage Secret Key",
        },
    )
    OBJECT_STORAGE_BUCKET: str = Field(
        default="",
        json_schema_extra={
            "env": "OBJECT_STORAGE_BUCKET",
            "description": "Object Storage Bucket (i.e. Working Directory)",
        },
    )

settings = Settings()
