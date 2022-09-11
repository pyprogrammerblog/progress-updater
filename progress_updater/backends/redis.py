import logging
import redis  # type: ignore
from typing import Dict
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from progress_updater.backends.log import Log
from contextlib import contextmanager

__all__ = ["RedisLog", "RedisSettings"]


logger = logging.getLogger(__name__)


class RedisLog(Log):
    """
    Mongo DB Adapter
    """

    class Meta:
        redis_host: str
        redis_port: int
        redis_db: int
        redis_password: str
        redis_extras: Dict

    @classmethod
    @contextmanager
    def redis_connection(cls) -> redis.Redis:
        """
        Yield a redis connection
        """
        assert cls.Meta.redis_host, "Please set a redis host"
        assert cls.Meta.redis_port, "Please set a redis port"
        assert cls.Meta.redis_db, "Please set a redis db"
        assert cls.Meta.redis_password, "Please set a redis password"

        with redis.Redis(
            host=cls.Meta.redis_host,
            port=cls.Meta.redis_port,
            db=cls.Meta.redis_db,
            password=cls.Meta.redis_password,
            **cls.Meta.redis_extras,
        ) as r:
            yield r

    @classmethod
    def get(cls, uuid: UUID):
        """
        Get object from Redis
        """
        with cls.redis_connection() as r:
            if task := r.get(str(uuid)):
                return cls.parse_raw(task)

    def save(self):
        """
        Updates object in Redis
        """
        self.updated = datetime.utcnow()
        with self.redis_connection() as r:
            r.set(str(self.uuid), self.json())
        return self

    def delete(self) -> int:
        """
        Deletes object in DataBase
        """
        with self.redis_connection() as r:
            return r.delete(str(self.uuid))


class RedisSettings(BaseModel):
    """
    Redis Settings
    """

    redis_host: str
    redis_port: int = 6379
    redis_db: int = 1
    redis_password: str
    redis_extras: Dict = {}

    def backend(self):
        RedisLog.Meta.redis_host = self.redis_host
        RedisLog.Meta.redis_port = self.redis_port
        RedisLog.Meta.redis_db = self.redis_db
        RedisLog.Meta.redis_password = self.redis_password
        RedisLog.Meta.redis_extras = self.redis_extras
        return RedisLog
