## Task 05 Completion Report

**Status:** Complete
**Confidence:** 5 — All 9 required tests pass, all acceptance criteria met, ruff clean.

### What Was Implemented

A Pydantic model linter that scans Python files for BaseModel subclasses and checks 5 convention rules: class docstrings, field ordering (required before optional), no Any type, snake_case field names, and type hint presence. Reports violations with file path, line number, model name, and description. CLI supports `--strict` flag that treats warnings as errors for exit code purposes.

### Files Created or Modified

- `src/lint_rules.py` — Severity enum, Violation dataclass, 5 rule functions (created)
- `src/model_linter.py` — AST scanner, directory/file scanning, CLI entry point (created)
- `tests/fixtures/clean_models.py` — 2 clean BaseModel classes + 1 non-BaseModel (created)
- `tests/fixtures/dirty_models.py` — 1 BadModel with 5 violations + 1 RegularClass (created)
- `tests/test_model_linter.py` — 9 tests covering all required scenarios (created)
- `reports/task_05_preflight.md` — Pre-flight check (created)
- `reports/task_05_report.md` — This file (created)

### Assumptions Made

- BaseModel subclasses detected by checking class bases for `BaseModel` name in AST (covers `class Foo(BaseModel)` and `class Foo(pydantic.BaseModel)`)
- Field ordering: `ast.AnnAssign` with a `value` (default) or `Optional`/`None` in annotation = optional; without = required
- Bare assignments (`ast.Assign`) in class body = missing type hint violation
- Field ordering is a WARNING; all other violations are ERRORs
- Non-BaseModel classes are completely skipped (no rules applied)

### Known Limitations

- Does not detect BaseModel subclasses through indirect inheritance (e.g., `class Foo(MyBaseModel)` where `MyBaseModel` extends `BaseModel`)
- snake_case regex is strict: requires lowercase start, underscores between segments
- Directory scanning is non-recursive (top-level `.py` files only)

### Test Results

67 passed, 0 failed (pytest tests/ -v)

### Lint Results

All checks passed (ruff check .)
