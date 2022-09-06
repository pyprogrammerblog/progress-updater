import logging
from typing import Dict
from datetime import datetime
from uuid import UUID
from updater.backends import Base
from updater.backends.base import BaseLog
from pymongo.collection import Collection
from contextlib import contextmanager
from pymongo.mongo_client import MongoClient

__all__ = ["RedisLog", "RedisSettings"]


logger = logging.getLogger(__name__)


class RedisLog(BaseLog):
    """
    Mongo DB Adapter
    """

    @classmethod
    @contextmanager
    def mongo_collection(cls) -> Collection:
        """
        Yield a connection
        """
        with MongoClient(db_conn, UuidRepresentation="standard") as client:
            db = client.get_database(db_name)
            collection = db.get_collection(db_collection)
            yield collection

    @classmethod
    def get(cls, uuid: UUID):
        """
        Get object from DataBase
        """
        with cls.mongo_collection() as collection:
            if task := collection.find_one({"uuid": uuid}):
                return cls(**task)

    def save(self):
        """
        Updates object in DataBase
        """
        self.updated = datetime.utcnow()
        with self.mongo_collection() as collection:
            collection.update_one(
                filter={"uuid": self.uuid},
                update={"$set": self.dict()},
                upsert=True,
            )
        return self

    def delete(self) -> int:
        """
        Deletes object in DataBase
        """
        with self.mongo_collection() as collection:
            deleted = collection.delete_one({"uuid": self.uuid})
            return deleted.deleted_count


class RedisSettings(Base):

    redis_host: str = "localhost"
    redis_db: int = 1
    redis_password: str
    redis_extras: Dict = None

    def backend(self):
        RedisLog.Config.redis_host = self.redis_host
        RedisLog.Config.redis_db = self.redis_db
        RedisLog.Config.redis_password = self.redis_password
        return RedisLog
