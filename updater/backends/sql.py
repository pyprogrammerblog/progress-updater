import logging
from typing import Dict
from updater.backends import Base
from datetime import datetime
from uuid import UUID
from updater.backends.base import BaseLog
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlmodel import Session


__all__ = ["SQLLog", "SQLSettings"]


logger = logging.getLogger(__name__)


class SQLLog(BaseLog):
    """
    Mongo DB Adapter
    """

    class Config:
        sql_dsn: str
        sql_table: str

    @classmethod
    @contextmanager
    def sql_session(cls) -> Session:
        """
        Yield a connection
        """
        engine = create_engine(cls.Config.sql_dsn)
        with Session(engine) as session:
            yield session

    @classmethod
    def get(cls, uuid: UUID):
        """
        Get object from DataBase
        """
        with cls.sql_session() as session:
            if task := session.query(SQLLog).get():
                return task

    def save(self):
        """
        Updates object in DataBase
        """
        self.updated = datetime.utcnow()
        with self.sql_session() as collection:
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
        with self.sql_session() as collection:
            deleted = collection.delete_one({"uuid": self.uuid})
            return deleted.deleted_count


class SQLSettings(Base):
    sql_dsn: str
    sql_table: str
    sql_extras: Dict = None

    def backend(self):
        SQLLog.Config.sql_dsn = self.sql_dsn
        SQLLog.Config.sql_table = self.sql_table
        return SQLLog
