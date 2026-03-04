"""Pydantic models for Atlas Ledger events."""

from datetime import datetime

from pydantic import BaseModel


class LedgerEvent(BaseModel):
    """A single event entry from an Atlas Ledger file."""

    timestamp: datetime
    event_type: str
    task_id: str
    description: str
