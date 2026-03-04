"""Tests for the ledger CLI argument parsing and output."""

from pathlib import Path

from src.ledger_cli import build_parser, format_table, main

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "sample_ledger.jsonl"


def test_parse_event_type_flag():
    """CLI parses --event-type flag correctly."""
    parser = build_parser()
    args = parser.parse_args([str(FIXTURE_PATH), "--event-type", "task_started"])
    assert args.event_type == "task_started"


def test_parse_date_flags():
    """CLI parses --from and --to date flags correctly."""
    parser = build_parser()
    args = parser.parse_args([
        str(FIXTURE_PATH),
        "--from", "2025-01-15",
        "--to", "2025-01-17",
    ])
    assert args.from_date == "2025-01-15"
    assert args.to_date == "2025-01-17"


def test_parse_task_id_flag():
    """CLI parses --task-id flag correctly."""
    parser = build_parser()
    args = parser.parse_args([str(FIXTURE_PATH), "--task-id", "task-001"])
    assert args.task_id == "task-001"


def test_empty_result_clean_output(capsys):
    """Empty result set produces clean output (no crash)."""
    main([str(FIXTURE_PATH), "--event-type", "nonexistent"])
    captured = capsys.readouterr()
    assert "No matching events found." in captured.out


def test_table_output_has_headers(capsys):
    """Output includes the expected column headers."""
    main([str(FIXTURE_PATH)])
    captured = capsys.readouterr()
    assert "timestamp" in captured.out
    assert "event_type" in captured.out
    assert "task_id" in captured.out
    assert "description" in captured.out


def test_format_table_empty_list():
    """format_table with no events returns a clean message."""
    assert format_table([]) == "No matching events found."
