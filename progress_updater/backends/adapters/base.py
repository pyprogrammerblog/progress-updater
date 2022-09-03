import logging
from datetime import datetime
from uuid import uuid4, UUID
from pydantic import BaseModel, Field

__all__ = ["DBAdapter"]


logger = logging.getLogger(__name__)


class DBAdapter(BaseModel):
    """
    Mongo DB Adapter
    """

    uuid: UUID = Field(default_factory=uuid4, description="UUID")
    updated: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    def get(cls, uuid: UUID):
        """
        Get object from DataBase
        """
        pass

    def save(self):
        """
        Updates object in DataBase
        """
        pass

    def delete(self) -> int:
        """
        Deletes object in DataBase
        """
        pass
