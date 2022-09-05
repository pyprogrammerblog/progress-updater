import datetime
from uuid import UUID, uuid4
from progress_updater.backends import Config
from progress_updater.backends.mongo import MongoConfig
from progress_updater.backends.redis import RedisConfig
from progress_updater.backends.sql import SQLConfig
from typing import Tuple, Optional, NoReturn


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
        config: MongoConfig | RedisConfig | SQLConfig = None,
    ):
        self.uuid: UUID = uuid or uuid4()
        self.task_name: str = task_name
        self.verbose: bool = verbose
        self.exception: Optional[Tuple] = None
        self.suppress_exception: bool = suppress_exception

        config = config or Config()
        self.log = config.backend()(uuid=uuid, task_name=task_name)

    def __enter__(self, task_name: str = None):
        self.task_name = task_name or "..."
        self.start_t, self.end_t = datetime.datetime.utcnow(), None
        self.notify(f"- Entering {self.task_name}")
        self.log.save()

    def __exit__(self, exc_type, exc_val, exc_tb):
        td = self.end_t - self.start_t
        hours, minutes = td.seconds // 3600, td.seconds // 60 % 60
        self.notify(f"\tTime spent: {hours}h{minutes}m")
        if exc_type:
            self.notify("\tFailed")
            self.notify(f"\tError message: {exc_type}: {exc_val}")
            self.exception = (exc_type, exc_val, exc_tb)
        else:
            self.notify("\tSuccessfully completed")
        self.log.save()
        return self.suppress_exception

    def __call__(self, **kwargs) -> "ProgressUpdater":
        self.__dict__.update(kwargs)
        return self

    def raise_latest_exception(self) -> NoReturn | Exception:
        if self.exception:
            exc_type, exc_val, exc_tb = self.exception
            raise exc_type(exc_val).with_traceback(exc_tb)

    def notify(self, message: str):
        msg = "\t" + message
        self.log.log += f"{message}\n"
        self.log.save()

        if self.verbose:
            print(msg)
