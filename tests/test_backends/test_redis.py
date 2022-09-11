import uuid
from progress_updater.backends import Settings
from progress_updater.backends.redis import RedisLog, RedisSettings


def test_create_settings_passing_params_redis(redis_backend):

    redis_settings = RedisSettings(redis_host="redis", redis_password="pass")
    klass = redis_settings.backend()
    log: RedisLog = klass(task_name="My task")

    assert not redis_backend.get(str(log.uuid))

    log.description = "A description"
    log = log.save()
    log = RedisLog.get(uuid=log.uuid)

    assert log.description == "A description"
    assert isinstance(log.uuid, uuid.UUID)
    assert redis_backend.get(str(log.uuid))
    assert 1 == log.delete()
    assert not redis_backend.get(str(log.uuid))
    assert 0 == log.delete()


def test_create_settings_env_vars_redis(redis_backend, env_vars_redis):

    settings = Settings()
    klass = settings.backend()
    log: RedisLog = klass(task_name="My task")

    assert not redis_backend.get(str(log.uuid))

    log.description = "A description"
    log = log.save()
    log = RedisLog.get(uuid=log.uuid)

    assert log.description == "A description"
    assert isinstance(log.uuid, uuid.UUID)
    assert redis_backend.get(str(log.uuid))
    assert 1 == log.delete()
    assert not redis_backend.get(str(log.uuid))
    assert 0 == log.delete()
