import logging
from datetime import datetime
from uuid import UUID
from updater.backends import BaseConfig
from pymongo.collection import Collection
from contextlib import contextmanager
from updater.backends.base import BaseLog
from pymongo.mongo_client import MongoClient

__all__ = ["MongoLog", "MongoConfig"]


logger = logging.getLogger(__name__)


class MongoLog(BaseLog):
    """
    Mongo DB Adapter
    """

    class Meta:
        mongo_connection: str
        mongo_db_name: str
        mongo_collection: str

    @classmethod
    @contextmanager
    def mongo_collection(cls) -> Collection:
        """
        Yield a connection
        """
        assert cls.Meta.mongo_connection, "Please set a db connection"
        assert cls.Meta.mongo_db_name, "Please set a db name"
        assert cls.Meta.mongo_collection, "Please set a db collection"

        with MongoClient(
            cls.Meta.mongo_connection, UuidRepresentation="standard"
        ) as client:
            db = client.get_database(cls.Meta.mongo_db_name)
            collection = db.get_collection(cls.Meta.mongo_collection)
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


class MongoConfig(BaseConfig):
    mongo_connection: str
    mongo_db_name: str
    mongo_collection: str

    def backend(self):
        MongoLog.Config.mongo_connection = self.mongo_connection
        MongoLog.Config.mongo_db_name = self.mongo_db_name
        MongoLog.Config.mongo_collection = self.mongo_collection
        return MongoLog