from datetime import datetime
from pydantic import BaseModel
from pydantic import Field
from uuid import uuid4, UUID
from typing import List

import logging


__all__ = ["Log", "Logs"]

logger = logging.getLogger(__name__)


class Status:
    """
    Status
    """

    PENDING: str = "PENDING"
    STARTED: str = "STARTED"
    SUCCESS: str = "SUCCESS"


class Log(BaseModel):
    """
    Defines the Log written to DB
    """

    uuid: UUID = Field(default_factory=uuid4, description="UUID")
    task_name: str = Field(description="Task name")
    status: str = Field(default=Status.PENDING, description="Status")
    log: str = Field(default="", description="Result")
    description: str = Field(default=None, description="Description")

    start_time: datetime = Field(
        default_factory=datetime.utcnow, description="Started"
    )
    end_time: datetime = Field(default=None, description="Finished")

    created: datetime = Field(default_factory=datetime.utcnow)
    updated: datetime = Field(default=None)


class Logs(BaseModel):
    logs: List[Log] = Field(default_factory=list, description="Logs")
    count: int = Field(default=0, description="Count")
