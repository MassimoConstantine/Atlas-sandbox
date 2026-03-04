"""Ledger file parsing and event filtering logic."""

import json
import sys
from datetime import datetime
from pathlib import Path

from src.ledger_models import LedgerEvent


def parse_ledger_file(path: Path) -> list[LedgerEvent]:
    """Parse a JSONL ledger file into a list of LedgerEvent objects.

    Malformed lines are skipped with a warning printed to stderr.
    """
    events: list[LedgerEvent] = []
    with open(path, encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                events.append(LedgerEvent(**data))
            except (json.JSONDecodeError, Exception) as e:  # noqa: BLE001
                print(
                    f"Warning: skipping malformed line {line_num}: {e}",
                    file=sys.stderr,
                )
    return events


def filter_events(
    events: list[LedgerEvent],
    *,
    event_type: str | None = None,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    task_id: str | None = None,
) -> list[LedgerEvent]:
    """Filter ledger events using AND logic across all provided criteria."""
    result = events
    if event_type is not None:
        result = [e for e in result if e.event_type == event_type]
    if from_date is not None:
        result = [e for e in result if e.timestamp >= from_date]
    if to_date is not None:
        result = [e for e in result if e.timestamp <= to_date]
    if task_id is not None:
        result = [e for e in result if e.task_id == task_id]
    return result
