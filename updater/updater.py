import datetime
from uuid import UUID, uuid4
from updater.backends import Settings
from updater.backends.mongo import MongoSettings
from updater.backends.redis import RedisSettings
from updater.backends.sql import SQLSettings
from typing import Tuple, Optional


class ProgressUpdater:
    """
    Task Updater
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
        settings: MongoSettings | RedisSettings | SQLSettings = None,
    ):
        self.uuid: UUID = uuid or uuid4()
        self.task_name: str = task_name.capitalize()
        self.verbose: bool = verbose
        self.exception: Optional[Tuple] = None
        self.suppress_exception: bool = suppress_exception
        self.write_on_backend: bool = write_on_backend

        if write_on_backend:
            settings = settings or Settings()
            self.log = settings.backend()(uuid=uuid, task_name=task_name)

    def __enter__(self, block_name: str = None) -> "ProgressUpdater":
        self.block_name = block_name or "..."
        self.start_t = datetime.datetime.utcnow()
        self.notify(f"- Entering {self.block_name}")
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
        if self.exception:
            exc_type, exc_val, exc_tb = self.exception
            raise exc_type(exc_val).with_traceback(exc_tb)

    def notify(self, message: str):
        msg = "\t" + message

        if self.write_on_backend:
            self.log.log += f"{message}\n"
            self.log.save()

        if self.verbose:
            print(msg)
