.. _backends:

Backends
=====================


:mod:`Settings`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: progress_updater.backends
    :members: Settings
    :exclude-members: Config, backend


:mod:`Mongo`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: progress_updater.backends.mongo
    :members: MongoLog, MongoSettings
    :exclude-members: mongo_collection, backend


:mod:`Redis`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: progress_updater.backends.redis
    :members: RedisLog, RedisSettings
    :exclude-members: redis_connection, backend


:mod:`SQL`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: progress_updater.backends.sql
    :members: SQLLog, SQLSettings
    :exclude-members: sql_session, backend


:mod:`Base Log`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: progress_updater.backends.log
    :members: Log, Logs
    :exclude-members:
