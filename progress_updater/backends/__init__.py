from pydantic import BaseSettings
from typing import Union
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
    **Backends**
    There are three backends available to save our logs.

    1. **Mongo**. `MongoSettings`. Parameters are:
        - mongo_connection: str. Connection string
        - mongo_db:m str. DB Name
        - mongo_collection: str. Collection name.
        - mongo_extras: dict. See extra arguments in Pymongo.

    2. **Redis**. `RedisSettings`. Parameters are:
        - sql_dsn: str. SQLAlchemy connection string.
        - sql_table:m str. SQL Table Name.
        - sql_extras: dict. See extra arguments for SQLAlchemy.

    3. **SQL**. `SQLSettings`. Parameters are:
        - redis_host. str.
        - redis_port. int.
        - redis_db. int.
        - redis_password. str.
        - redis_extras. dict.

    **Settings.**
    Different ways to pass settings to the `Settings` with
    priority order.

    **1. Passing settings** as parameters when creating a `ProgressUpdater`
    object:

        >>> from progress_updater import ProgressUpdater
        >>> from progress_updater.backends import MongoSettings
        >>>
        >>> mongo_settings = MongoSettings(
        >>>     mongo_connection="mongodb://user:pass@mongo:27017",
        >>>     mongo_db="db",
        >>>     mongo_collection="logs",
        >>> )
        >>> settings = Settings(pu=mongo_settings)
        >>> MongoLog = settings.backend()

    **2. Environment variables**. Set you setting parameters in your
    environment. The `PU__` prefix indicates that belongs to the
    `ProgressUpdater` settings. The `ProgressUpdater` will catch
    these settings if the option `write_on_backend` is set to `True`.

    Examples:

    SQL::

        PU__SQL_DSN='postgresql+psycopg2://user:pass@postgres:5432/db'
        PU__SQL_TABLE='logs'

    Redis::

        PU__REDIS_HOST='redis'
        PU__REDIS_DB='1'
        PU__REDIS_PASSWORD='pass'

    Mongo::

        PU__MONGO_CONNECTION='mongodb://user:pass@mongo:27017'
        PU__MONGO_DB='db'
        PU__MONGO_COLLECTION='logs'

    And then when creating a `ProgressUpdater` object, the backend will be
    automatically configured::

        >>> from progress_updater import ProgressUpdater
        >>> from progress_updater.backends import Settings
        >>>
        >>> updater = ProgressUpdater(task_name="My Task")
        >>> isinstance(updater.settings, Settings)
    """

    pu: Union[RedisSettings, MongoSettings, SQLSettings]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"

    def backend(self):
        """
        Return a Backend with configuration already set
        """
        return self.pu.backend()
