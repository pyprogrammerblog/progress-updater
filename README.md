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
pip install progress-progress_updater
```

Basic usage
-------------

```python
from progress_updater import ProgressUpdater

# create an progress_updater object
updater = ProgressUpdater(task_name="My Task")

with updater(block_name="First part") as updater:
    # doing things
    updater.notify("doing first block...")
    # doing more things

with updater(block_name="Second part"):
    # doing things
    updater.notify("doing second block...")
    # doing more things

updater.raise_latest_exception()
```

Backends
----------
There are three backends available to save our logs.

1. Mongo. See [documentation]().
2. Redis. See [documentation]().
3. SQL. See [documentation]().


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
    ...
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
