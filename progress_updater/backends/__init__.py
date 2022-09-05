from pydantic import BaseSettings
from progress_updater.backends.redis import RedisConfig
from progress_updater.backends.mongo import MongoConfig
from progress_updater.backends.sql import SQLConfig


class BaseConfig(BaseSettings):
    """
    Base Config
    """

    def backend(self):
        """
        Return the backend Log class
        """
        raise NotImplementedError


class Config(BaseConfig):
    """
    Config
    """

    updater: RedisConfig | MongoConfig | SQLConfig

    class Config:
        env_file = ".env", ".env.prod"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"

    def backend(self):
        return self.updater.backend()
