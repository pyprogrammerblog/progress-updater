from pydantic import BaseSettings
from updater.backends.redis import RedisSettings
from updater.backends.mongo import MongoSettings
from updater.backends.sql import SQLSettings


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
