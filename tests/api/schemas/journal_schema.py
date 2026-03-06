from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JournalEntryResponse(BaseModel):
    """Journal entry schema returned by the POST /journal API."""

    model_config = ConfigDict(extra="forbid")

    id: int
    content: str
    created_at: datetime
    updated_at: datetime | None
    mood: str | None
