import logging
from datetime import datetime
from uuid import UUID
from progress_updater.backends import BaseConfig
from progress_updater.backends.base import BaseLog
from pymongo.collection import Collection
from contextlib import contextmanager
from pymongo.mongo_client import MongoClient

__all__ = ["RedisLog", "RedisConfig"]


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


class RedisConfig(BaseConfig):

    redis_host: str
    redis_db: int
    redis_password: str

    def backend(self):
        RedisLog.Config.redis_host = self.redis_host
        RedisLog.Config.redis_db = self.redis_db
        RedisLog.Config.redis_password = self.redis_password
        return RedisLog
