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
from progress_updater.backends.mongo import MongoSettings

settings = MongoSettings(
    mongo_connection="mongodb://user:pass@mongo:27017",
    mongo_db="db",
    mongo_collection="logs",
)

updater = ProgressUpdater(task_name="My Task", settings=settings)

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
-------------------
The available backends to store logs are **Mongo**, **Redis** and **SQL**.
Please read the [docs](https://progress-updater.readthedocs.io/en/latest/) 
for further information.

Environment variables
-----------------------
You can set your backend by defining env vars.
The `PU__` prefix indicates that it belongs to `ProgressUpdater`.
```shell
# SQL
PU__SQL_DSN='postgresql+psycopg2://user:pass@postgres:5432/db'
PU__SQL_TABLE='logs'
...
# Redis
PU__REDIS_HOST='redis'
PU__REDIS_DB='1'
PU__REDIS_PASSWORD='pass'
...
# Mongo
PU__MONGO_CONNECTION='mongodb://user:pass@mongo:27017'
PU__MONGO_DB='db'
PU__MONGO_COLLECTION='logs'
...
```

And then when creating a `ProgressUpdater` object, the backend will be 
automatically configured.
```python
from progress_updater import ProgressUpdater

with ProgressUpdater(task_name="My Task") as updater:
    pass
```

Documentation
--------------

Please visit this [link](https://progress-updater.readthedocs.io/en/latest/) for documentation.
