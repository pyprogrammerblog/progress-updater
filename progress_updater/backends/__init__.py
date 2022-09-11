from pydantic import BaseSettings
from progress_updater.backends.redis import RedisSettings, RedisLog
from progress_updater.backends.mongo import MongoSettings, MongoLog
from progress_updater.backends.sql import SQLSettings, SQLLog

__all__ = [
    "MongoSettings",
    "RedisSettings",
    "SQLSettings",
    "Settings",
    "RedisLog",
    "MongoLog",
    "SQLLog",
]


class Settings(BaseSettings):
    """
    Config
    """

    pu: RedisSettings | MongoSettings | SQLSettings

    class Config:
        # env_file = "~/.env"
        # env_file_encoding = "utf-8"
        env_nested_delimiter = "__"

    def backend(self):
        return self.pu.backend()
