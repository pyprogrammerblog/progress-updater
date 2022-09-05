 tiny-blocks
=============

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

updater = ProgressUpdater(task_name="My Task")

with updater(task_name="First part") as updater:
    # doing things
    updater.notify("doing first part...")
    # doing more things

with updater(task_name="Second part"):
    # doing things
    updater.notify("doing second part...")
    # doing more things

updater.raise_latest_exception()
```

Settings
----------

There are three ways to passing settings to the updater.

1. Passing settings as parameters when creating a ```ProgressUpdater``` object.
2. Environment variables
3. Env file (~/.env)


Documentation
--------------

Please visit this [link](https://tiny-blocks.readthedocs.io/en/latest/) for documentation.
