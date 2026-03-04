"""Stress and edge-case tests for the Ledger CLI reader and filter logic."""

import json
from datetime import datetime
from pathlib import Path

from src.ledger_cli import format_table
from src.ledger_reader import filter_events, parse_ledger_file

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "edge_case_ledger.jsonl"


def test_empty_jsonl_produces_clean_empty_output(tmp_path):
    """Empty JSONL file produces clean empty output, no crash."""
    empty_file = tmp_path / "empty.jsonl"
    empty_file.write_text("", encoding="utf-8")

    events = parse_ledger_file(empty_file)
    assert events == []
    assert format_table(events) == "No matching events found."


def test_all_malformed_lines_warning_and_empty(tmp_path, capsys):
    """JSONL with only malformed lines produces warnings to stderr and empty event list."""
    bad_file = tmp_path / "bad.jsonl"
    bad_file.write_text(
        "not json at all\n"
        "{broken json\n"
        "12345\n",
        encoding="utf-8",
    )

    events = parse_ledger_file(bad_file)
    assert events == []

    captured = capsys.readouterr()
    assert captured.err.count("Warning: skipping malformed line") == 3


def test_1000_line_file_filters_correctly(tmp_path):
    """1000-line JSONL file filters correctly and completes promptly."""
    large_file = tmp_path / "large.jsonl"
    lines: list[str] = []
    for i in range(1000):
        event_type = "type_a" if i < 500 else "type_b"
        entry = {
            "timestamp": f"2025-01-{(i % 28) + 1:02d}T10:00:00",
            "event_type": event_type,
            "task_id": f"task-{i:04d}",
            "description": f"Event number {i}",
        }
        lines.append(json.dumps(entry))
    large_file.write_text("\n".join(lines), encoding="utf-8")

    events = parse_ledger_file(large_file)
    assert len(events) == 1000

    filtered = filter_events(events, event_type="type_a")
    assert len(filtered) == 500
    assert all(e.event_type == "type_a" for e in filtered)


def test_unicode_in_description_handled():
    """Unicode characters in the description field are preserved correctly."""
    events = parse_ledger_file(FIXTURE_PATH)
    unicode_event = [e for e in events if "café" in e.description]
    assert len(unicode_event) == 1
    assert "résumé" in unicode_event[0].description
    assert "日本語" in unicode_event[0].description
    assert "🚀" in unicode_event[0].description


def test_from_equals_to_returns_exact_date_match():
    """Date filter with from == to returns only events on that exact timestamp."""
    events = parse_ledger_file(FIXTURE_PATH)
    target = datetime(2025, 3, 11, 9, 0, 0)

    filtered = filter_events(events, from_date=target, to_date=target)
    assert len(filtered) == 1
    assert filtered[0].task_id == "edge-001"
    assert filtered[0].timestamp == target


def test_all_filters_combined_nothing_matches():
    """All filters combined on a dataset where no event matches all criteria → empty."""
    events = parse_ledger_file(FIXTURE_PATH)

    filtered = filter_events(
        events,
        event_type="task_started",
        from_date=datetime(2025, 3, 14, 0, 0),
        to_date=datetime(2025, 3, 14, 23, 59),
        task_id="edge-001",
    )
    assert filtered == []


def test_event_type_filter_is_case_sensitive():
    """Event type filter is case-sensitive — 'task_started' does not match 'Task_Started'."""
    events = parse_ledger_file(FIXTURE_PATH)

    lower = filter_events(events, event_type="task_started")
    upper = filter_events(events, event_type="Task_Started")

    lower_ids = {e.task_id for e in lower}
    upper_ids = {e.task_id for e in upper}

    # "Task_Started" (capital) only matches edge-004
    assert "edge-004" in upper_ids
    assert "edge-004" not in lower_ids

    # "task_started" (lowercase) should not include edge-004
    assert all(e.event_type == "task_started" for e in lower)
    assert all(e.event_type == "Task_Started" for e in upper)


def test_extra_fields_in_jsonl_still_parsed():
    """JSONL line with extra unexpected fields is still parsed into a valid LedgerEvent."""
    events = parse_ledger_file(FIXTURE_PATH)
    extra_event = [e for e in events if e.task_id == "edge-005"]
    assert len(extra_event) == 1
    assert extra_event[0].event_type == "review_requested"
    assert extra_event[0].description == "Event with extra fields"
