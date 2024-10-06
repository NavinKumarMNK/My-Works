from typing import Type
from pydantic_settings import (
    PydanticBaseSettingsSource,
    BaseSettings as PydanticBaseSettings,
    SettingsConfigDict as PydanticSettingsConfigDict,
    YamlConfigSettingsSource as PydanticYamlConfigSettingsSource,
    TomlConfigSettingsSource as PydanticTomlConfigSettingsSource,
)
from pydantic import BaseModel


class AppConfigModel(BaseModel):
    version: str
    description: str
    license_info: dict
    contact: dict

class AppConfig(PydanticBaseSettings):
    app: AppConfigModel

    model_config = PydanticSettingsConfigDict(
        yaml_file="config.yaml",
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[PydanticBaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (PydanticYamlConfigSettingsSource(settings_cls),)


class ProjectConfigModel(BaseModel):
    name: str
    version: str
    description: str
    license: str
    authors: list[dict]


class ProjectConfig(PydanticBaseSettings):
    project: ProjectConfigModel

    model_config = PydanticSettingsConfigDict(
        toml_file="pyproject.toml",
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[PydanticBaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (PydanticTomlConfigSettingsSource(settings_cls),)


class EnvConfig(PydanticBaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_MAXAGE: int

    model_config = PydanticSettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


APP_CONFIG = AppConfig()
PROJECT_CONFIG = ProjectConfig()
ENV_CONFIG = EnvConfig()