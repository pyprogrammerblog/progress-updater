import logging
from datetime import datetime
from uuid import UUID
from progress_updater.backends import BaseConfig
from pymongo.collection import Collection
from contextlib import contextmanager
from progress_updater.backends.base import BaseLog
from pymongo.mongo_client import MongoClient

__all__ = ["MongoLog"]


logger = logging.getLogger(__name__)


class MongoLog(BaseLog):
    """
    Mongo DB Adapter
    """

    class Meta:
        db_conn = None
        db_name = None
        db_collection = None

    @classmethod
    @contextmanager
    def mongo_collection(cls) -> Collection:
        """
        Yield a connection
        """
        assert cls.Meta.db_conn, "Please set a db connection"
        assert cls.Meta.db_name, "Please set a db name"
        assert cls.Meta.db_collection, "Please set a db collection"

        with MongoClient(
            cls.Meta.db_conn, UuidRepresentation="standard"
        ) as client:
            db = client.get_database(cls.Meta.db_name)
            collection = db.get_collection(cls.Meta.db_collection)
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
    updater_mongo_connection: str
    updater_mongo_db_name: str
    updater_mongo_collection: str

    def backend(self):
        MongoLog.Config.db_connection = self.updater_mongo_connection
        MongoLog.Config.db_name = self.updater_mongo_db_name
        MongoLog.Config.db_collection = self.updater_mongo_collection
        return MongoLog
