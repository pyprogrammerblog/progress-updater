import logging
import redis  # type: ignore
from typing import Dict, Type, List, Union
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from progress_updater.backends.log import BaseLog
from contextlib import contextmanager

__all__ = ["RedisLog", "RedisSettings"]


logger = logging.getLogger(__name__)


class RedisLog(BaseLog):
    """
    RedisLog class. Defines the Log for Redis Backend
    """

    class Meta:
        redis_host: str
        redis_port: int
        redis_db: int
        redis_password: str
        redis_extras: Dict

    @classmethod
    @contextmanager
    def redis_connection(cls):
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
    def get(cls, uuid: UUID) -> Union["RedisLog", None]:
        """
        Get object from DataBase

        Usage:
            >>> ...
            >>> log = RedisLog.get(uuid=UUID("<your-uuid>"))
            >>> assert log.uuid == UUID("<your-uuid>")
            >>>
        """
        with cls.redis_connection() as r:  # type: redis.Redis
            if task := r.get(str(uuid)):
                return cls.parse_raw(task)
            return None

    def save(self) -> "RedisLog":
        """
        Updates/Creates object in DataBase

        Usage:
            >>> ...
            >>> log = RedisLog(task_name="My Task")
            >>> log.save()
            >>> log.description = "A new description"
            >>> log.save()
            >>> ...
        """
        self.updated = datetime.utcnow()
        with self.redis_connection() as r:  # type: redis.Redis
            r.set(str(self.uuid), self.json())
        return self

    def delete(self) -> int:
        """
        Deletes object in DataBase

        Usage:
            >>> ...
            >>> assert log.delete() == 1  # count deleted 1
            >>> assert log.delete() == 0  # count deleted 0
            >>> ...
        """
        with self.redis_connection() as r:  # type: redis.Redis
            return r.delete(str(self.uuid))


class RedisSettings(BaseModel):
    """
    Redis Settings. Defines settings for Redis Backend
    """

    redis_host: str = Field(..., description="Redis Host")
    redis_port: int = Field(default=6379, description="Redis Host")
    redis_db: int = Field(default=1, description="Redis DB")
    redis_password: str = Field(..., description="Redis Password")
    redis_extras: Dict = Field(
        default_factory=dict, description="Redis extras"
    )

    def backend(self) -> Type[RedisLog]:
        """
        Returns a RedisLog class and set Redis backend settings

        Usage:
            >>> from progress_updater.backends import RedisSettings
            >>>
            >>> settings = RedisSettings(
            >>>     redis_host="redis",
            >>>     redis_port="6379",
            >>>     redis_db="logs",
            >>>     redis_password="pass"
            >>> )
            >>> RedisLog = RedisSettings.backend()  # type: Type[RedisLog]
            >>> log = RedisLog(task_name="My task", description="A cool task")
            >>> log.save()
            >>>
            >>> assert log.dict() == {"task_name": "My task", ...}
            >>> assert log.json() == '{"task_name": "My task", ...}'
            >>>
            >>> log = RedisLog.get(uuid=UUID("<your-uuid>"))
            >>> assert log.description == "A cool task"
            >>>
            >>> assert log.delete() == 1
        """
        RedisLog.Meta.redis_host = self.redis_host
        RedisLog.Meta.redis_port = self.redis_port
        RedisLog.Meta.redis_db = self.redis_db
        RedisLog.Meta.redis_password = self.redis_password
        RedisLog.Meta.redis_extras = self.redis_extras
        return RedisLog


class RedisLogs(BaseModel):
    """
    Defines the RedisLogs collection
    """

    logs: List[RedisLog] = Field(default_factory=list, description="Logs")
    count: int = Field(default=0, description="Count")
