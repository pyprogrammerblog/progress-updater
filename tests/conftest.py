import os
import pytest


@pytest.fixture(scope="function")
def env_file():
    try:
        with open("~./env", "a") as file:
            yield file
    finally:
        os.remove("~./env")


@pytest.fixture(scope="function")
def env_file_redis(env_file):
    env_file.write("PU__REDIS_HOST=redis")
    env_file.write("PU__REDIS_DB=1")
    env_file.write("PU__REDIS_PASSWORD=pass")
    yield


@pytest.fixture(scope="function")
def env_file_mongo(env_file):
    env_file.write("PU__MONGO_CONNECTION=mongodb://user:pass@mongo:27017")
    env_file.write("PU__MONGO_DB_NAME=db")
    env_file.write("PU__MONGO_COLLECTION=logs")
    yield


@pytest.fixture(scope="function")
def env_file_sql(env_file):
    env_file.write(
        "PU__SQL_DSN=postgresql+psycopg2://user:pass@postgres:5432/db"
    )
    env_file.write("PU__SQL_TABLE=logs")
    yield


@pytest.fixture(scope="function")
def env_vars_redis():
    os.environ["PU__REDIS_HOST"] = "redis"
    os.environ["PU__REDIS_DB"] = "1"
    os.environ["PU__REDIS_PASSWORD"] = "pass"
    try:
        yield
    finally:
        del os.environ["PU__REDIS_HOST"]
        del os.environ["PU__REDIS_DB"]
        del os.environ["PU__REDIS_PASSWORD"]


@pytest.fixture(scope="function")
def env_vars_mongo():
    os.environ["PU__MONGO_CONNECTION"] = "mongodb://user:pass@mongo:27017"
    os.environ["PU__MONGO_DB"] = "db"
    os.environ["PU__MONGO_COLLECTION"] = "logs"
    try:
        yield
    finally:
        del os.environ["PU__MONGO_CONNECTION"]
        del os.environ["PU__MONGO_DB"]
        del os.environ["PU__MONGO_COLLECTION"]


@pytest.fixture(scope="function")
def env_vars_sql():
    os.environ[
        "PU__SQL_DSN"
    ] = "postgresql+psycopg2://user:pass@postgres:5432/db"
    os.environ["PU__SQL_TABLE"] = "logs"
    try:
        yield
    finally:
        del os.environ["PU__SQL_DSN"]
        del os.environ["PU__SQL_TABLE"]
