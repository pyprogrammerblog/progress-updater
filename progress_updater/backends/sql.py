import logging
from progress_updater.backends import BaseConfig
from datetime import datetime
from uuid import UUID
from progress_updater.backends.base import BaseLog
from pymongo.collection import Collection
from contextlib import contextmanager


__all__ = ["SQLLog", "SQLConfig"]


logger = logging.getLogger(__name__)


class SQLLog(BaseLog):
    """
    Mongo DB Adapter
    """

    class Config:
        sql_dsn: str
        sql_db_name: str
        sql_table_name: str

    @classmethod
    @contextmanager
    def mongo_collection(cls) -> Collection:
        """
        Yield a connection
        """
        with Session(cls.Config.sql_dsn) as session:
            yield session

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


class SQLConfig(BaseConfig):
    updater_sql_dsn: str
    updater_sql_db_name: str
    updater_sql_table_name: str

    def backend(self):
        SQLLog.Config.db_connection = self.updater_sql_dsn
        SQLLog.Config.db_name = self.updater_sql_db_name
        SQLLog.Config.db_table = self.updater_sql_table_name
        return SQLLog
