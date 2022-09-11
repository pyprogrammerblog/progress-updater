progress-updater
=================

[![Documentation Status](https://readthedocs.org/projects/progress-updater/badge/?version=latest)](https://progress-updater.readthedocs.io/en/latest/?badge=latest)
[![License-MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/pyprogrammerblog/progress-updater/blob/master/LICENSE)
[![GitHub Actions](https://github.com/pyprogrammerblog/progress-updater/workflows/CI/badge.svg/)](https://github.com/pyprogrammerblog/progress-updater/workflows/CI/badge.svg/)
[![PyPI version](https://badge.fury.io/py/progress-updater.svg)](https://badge.fury.io/py/progress-updater)

Writing the progress of a task to a backend!

Installation
-------------

Install it using ``pip``

```shell
pip install progress-updater
```

Basic usage
-------------

```python
from progress_updater import ProgressUpdater

updater = ProgressUpdater(task_name="My Task")

with updater(block_name="First part"):
    # doing things
    updater.notify("doing first block...")
    # doing more things

with updater(block_name="Second part"):
    # doing things
    updater.notify("doing second block...")
    # doing more things

updater.raise_latest_exception()  # if exists
```

The output is:
```shell
- Task: My task

- Entering First part
  doing first block...
	Time spent: 0h0m
	Successfully completed

- Entering Second part
  doing second block...
	Time spent: 0h0m
	Successfully completed
```

Backends
----------
If you want to save the output in a Database you will need to define 
a backend. There are three backends available to save our logs.

1. Mongo.
2. Redis.
3. SQL.

```python
from progress_updater.backends import MongoLog
from uuid import UUID

log = MongoLog.get(uuid=UUID("<your task uuid>"))
assert log.status == "SUCCESS"
```


Settings
----------

There are some possible ways to pass settings to the updater. 
This is the priority.

1. Passing settings as parameters when creating a `ProgressUpdater` object.

```python
from progress_updater import ProgressUpdater
from progress_updater.backends.mongo import MongoSettings

settings = MongoSettings(
    mongo_connection="mongodb://user:pass@mongo:27017",
    mongo_db="db",
    mongo_collection="logs",
)

with ProgressUpdater(task_name="My Task", settings=settings) as updater:
    pass
```

2. Environment variables.

The `PU__` prefix indicates that it belongs to `ProgressUpdater`.
```shell
export PU__SQL_DSN=postgresql+psycopg2://user:pass@postgres:5432/db
export PU__SQL_TABLE=logs
```


Documentation
--------------

Please visit this [link](https://progress-updater.readthedocs.io/en/latest/) for documentation.
