import os

import yaml
from pydantic import BaseSettings, BaseModel


def yaml_config_settings_source(settings: BaseSettings):
    """
    Custom settings source that reads the settings from a YAML file.
    """
    path = os.getenv("CONFIG_PATH", "config.yaml")
    with open(path, "r") as fh:
        return yaml.safe_load(fh)


class ConverterOptions(BaseModel):
    """
    Converter options.

    Attributes
    ----------
    author_rewrite : str
        Will rewrite the author to this value for all the posts.
    links_rewrite : list[dict]
        Will rewrite the links to this value for all the posts.
    """

    author_rewrite: str
    links_rewrite: list[dict]


class Configurator(BaseSettings):
    """
    Configurator class for the app.

    Attributes
    ----------
    logging_level: str
        The logging level.
    source_path : str
        The path to the Jekyll posts.
    output_path : str
        The path to the Hugo posts.
    converter : str
        The converter that converts the markdown
    """

    logging_level: str = "INFO"
    source_path: str
    output_path: str
    converter: str
    converter_options: ConverterOptions

    class Config:
        env_file_encoding = "utf-8"

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (yaml_config_settings_source,)
