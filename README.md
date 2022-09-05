progress-updater
=================

[![Documentation Status](https://readthedocs.org/projects/tiny-blocks/badge/?version=latest)](https://tiny-blocks.readthedocs.io/en/latest/?badge=latest)
[![License-MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/pyprogrammerblog/tiny-blocks/blob/master/LICENSE)
[![GitHub Actions](https://github.com/pyprogrammerblog/tiny-blocks/workflows/CI/badge.svg/)](https://github.com/pyprogrammerblog/tiny-blocks/workflows/CI/badge.svg/)
[![PyPI version](https://badge.fury.io/py/tiny-blocks.svg)](https://badge.fury.io/py/tiny-blocks)

Tiny Blocks to build large and complex ETL data pipelines!

Installation
-------------

Install it using ``pip``

```shell
pip install task-updater
```

Basic usage
---------------

```python
from updater import ProgressUpdater

# create an updater object
updater = ProgressUpdater(task_name="My Task")

with updater(block_name="First part") as updater:
    # doing things
    updater.notify("doing first part...")
    # doing more things

with updater(block_name="Second part"):
    # doing things
    updater.notify("doing second part...")
    # doing more things

updater.raise_latest_exception()
```

Settings
----------

There are three possible ways to pass settings to the updater. 
This is the priority.

1. Passing settings as parameters when creating a `ProgressUpdater` object.
```python
from updater import ProgressUpdater
from updater.backends.redis import RedisSettings

redis_settings = RedisSettings(redis_password="pass")

with ProgressUpdater(task_name="My Task", settings=redis_settings) as updater:
    # doing things
    updater.notify("doing things...")
    # doing more things
```
2. Environment variables. 
The `PU__` prefix indicates that it belongs to `ProgressUpdater`.
```shell
export PU__SQL_DSN=postgresql+psycopg2://user:pass@postgres:5432/db
export PU__SQL_TABLE=logs
```

3. Env file (~/.env)
The `PU__` prefix indicates that it belongs to `ProgressUpdater`.
```shell
PU__MONGO_CONNECTION=mongodb://user:pass@mongo:27017
PU__MONGO_DB_NAME=db
PU__MONGO_COLLECTION=logs
```


Documentation
--------------

Please visit this [link](https://tiny-blocks.readthedocs.io/en/latest/) for documentation.
