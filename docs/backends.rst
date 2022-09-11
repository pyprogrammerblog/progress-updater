.. _backends:

Backends
=====================


:mod:`Settings`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: updater.backends
    :members: Settings
    :exclude-members: Config, backend


:mod:`Mongo`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: updater.backends.mongo
    :members: MongoLog, MongoSettings
    :exclude-members: mongo_collection, backend


:mod:`Redis`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: updater.backends.redis
    :members: RedisLog, RedisSettings
    :exclude-members: redis_connection, backend


:mod:`SQL`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: updater.backends.sql
    :members: SQLLog, SQLSettings
    :exclude-members: sql_session, backend


:mod:`Log`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: updater.backends.log
    :members: Log, Logs
    :exclude-members:
