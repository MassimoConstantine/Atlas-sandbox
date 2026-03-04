# Task 01: Ledger CLI Tool

## Description

Build a command-line tool that reads Atlas Ledger event files (JSON/JSONL format) and prints filtered summaries. The tool accepts filter flags for event type, date range, and task ID, and outputs a formatted table or list of matching events. This provides a quick way to inspect what happened during Atlas pipeline runs without manually parsing raw log files.

## Acceptance Criteria

- [ ] CLI tool is callable via `python -m src.ledger_cli` or `python src/ledger_cli.py`
- [ ] Supports `--event-type <type>` flag to filter events by their `event_type` field
- [ ] Supports `--from <date>` and `--to <date>` flags to filter events within a date range (ISO 8601 format)
- [ ] Supports `--task-id <id>` flag to filter events by task identifier
- [ ] Prints a human-readable summary table to stdout with columns: timestamp, event_type, task_id, description

## Files to Create

- `src/ledger_cli.py` — Main CLI entry point and argument parsing
- `src/ledger_reader.py` — Ledger file parsing and filtering logic
- `src/ledger_models.py` — Pydantic models for Ledger events
- `tests/test_ledger_cli.py` — CLI argument parsing tests
- `tests/test_ledger_reader.py` — Filtering and parsing logic tests
- `tests/fixtures/sample_ledger.jsonl` — Sample ledger data for tests

## Files NOT to Touch

- `CLAUDE.md`
- `docs/scope-boundary.md`
- `tasks/` (any file)
- `pyproject.toml`
- `tests/test_baseline.py`

## Tests Required

- Test: CLI parses `--event-type` flag correctly
- Test: CLI parses `--from` and `--to` date flags correctly
- Test: CLI parses `--task-id` flag correctly
- Test: Filtering by event_type returns only matching events
- Test: Filtering by date range returns only events within range
- Test: Filtering by task_id returns only matching events
- Test: Combined filters work correctly (AND logic)
- Test: Empty result set produces clean output (no crash)
- Test: Malformed JSONL lines are skipped with warning

## Estimated Effort

2-3 hours
