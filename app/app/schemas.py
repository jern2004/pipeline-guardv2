from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Severity = Literal["low", "medium", "high", "critical"]
Status = Literal["open", "investigating", "resolved"]


class IncidentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    severity: Severity


class IncidentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    severity: Severity | None = None
    status: Status | None = None


class IncidentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    severity: Severity
    status: Status
    created_at: datetime
    resolved_at: datetime | None