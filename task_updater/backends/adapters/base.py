import logging


logger = logging.getLogger(__name__)


class TasksBackend:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        pass

    def get_(self):
        pass
