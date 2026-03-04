## Task 01 Pre-Flight Check

### Acceptance Criteria (echoed from task)

1. CLI tool is callable via `python -m src.ledger_cli` or `python src/ledger_cli.py`
2. Supports `--event-type <type>` flag to filter events by `event_type` field
3. Supports `--from <date>` and `--to <date>` flags for date range filtering (ISO 8601)
4. Supports `--task-id <id>` flag to filter events by task identifier
5. Prints a human-readable summary table to stdout with columns: timestamp, event_type, task_id, description

### Files to Create

- `src/ledger_models.py` — Pydantic models for Ledger events
- `src/ledger_reader.py` — Ledger file parsing and filtering logic
- `src/ledger_cli.py` — CLI entry point and argument parsing
- `tests/fixtures/sample_ledger.jsonl` — Sample ledger data for tests
- `tests/test_ledger_reader.py` — Filtering and parsing logic tests
- `tests/test_ledger_cli.py` — CLI argument parsing tests

### Files NOT to Touch

- `CLAUDE.md`
- `docs/scope-boundary.md`
- `tasks/` (any file)
- `pyproject.toml`
- `tests/test_baseline.py`

### Scope Confirmation

All intended actions (create files in `src/`, `tests/`, `reports/`; run `pytest`; run `ruff`) fall within the CAN list in CLAUDE.md.
