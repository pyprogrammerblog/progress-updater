import os
import pytest
import redis
from pymongo import MongoClient


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


@pytest.fixture(scope="function")
def drop_mongo():
    with MongoClient(
        "mongodb://user:pass@mongo:27017", UuidRepresentation="standard"
    ) as client:
        client.drop_database("db")
        yield
        client.drop_database("db")


@pytest.fixture(scope="function")
def drop_redis():
    with redis.Redis(host="redis", password="pass", port=6379, db=1) as r:
        r.flushdb()
        yield
        r.flushdb()
