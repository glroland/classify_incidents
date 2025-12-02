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

    # MCP Server Network Config
    SERVER_ADDRESS: str = Field(
        default="0.0.0.0",
        json_schema_extra={
            "env": "SERVER_ADDRESS",
            "description": "Listen To Address for MCP Server",
            "example": "0.0.0.0",
        },
    )
    SERVER_PORT: int = Field(
        default=8080,
        json_schema_extra={
            "env": "SERVER_PORT",
            "description": "MCP Server Listen To Port",
            "example": "8080",
        },
    )
    NUM_WORKERS: int = Field(
        default=0,
        json_schema_extra={
            "env": "NUM_WORKERS",
            "description": "Number of Workers",
            "example": "0 for ignore,10",
        },
    )

    # Logging Config
    LOG_LEVEL: str = Field(
        default="info",
        json_schema_extra={
            "env": "LOG_LEVEL",
            "description": "Logging Level for Server",
            "example": "info,debug",
        },
    )

    # Knowledge Config
    KNOWLEDGE_ENVIRONMENT_URL: str = Field(
        default="https://raw.githubusercontent.com/glroland/automate-it/refs/heads/main/knowledge/",
        json_schema_extra={
            "env": "KNOWLEDGE_ENVIRONMENT_URL",
            "description": "Environmental Metadata URL",
        },
    )

    # OpenAI API Endpoint
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

    # Model Configuration
    PLANNING_MODEL: str = Field(
        default="openai/gpt-5",
        json_schema_extra={
            "env": "PLANNING_MODEL",
            "description": "Planning Model",
        },
    )
    JUDGE_PLAN_MODEL: str = Field(
        default="anthropic/claude-3-7-sonnet-20250219",
        json_schema_extra={
            "env": "JUDGE_PLAN_MODEL",
            "description": "Model to Judge Plan",
        },
    )
    CODING_MODEL: str = Field(
        default="anthropic/claude-3-7-sonnet-20250219",
        json_schema_extra={
            "env": "CODING_MODEL",
            "description": "Coding Model",
        },
    )

    # working directory for various tools, like ansible-lint
    WORK_DIR: str = Field(
        default="/tmp",
        json_schema_extra={
            "env": "WORK_DIR",
            "description": "Working Directory for Temp Files",
        },
    )

settings = Settings()
