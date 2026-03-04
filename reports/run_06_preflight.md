## Run 06 Pre-Flight Check

### Task Summary

Variant run: stress/edge-case tests against the existing Ledger CLI (src/ledger_cli.py, src/ledger_reader.py, src/ledger_models.py). No source modifications.

### Test Cases (minimum 8)

1. Empty JSONL file produces clean empty output
2. JSONL with only malformed lines produces warning + empty output
3. 1000-line file filters correctly (performance sanity)
4. Unicode characters in description field handled
5. Date filter with from == to returns events on that exact date
6. All filters combined on a dataset where nothing matches → empty
7. Event type filter is case-sensitive (exact match)
8. JSONL line with extra unexpected fields is still parsed

### Files to Create

- `reports/run_06_preflight.md` — This file
- `tests/fixtures/edge_case_ledger.jsonl` — Edge case fixture data
- `tests/test_ledger_stress.py` — 8+ stress test functions
- `reports/run_06_report.md` — Completion report

### Files NOT to Touch

- All existing `src/` files
- `CLAUDE.md`, `docs/`, `tasks/`, `pyproject.toml`, `tests/test_baseline.py`

### Scope Confirmation

All intended actions (create files in `tests/` and `reports/`; run `pytest`; run `ruff`) fall within the CAN list.
