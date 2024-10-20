import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class StatusEnum(str, Enum):
    PENDING = "PENDING"
    FAILED = "FAILED"
    SUCCESS = "SUCCESS"
    IN_PROCESS = "IN_PROCESS"


class ReviewRequest(BaseModel):
    token_id: str
    status: str = Field(default=StatusEnum.PENDING)
    url: str
    scrapped_at: datetime = Field(default=None) 
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
