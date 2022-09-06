from updater.utils import progress_updater
from updater.backends import Settings
from updater.backends.sql import SQLSettings, SQLLog
from updater.backends.mongo import MongoSettings, MongoLog
from updater.backends.redis import RedisSettings, RedisLog


def test_progress_updater_passing_params_redis(redis_backend):
    redis_settings = RedisSettings(redis_password="pass")

    @progress_updater(task_name="My task", settings=redis_settings)
    def task():
        return "doing a lot of work..."

    task()  # run the task

    assert redis.get()


def test_progress_updater_passing_params_mongo(mongo_backend):

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


def test_progress_updater_passing_params_sql(sql):

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
def test_progress_updater_env_vars_redis(redis_backend, env_vars_redis):
    settings = Settings()
    klass = settings.backend()
    assert klass == RedisLog
    assert klass.Meta.redis_password == RedisLog.Meta.redis_password == "pass"


def test_progress_updater_env_vars_mongo(mongo_backend, env_vars_mongo):
    settings = Settings()
    klass = settings.backend()
    assert klass == MongoLog
    assert (
        klass.Meta.mongo_connection
        == MongoLog.Meta.mongo_connection
        == "mongodb://user:pass@mongo:27017"
    )


def test_progress_updater_env_vars_sql(env_vars_sql):
    settings = Settings()
    klass = settings.backend()
    assert klass == SQLLog
    assert (
        klass.Meta.sql_dsn
        == SQLLog.Meta.sql_dsn
        == "postgresql+psycopg2://user:pass@postgres:5432/db"
    )
