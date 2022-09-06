import uuid
import redis
import json
from updater.backends import Settings
from updater.backends.redis import RedisLog, RedisSettings


def test_create_settings_passing_params_redis(drop_redis):

    redis_settings = RedisSettings(redis_host="redis", redis_password="pass")
    klass = redis_settings.backend()
    log: RedisLog = klass(task_name="My task")

    with redis.Redis(host="redis", password="pass", port=6379, db=1) as r:
        assert not r.get(str(log.uuid))

    log.description = "A description"
    log = log.save()

    log = RedisLog.get(uuid=log.uuid)
    assert log.description == "A description"
    assert isinstance(log.uuid, uuid.UUID)

    with redis.Redis(host="redis", password="pass", port=6379, db=1) as r:
        assert r.get(str(log.uuid))

    assert 1 == log.delete()

    with redis.Redis(host="redis", password="pass", port=6379, db=1) as r:
        assert not r.get(str(log.uuid))

    assert 0 == log.delete()


def test_create_settings_env_vars_redis(drop_redis, env_vars_redis):

    settings = Settings()
    klass = settings.backend()
    log: RedisLog = klass(task_name="My task")

    with redis.Redis(host="redis", password="pass", port=6379, db=1) as r:
        assert not r.get(str(log.uuid))

    log.description = "A description"
    log = log.save()

    log = RedisLog.get(uuid=log.uuid)
    assert log.description == "A description"
    assert isinstance(log.uuid, uuid.UUID)

    with redis.Redis(host="redis", password="pass", port=6379, db=1) as r:
        assert r.get(str(log.uuid))

    assert 1 == log.delete()

    with redis.Redis(host="redis", password="pass", port=6379, db=1) as r:
        assert not r.get(str(log.uuid))

    assert 0 == log.delete()
