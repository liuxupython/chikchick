from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .database import DatabaseConfig
from .redis import RedisConfig


class DeploymentConfig(BaseSettings):
    """
    Configuration settings for application deployment
    """

    APPLICATION_NAME: str = Field(
        description="Name of the application, used for identification and logging purposes",
        default="langgenius/dify",
    )

    DEBUG: bool = Field(
        description="Enable debug mode for additional logging and development features",
        default=False,
    )

    TESTING: bool = Field(
        description="Enable testing mode for running automated tests",
        default=False,
    )

    EDITION: str = Field(
        description="Deployment edition of the application (e.g., 'SELF_HOSTED', 'CLOUD')",
        default="SELF_HOSTED",
    )

    DEPLOY_ENV: str = Field(
        description="Deployment environment (e.g., 'PRODUCTION', 'DEVELOPMENT'), default to PRODUCTION",
        default="PRODUCTION",
    )
    PORT: int = Field(
        description="Port number for the application to listen on",
        default=5000,
    )


class AppConfig(
    DeploymentConfig,
    DatabaseConfig,
    RedisConfig,
):
    """
    Application configs
    """

    SECRET_KEY: str = Field(
        description="Secret key for application security",
        default="",
    )

    model_config = SettingsConfigDict(
        # read from dotenv format config file
        env_file=".env",
        env_file_encoding="utf-8",
        frozen=True,
        # ignore extra attributes
        extra="ignore",
    )
