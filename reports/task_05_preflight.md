## Task 05 Pre-Flight Check

### Acceptance Criteria (echoed from task)

1. Scans all `.py` files in a given directory for Pydantic BaseModel subclasses
2. Checks: field ordering (required before optional), class docstrings, type hints, no `Any`, snake_case names
3. Reports violations with: file path, line number, model name, violation description
4. Exit code 0 when no violations, exit code 1 when violations found
5. Supports `--strict` flag that treats warnings as errors

### Files to Create

- `src/lint_rules.py` — Individual lint rule implementations
- `src/model_linter.py` — Main linter logic and CLI entry point
- `tests/fixtures/clean_models.py` — Sample file with all conventions followed
- `tests/fixtures/dirty_models.py` — Sample file with multiple violations
- `tests/test_model_linter.py` — 9 linter rule tests

### Files NOT to Touch

- `CLAUDE.md`
- `docs/scope-boundary.md`
- `tasks/` (any file)
- `pyproject.toml`
- `tests/test_baseline.py`

### Scope Confirmation

All intended actions (create files in `src/`, `tests/`, `reports/`; run `pytest`; run `ruff`) fall within the CAN list.
