import logging
from datetime import datetime
from uuid import uuid4, UUID

from pymongo.collection import Collection
from contextlib import contextmanager
from pydantic import BaseModel, Field
from pymongo.mongo_client import MongoClient

__all__ = ["DBAdapter"]


logger = logging.getLogger(__name__)


class DBAdapter(BaseModel):
    """
    Mongo DB Adapter
    """

    uuid: UUID = Field(default_factory=uuid4, description="UUID")
    updated: datetime = Field(default_factory=datetime.utcnow)

    class Meta:
        db_connection: str = settings.mongo_connection
        db_name: str = settings.mongo_db
        db_collection: str

    @classmethod
    @contextmanager
    def mongo_collection(cls) -> Collection:
        """
        Yield a connection
        """
        db_conn = (
            cls.Meta.db_connection
            if hasattr(cls.Meta, "db_connection")
            else DBAdapter.Meta.db_connection
        )
        db_name = (
            cls.Meta.db_name
            if hasattr(cls.Meta, "db_name")
            else DBAdapter.Meta.db_name
        )
        db_collection = cls.Meta.db_collection or "default"

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
