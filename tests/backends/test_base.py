from updater.backends import Settings
from updater.backends.sql import SQLSettings, SQLLog
from updater.backends.mongo import MongoSettings, MongoLog
from updater.backends.redis import RedisSettings, RedisLog


# passing params
def test_create_settings_passing_params_redis():

    redis_settings = RedisSettings()
    settings = Settings(pu=redis_settings)
    assert isinstance(settings.backend(), RedisLog)


def test_create_settings_passing_params_mongo():

    redis_settings = MongoSettings()
    settings = Settings(pu=redis_settings)
    assert isinstance(settings.backend(), MongoLog)


def test_create_settings_passing_params_sql():

    redis_settings = SQLSettings()
    settings = Settings(pu=redis_settings)
    assert isinstance(settings.backend(), SQLLog)


# env file
def test_create_settings_env_file_redis(env_file_redis):
    settings = Settings()
    assert isinstance(settings.backend(), RedisLog)


def test_create_settings_env_file_mongo(env_file_mongo):
    settings = Settings()
    assert isinstance(settings.backend(), MongoLog)


def test_create_settings_env_file_sql(env_file_sql):
    settings = Settings()
    assert isinstance(settings.backend(), SQLLog)


# env vars
def test_create_settings_env_vars_redis(env_vars_redis):
    settings = Settings()
    assert isinstance(settings.backend(), RedisLog)


def test_create_settings_env_vars_mongo(env_vars_mongo):
    settings = Settings()
    assert isinstance(settings.backend(), MongoLog)


def test_create_settings_env_vars_sql(env_vars_sql):
    settings = Settings()
    assert isinstance(settings.backend(), SQLLog)
