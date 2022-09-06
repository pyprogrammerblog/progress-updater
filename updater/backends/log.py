from datetime import datetime
from pydantic import BaseModel
from pydantic import Field
from typing import Any
from typing import Optional
from uuid import uuid4, UUID
from typing import List

import logging


logger = logging.getLogger(__name__)


DEFAULT_TTR = 30 * 60  # 30 min


class Status:
    """
    Status
    """

    PENDING: str = "PENDING"
    STARTED: str = "STARTED"
    SUCCESS: str = "SUCCESS"


class Log(BaseModel):
    """
    Defines the log written to DB
    """

    uuid: UUID = Field(default_factory=uuid4, description="UUID")
    task_name: str = Field(description="Task name")
    status: str = Field(default=Status.PENDING, description="Status")
    log: Optional[Any] = Field(default=None, description="Result")

    start_time: Optional[datetime] = Field(
        default_factory=datetime.utcnow, description="Started"
    )
    end_time: Optional[datetime] = Field(None, description="Finished")

    created: datetime = Field(default_factory=datetime.utcnow)
    updated: datetime = Field(default=None)


class Logs(BaseModel):
    logs: List[Log] = Field(default_factory=list, description="Logs")
    count: int = Field(default=0, description="Count")
