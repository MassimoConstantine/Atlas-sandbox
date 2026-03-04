## Run 10 Pre-Flight Check

### Task Summary

Variant run: stress tests with pathological Pydantic models against the existing model linter (src/model_linter.py, src/lint_rules.py). No source modifications.

### Test Cases (minimum 8)

1. Model with 50 fields — all linted correctly
2. Model with no fields (empty body) — handled gracefully
3. Field with extremely long name (200 chars)
4. Model inheriting from non-BaseModel class — skipped
5. Model with validator methods — validators not flagged as missing docstrings
6. Nested model (model field referencing another model)
7. Model with Field(...) using alias, description, examples
8. File with syntax errors — linter fails gracefully with clear error

### Files to Create

- `reports/run_10_preflight.md` — This file
- `tests/fixtures/pathological_models.py` — Pathological model fixtures
- `tests/test_linter_stress.py` — 8+ stress test functions
- `reports/run_10_report.md` — Completion report

### Files NOT to Touch

- All existing `src/` files
- `CLAUDE.md`, `docs/`, `tasks/`, `pyproject.toml`, `tests/test_baseline.py`

### Scope Confirmation

All intended actions (create files in `tests/` and `reports/`; run `pytest`; run `ruff`) fall within the CAN list.
