from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JournalEntryResponse(BaseModel):
    """Journal entry schema returned by the POST /journal API."""

    model_config = ConfigDict(strict=True, extra="forbid")

    id: int
    content: str
    created_at: datetime
    mood: str | None
