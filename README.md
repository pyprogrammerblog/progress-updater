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
from task_updater import ProgressUpdater

updater = ProgressUpdater(name="Progess Updater")

with updater(task_name="First part"):
    pass

with updater(task_name="Second part"):
    pass

updater.raise_latest_exception()
```

Examples
----------------------

For more complex examples please visit 
the [notebooks' folder](https://github.com/pyprogrammerblog/tiny-blocks/blob/master/notebooks/Examples.ipynb).


Documentation
--------------

Please visit this [link](https://tiny-blocks.readthedocs.io/en/latest/) for documentation.
