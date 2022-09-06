from updater.backends import Settings
from updater.backends.sql import SQLSettings, SQLLog
from updater.backends.mongo import MongoSettings, MongoLog
from updater.backends.redis import RedisSettings, RedisLog


# passing params
def test_create_settings_passing_params_redis():

    redis_settings = RedisSettings(redis_password="pass")
    settings = Settings(pu=redis_settings)
    assert issubclass(settings.backend(), RedisLog)


def test_create_settings_passing_params_mongo():

    mongo_settings = MongoSettings(
        mongo_connection="mongodb://user:pass@mongo:27017",
        mongo_db="db",
        mongo_collection="logs",
    )
    settings = Settings(pu=mongo_settings)
    assert issubclass(settings.backend(), MongoLog)


def test_create_settings_passing_params_sql():

    sql_settings = SQLSettings(
        sql_dsn="postgresql+psycopg2://user:pass@postgres:5432/db",
        sql_table="logs",
    )
    settings = Settings(pu=sql_settings)
    assert issubclass(settings.backend(), SQLLog)


# env vars
def test_create_settings_env_vars_redis(env_vars_redis):
    settings = Settings()
    klass = settings.backend()
    assert klass == RedisLog
    assert klass.Meta.redis_password == "pass"


def test_create_settings_env_vars_mongo(env_vars_mongo):
    settings = Settings()
    klass = settings.backend()
    assert klass == MongoLog
    assert klass.Meta.mongo_connection == "mongodb://user:pass@mongo:27017"


def test_create_settings_env_vars_sql(env_vars_sql):
    settings = Settings()
    klass = settings.backend()
    assert klass == SQLLog
    assert (
        klass.Meta.sql_dsn
        == "postgresql+psycopg2://user:pass@postgres:5432/db"
    )
