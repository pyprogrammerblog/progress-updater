import datetime
from uuid import UUID, uuid4
from task_updater.backends.log import Log
from typing import Tuple, Optional


class Updater:
    """
    Task Updater
    """
    FAIL = "FAIL"
    COMPLETED = "SUCCESS"
    PENDING = "PENDING"

    def __init__(self, task_name: str, uuid: UUID = None, suppress_exception: bool = True, verbose: bool = True):
        self.uuid: UUID = uuid or uuid4()
        self.task_name: str = task_name
        self.verbose: bool = verbose
        self.exception: Optional[Tuple] = None
        self.suppress_exception: bool = suppress_exception
        self.log = Log(uuid=uuid, task_name=task_name)

    def __enter__(self, name: str = None):
        self.task_name = name or self.task_name
        self.start_t, self.end_t = datetime.datetime.utcnow(), None
        self.notify(' - ' + self.task_name)
        self.log.save()

    def __exit__(self, exc_type, exc_val, exc_tb):
        td = self.end_t - self.start_t
        hours, minutes = td.seconds // 3600, td.seconds // 60 % 60
        self.notify(f"\tTime spent: {hours}h{minutes}m")
        if exc_type:
            self.notify('\tFailed')
            self.notify(f'\tError message: {exc_type}: {exc_val}')
            self.exception = (exc_type, exc_val, exc_tb)
        else:
            self.notify('\tSuccessfully completed')
        self.log.save()
        return self.suppress_exception

    def raise_latest_exception(self):
        if self.exception:
            exc_type, exc_val, exc_tb = self.exception
            raise exc_type(exc_val).with_traceback(exc_tb)

    def notify(self, message):
        msg = '\t' + message
        self.log.log += f"{message}\n"
        self.log.save()

        if self.verbose:
            print(msg)
