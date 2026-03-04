"""Tests for ledger file parsing and filtering logic."""

from datetime import datetime
from pathlib import Path

from src.ledger_reader import filter_events, parse_ledger_file

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "sample_ledger.jsonl"


def test_parse_ledger_file_loads_valid_events():
    """Valid JSONL lines are parsed into LedgerEvent objects."""
    events = parse_ledger_file(FIXTURE_PATH)
    assert len(events) == 8


def test_malformed_lines_skipped(capsys):
    """Malformed JSONL lines are skipped with a warning to stderr."""
    events = parse_ledger_file(FIXTURE_PATH)
    captured = capsys.readouterr()
    assert len(events) == 8
    assert "Warning: skipping malformed line" in captured.err


def test_filter_by_event_type():
    """Filtering by event_type returns only matching events."""
    events = parse_ledger_file(FIXTURE_PATH)
    result = filter_events(events, event_type="task_started")
    assert len(result) == 3
    assert all(e.event_type == "task_started" for e in result)


def test_filter_by_date_range():
    """Filtering by date range returns only events within range."""
    events = parse_ledger_file(FIXTURE_PATH)
    result = filter_events(
        events,
        from_date=datetime(2025, 1, 16, 0, 0),
        to_date=datetime(2025, 1, 17, 23, 59, 59),
    )
    assert len(result) == 4
    for e in result:
        assert e.timestamp >= datetime(2025, 1, 16, 0, 0)
        assert e.timestamp <= datetime(2025, 1, 17, 23, 59, 59)


def test_filter_by_task_id():
    """Filtering by task_id returns only matching events."""
    events = parse_ledger_file(FIXTURE_PATH)
    result = filter_events(events, task_id="task-002")
    assert len(result) == 4
    assert all(e.task_id == "task-002" for e in result)


def test_combined_filters():
    """Combined filters use AND logic."""
    events = parse_ledger_file(FIXTURE_PATH)
    result = filter_events(
        events,
        event_type="task_started",
        task_id="task-001",
    )
    assert len(result) == 1
    assert result[0].task_id == "task-001"
    assert result[0].event_type == "task_started"


def test_empty_result_set():
    """Empty result set returns an empty list without errors."""
    events = parse_ledger_file(FIXTURE_PATH)
    result = filter_events(events, event_type="nonexistent_type")
    assert result == []
