.. progress-updater documentation master file, created by
   sphinx-quickstart on Tue Aug  9 09:38:22 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
.. _index:

Welcome to progress-updater' documentation!
=============================================

Writing the progress of a task to a backend!

Installation
-------------

Install it using `pip`::

   pip install progress-updater

Basic usage
-------------

Make sure you have the `progress-updater` installed::

   from progress_updater import ProgressUpdater

   updater = ProgressUpdater(task_name="My Task", write_on_backend=False, verbose=True)

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
----------
If you want to save the output in a Database you will need to define
a backend. There are three backends available to save our logs.

1. Mongo.
2. Redis.
3. SQL.

In you console, for example::

   from progress_updater.backends import MongoLog
   from uuid import UUID

   log = MongoLog.get(uuid=UUID("<your task uuid>"))
   assert log.status == "SUCCESS"


There are some possible ways to pass backend settings to the updater.
This is the priority.

1. Passing settings as parameters when creating a `ProgressUpdater` object::

   from progress_updater import ProgressUpdater
   from progress_updater.backends.mongo import MongoSettings

   settings = MongoSettings(
       mongo_connection="mongodb://user:pass@mongo:27017",
       mongo_db="db",
       mongo_collection="logs",
   )

   with ProgressUpdater(task_name="My Task", settings=settings) as updater:
       pass

2. Environment variables::
The `PU__` prefix indicates that it belongs to `ProgressUpdater`::

   export PU__SQL_DSN=postgresql+psycopg2://user:pass@postgres:5432/db
   export PU__SQL_TABLE=logs

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
   backends
   license
   help


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
