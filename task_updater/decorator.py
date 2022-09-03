import functools
from task_updater.updater import ProgressUpdater


def task_updater(
    task_name: str = None,
    verbose: bool = True,
    suppress_exception: bool = True,
):
    """
    Task Updater Decorator
    """

    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            with ProgressUpdater(
                task_name=task_name or func.name,
                suppress_exception=suppress_exception,
                verbose=verbose,
            ) as task_updater:
                func(*args, **kwargs)
            task_updater.raise_latest_exception()

        return inner

    return decorator
