import functools
from updater.updater import ProgressUpdater
from updater.backends.mongo import MongoConfig
from updater.backends.redis import RedisConfig
from updater.backends.sql import SQLConfig


def progress_updater(
    config: MongoConfig | RedisConfig | SQLConfig = None,
    task_name: str = None,
    verbose: bool = True,
    suppress_exception: bool = True,
):
    """
    Task Updater Decorator

    >>> from progress_updater.utils import progress_updater
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
                config=config,
            ) as task_updater:
                func(*args, **kwargs)
            task_updater.raise_latest_exception()

        return inner

    return decorator
