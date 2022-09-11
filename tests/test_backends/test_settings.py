from progress_updater.backends import Settings
from progress_updater.backends.sql import SQLSettings, SQLLog
from progress_updater.backends.mongo import MongoSettings, MongoLog
from progress_updater.backends.redis import RedisSettings, RedisLog


# passing params
def test_create_settings_passing_params_redis():

    redis_settings = RedisSettings(redis_password="pass", redis_host="redis")
    settings = Settings(pu=redis_settings)
    klass = settings.backend()
    assert issubclass(klass, RedisLog)
    assert klass.Meta.redis_password == RedisLog.Meta.redis_password == "pass"


def test_create_settings_passing_params_mongo():

    mongo_settings = MongoSettings(
        mongo_connection="mongodb://user:pass@mongo:27017",
        mongo_db="db",
        mongo_collection="logs",
    )
    settings = Settings(pu=mongo_settings)
    klass = settings.backend()
    assert issubclass(klass, MongoLog)
    assert (
        klass.Meta.mongo_connection
        == MongoLog.Meta.mongo_connection
        == "mongodb://user:pass@mongo:27017"
    )


def test_create_settings_passing_params_sql():

    sql_settings = SQLSettings(
        sql_dsn="postgresql+psycopg2://user:pass@postgres:5432/db",
        sql_table="logs",
    )
    settings = Settings(pu=sql_settings)
    klass = settings.backend()
    assert issubclass(klass, SQLLog)
    assert (
        klass.Meta.sql_dsn
        == SQLLog.Meta.sql_dsn
        == "postgresql+psycopg2://user:pass@postgres:5432/db"
    )


# env vars
def test_create_settings_env_vars_redis(env_vars_redis):
    settings = Settings()
    klass = settings.backend()
    assert klass == RedisLog
    assert klass.Meta.redis_password == RedisLog.Meta.redis_password == "pass"


def test_create_settings_env_vars_mongo(env_vars_mongo):
    settings = Settings()
    klass = settings.backend()
    assert klass == MongoLog
    assert (
        klass.Meta.mongo_connection
        == MongoLog.Meta.mongo_connection
        == "mongodb://user:pass@mongo:27017"
    )


def test_create_settings_env_vars_sql(env_vars_sql):
    settings = Settings()
    klass = settings.backend()
    assert klass == SQLLog
    assert (
        klass.Meta.sql_dsn
        == SQLLog.Meta.sql_dsn
        == "postgresql+psycopg2://user:pass@postgres:5432/db"
    )
