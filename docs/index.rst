.. progress-updater documentation master file, created by
   sphinx-quickstart on Tue Aug  9 09:38:22 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
.. _index:

Welcome to progress-updater' documentation!
=============================================


Basic usage
-------------

Make sure you had install the package by doing ``pip install progress-updater`` and then::

   from updater import ProgressUpdater

   # create an updater object
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


Backends
----------
There are three backends available to save our logs.

1. Mongo.
2. Redis.
3. SQL.


Settings
----------

There are some possible ways to pass settings to the updater.
This is the priority.

1. Passing settings as parameters when creating a `ProgressUpdater` object.
Example ::

   from updater import ProgressUpdater
   from updater.backends.mongo import MongoSettings

   settings = MongoSettings(
       mongo_connection="mongodb://user:pass@mongo:27017",
       mongo_db="db",
       mongo_collection="logs",
   )
   with ProgressUpdater(task_name="My Task", settings=settings) as updater:
       pass

2. Environment variables. The `PU__` prefix indicates that it belongs to `ProgressUpdater`.
Example::

   export PU__SQL_DSN='postgresql+psycopg2://user:pass@postgres:5432/db'
   export PU__SQL_TABLE='logs'


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
