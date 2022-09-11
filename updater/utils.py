import functools
from updater.updater import ProgressUpdater
from updater.backends.mongo import MongoSettings
from updater.backends.redis import RedisSettings
from updater.backends.sql import SQLSettings


def progress_updater(
    task_name: str = None,
    verbose: bool = True,
    suppress_exception: bool = True,
    raise_latest_exception: bool = True,
    write_on_backend: bool = True,
    settings: MongoSettings | RedisSettings | SQLSettings = None,
):
    """
    Progress Updater Decorator. Defines the Progress Updater as decorator

    Basic example:
        >>> from updater.utils import progress_updater
        >>>
        >>> @progress_updater
        >>> def task():
        >>>     return "Hello World"
        >>>
        >>> task()

    Advance example
        >>> from updater.utils import progress_updater
        >>> from updater.backends import MongoSettings
        >>>
        >>> @progress_updater(
        >>>     task_name="My task",
        >>>     suppress_exception=False,
        >>>     settings = MongoSettings(
        >>>         mongo_connection="mongodb://user:pass@mongo:27017",
        >>>         mongo_db="db",
        >>>         mongo_collection="logs",
        >>>     )
        >>> )
        >>> def task():
        >>>     return "Hello World"
        >>>
        >>> task()
    """

    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            with ProgressUpdater(
                task_name=task_name or func.__name__,
                suppress_exception=suppress_exception,
                write_on_backend=write_on_backend,
                verbose=verbose,
                settings=settings,
            ) as task_updater:
                func(*args, **kwargs)

            if raise_latest_exception:
                task_updater.raise_latest_exception()

        return inner

    return decorator
