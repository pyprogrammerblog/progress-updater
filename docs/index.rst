.. progress-updater documentation master file, created by
   sphinx-quickstart on Tue Aug  9 09:38:22 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
.. _index:

Welcome to progress-updater' documentation!
=============================================

Writing the progress of a task to a backend!

Installation
---------------

Install it using `pip`::

   pip install progress-updater

Basic usage
---------------

Make sure you have the `progress-updater` installed::

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


The output is::

   - Task: My task

   - Entering First part
     doing first block...
       Time spent: 0h0m
       Successfully completed

   - Entering Second part
     doing second block...
       Time spent: 0h0m
       Successfully completed

Backends
-------------------
The available backends to store logs are **Mongo**, **Redis** and **SQL**.

Setting your backend with environment variables
---------------------------------------------------
You can set your backend by defining env vars.
The `PU__` prefix indicates that it belongs to `ProgressUpdater`::

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


And then when creating a `ProgressUpdater` object, the backend will be
automatically configured::

   from progress_updater import ProgressUpdater

   with ProgressUpdater(task_name="My Task") as updater:
       pass

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   updater
   settings
   sql
   mongo
   redis
   license
   help


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
