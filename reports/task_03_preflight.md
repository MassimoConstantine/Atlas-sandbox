## Task 03 Pre-Flight Check

### Acceptance Criteria (echoed from task)

1. Validates JSON files against Pydantic v2 models for TaskIntent and BuildPlan
2. Reports all validation errors with field path, expected type, and actual value
3. Supports batch validation of a directory of JSON files
4. Exit code 0 when all files valid, exit code 1 when any file has errors
5. Outputs a summary line: "X files validated, Y passed, Z failed"

### Files to Create

- `src/schemas.py` — Pydantic v2 models for TaskIntent, BuildPlan
- `src/schema_validator.py` — Validation logic, error formatting, CLI entry point
- `tests/fixtures/valid_task_intent.json` — Valid TaskIntent sample
- `tests/fixtures/invalid_task_intent.json` — Invalid TaskIntent sample
- `tests/fixtures/valid_build_plan.json` — Valid BuildPlan sample
- `tests/fixtures/invalid_build_plan.json` — Invalid BuildPlan sample
- `tests/test_schema_validator.py` — 8 validation tests

### Files NOT to Touch

- `CLAUDE.md`
- `docs/scope-boundary.md`
- `tasks/` (any file)
- `pyproject.toml`
- `tests/test_baseline.py`

### Scope Confirmation

All intended actions (create files in `src/`, `tests/`, `reports/`; run `pytest`; run `ruff`) fall within the CAN list.
