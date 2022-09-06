import functools
from updater.updater import ProgressUpdater
from updater.backends.mongo import MongoSettings
from updater.backends.redis import RedisSettings
from updater.backends.sql import SQLSettings


def progress_updater(
    settings: MongoSettings | RedisSettings | SQLSettings = None,
    task_name: str = None,
    verbose: bool = True,
    suppress_exception: bool = True,
):
    """
    Task Updater Decorator

    >>> from updater.utils import progress_updater
    >>>
    >>> @progress_updater
    >>> def task():
    >>>     return "Hello World"
    >>>
    >>> task()
    """

    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            with ProgressUpdater(
                task_name=task_name or func.name,
                suppress_exception=suppress_exception,
                verbose=verbose,
                settings=settings,
            ) as task_updater:
                func(*args, **kwargs)
            task_updater.raise_latest_exception()

        return inner

    return decorator
