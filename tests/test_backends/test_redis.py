import uuid
import redis
from updater.backends import Settings
from updater.backends.redis import RedisLog, RedisSettings


def test_create_settings_passing_params_mongo(drop_mongo):

    redis_settings = RedisSettings(host="redis", redis_password="pass")
    klass = redis_settings.backend()
    log: RedisLog = klass(task_name="My task")

    with redis.Redis(host="redis", password="pass") as r:
        assert 0 == r.get(str(log.uuid))

    log.description = "A description"
    log = log.save()
    assert log.description == "A description"
    assert isinstance(log.uuid, uuid.UUID)

    with redis.Redis(host="redis", password="pass") as r:
        assert 1 == r.get(str(log.uuid))

    assert 1 == log.delete()

    with redis.Redis(host="redis", password="pass") as r:
        assert 0 == r.get(str(log.uuid))

    assert 0 == log.delete()


def test_create_settings_env_vars_mongo(drop_mongo, env_vars_mongo):

    settings = Settings()
    klass = settings.backend()
    log: RedisLog = klass(task_name="My task")

    with redis.Redis(host="redis", password="pass") as r:
        assert 0 == r.get(str(log.uuid))

    log.description = "A description"
    log = log.save()
    assert log.description == "A description"
    assert isinstance(log.uuid, uuid.UUID)

    with redis.Redis(host="redis", password="pass") as r:
        assert 1 == r.get(str(log.uuid))

    assert 1 == log.delete()

    with redis.Redis(host="redis", password="pass") as r:
        assert 0 == r.get(str(log.uuid))

    assert 0 == log.delete()
