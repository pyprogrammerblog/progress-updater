import datetime
import sys
from uuid import UUID, uuid4
from progress_updater.backends import Settings
from progress_updater.backends.mongo import MongoSettings
from progress_updater.backends.redis import RedisSettings
from progress_updater.backends.sql import SQLSettings
from typing import Tuple, Optional, Union


class ProgressUpdater:
    """
    Progress Updater. Defines the Progress Updater Class.

    Example:
        >>> from progress_updater import ProgressUpdater
        >>> from progress_updater.backends import MongoSettings
        >>>
        >>> settings = MongoSettings(
        >>>     mongo_connection="mongodb://user:pass@mongo:27017",
        >>>     mongo_db="db",
        >>>     mongo_collection="logs",
        >>> )
        >>> updater = ProgressUpdater(task_name="My Task", settings=settings)
        >>>
        >>> with updater(block_name="First part") as updater:
        >>>     # doing things
        >>>     updater.notify("doing first block...")
        >>>     # doing more things
        >>>
        >>> with updater(block_name="Second part"):
        >>>     # doing things
        >>>     updater.notify("doing second block...")
        >>>     # doing more things
        >>>
        >>> updater.raise_latest_exception()


    **Backends**
    There are three backends available to save our logs,
    **Mongo**, **Redis** and **SQL**.

    **Settings.**
    Different ways to pass settings to the `ProgressUpdater`.

    **1. Passing settings** as parameters when creating a `ProgressUpdater`
    object like in the above example:

        >>> from progress_updater import ProgressUpdater
        >>> from progress_updater import ProgressUpdater
        >>> from progress_updater.backends import MongoSettings
        >>> from progress_updater.backends import SQLSettings
        >>> from progress_updater.backends import RedisSettings
        >>>
        >>> mongo_settings = MongoSettings(
        >>>     mongo_connection="mongodb://user:pass@mongo:27017",
        >>>     mongo_db="db",
        >>>     mongo_collection="logs",
        >>> )
        >>> sql_settings = SQLSettings(
        >>>     sql_dsn="postgresql+psycopg2://user:pass@postgres:5432/db",
        >>>     sql_table="logs",
        >>> )
        >>> redis_settings = RedisSettings(
        >>>     redis_host="redis", redis_password="pass"
        >>> )


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
        >>> updater = ProgressUpdater(task_name="My Task")
    """

    FAIL = "FAIL"
    COMPLETED = "SUCCESS"
    PENDING = "PENDING"

    def __init__(
        self,
        task_name: str,
        uuid: UUID = None,
        suppress_exception: bool = True,
        verbose: bool = True,
        write_on_backend: bool = True,
        settings: Union[
            MongoSettings, RedisSettings, SQLSettings, None
        ] = None,
    ):
        self.uuid: UUID = uuid or uuid4()
        self.task_name: str = task_name.capitalize()
        self.verbose: bool = verbose
        self.exception: Optional[Tuple] = None
        self.suppress_exception: bool = suppress_exception
        self.write_on_backend: bool = write_on_backend

        if write_on_backend:
            self.settings = settings or Settings()
            self.log = self.settings.backend()(
                uuid=self.uuid, task_name=task_name
            )
            self.log.save()

        self.notify(f"- Task: {self.task_name}")

    def __enter__(self, block_name: str = None) -> "ProgressUpdater":
        self.block_name = self.__dict__.get("block_name") or "..."
        self.start_t = datetime.datetime.utcnow()
        self.notify(f"\n- Entering {self.block_name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        td = datetime.datetime.utcnow() - self.start_t
        hours, minutes = td.seconds // 3600, td.seconds // 60 % 60
        self.notify(f"\tTime spent: {hours}h{minutes}m")
        if exc_type:
            self.notify("\tFailed")
            self.notify(f"\tError message: {exc_type}: {exc_val}")
            self.exception = (exc_type, exc_val, exc_tb)
        else:
            self.notify("\tSuccessfully completed")
        return self.suppress_exception

    def __call__(self, **kwargs) -> "ProgressUpdater":
        self.__dict__.update(kwargs)
        return self

    def raise_latest_exception(self):
        """
        Raise latest exception
        """
        if self.exception:
            exc_type, exc_val, exc_tb = self.exception
            raise exc_type(exc_val).with_traceback(exc_tb)

    def notify(self, message: str):
        """
        Stores a message in the backend. If verbose is set
        to `True`, then the message will be printed.
        """
        msg = f"{message}\n"

        if self.write_on_backend:
            self.log.log += msg
            self.log.save()

        if self.verbose:
            sys.stdout.write(msg)
