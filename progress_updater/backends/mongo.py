import logging
from datetime import datetime
from uuid import UUID
from typing import Dict, Type, List, Union
from pydantic import BaseModel, Field
from pymongo.collection import Collection
from contextlib import contextmanager
from progress_updater.backends.log import BaseLog
from pymongo.mongo_client import MongoClient

__all__ = ["MongoLog", "MongoSettings"]


logger = logging.getLogger(__name__)


class MongoLog(BaseLog):
    """
    MongoLog class. Defines the Log for Mongo Backend
    """

    class Meta:
        mongo_connection: str
        mongo_db: str
        mongo_collection: str

    @classmethod
    @contextmanager
    def mongo_collection(cls):
        """
        Yield a Mongo connection to our logs Collection
        """
        assert cls.Meta.mongo_connection, "Please set a db connection"
        assert cls.Meta.mongo_db, "Please set a db name"
        assert cls.Meta.mongo_collection, "Please set a db collection"

        with MongoClient(
            cls.Meta.mongo_connection, UuidRepresentation="standard"
        ) as client:  # type: MongoClient
            db = client.get_database(cls.Meta.mongo_db)
            collection = db.get_collection(cls.Meta.mongo_collection)
            yield collection

    @classmethod
    def get(cls, uuid: UUID) -> Union["MongoLog", None]:
        """
        Get object from DataBase

        Usage:
            >>> ...
            >>> log = MongoLog.get(uuid=UUID("<your-uuid>"))
            >>> assert log.uuid == UUID("<your-uuid>")
            >>>
        """
        with cls.mongo_collection() as collection:  # type: Collection
            if task := collection.find_one({"uuid": uuid}):
                return cls(**task)
            return None

    def save(self) -> "MongoLog":
        """
        Updates/Creates object in DataBase

        Usage:
            >>> ...
            >>> log = MongoLog(task_name="My Task")
            >>> log.save()
            >>> log.description = "A new description"
            >>> log.save()
            >>> ...
        """
        self.updated = datetime.utcnow()
        with self.mongo_collection() as collection:  # type: Collection
            collection.update_one(
                filter={"uuid": self.uuid},
                update={"$set": self.dict()},
                upsert=True,
            )
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
        with self.mongo_collection() as collection:  # type: Collection
            deleted = collection.delete_one({"uuid": self.uuid})
            return deleted.deleted_count


class MongoSettings(BaseModel):
    """
    Mongo Settings. Defines settings for Mongo Backend
    """

    mongo_connection: str = Field(..., description="Connection string")
    mongo_db: str = Field(..., description="Database name")
    mongo_collection: str = Field(..., description="Collection name")
    mongo_extras: Dict = Field(default_factory=dict, description="Extras")

    def backend(self) -> Type[MongoLog]:
        """
        Returns a MongoLog class and set Mongo backend settings

        Usage:
            >>> from progress_updater.backends import MongoSettings
            >>>
            >>> settings = MongoSettings(
            >>>     mongo_connection="mongodb://user:pass@mongo:27017",
            >>>     mongo_db="db",
            >>>     mongo_collection="logs"
            >>> )
            >>> MongoLog = MongoSettings.backend()  # type: Type[MongoLog]
            >>> log = MongoLog(task_name="My task", description="A cool task")
            >>> log.save()
            >>>
            >>> assert log.dict() == {"task_name": "My task", ...}
            >>> assert log.json() == '{"task_name": "My task", ...}'
            >>>
            >>> log = MongoLog.get(uuid=UUID("<your-uuid>"))
            >>> assert log.description == "A cool task"
            >>>
            >>> assert log.delete() == 1
        """
        MongoLog.Meta.mongo_connection = self.mongo_connection
        MongoLog.Meta.mongo_db = self.mongo_db
        MongoLog.Meta.mongo_collection = self.mongo_collection
        return MongoLog


class MongoLogs(BaseModel):
    """
    Defines the MongoLogs collection
    """

    logs: List[MongoLog] = Field(default_factory=list, description="Logs")
    count: int = Field(default=0, description="Count")
