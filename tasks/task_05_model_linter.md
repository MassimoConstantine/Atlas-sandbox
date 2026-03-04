# Task 05: Pydantic Model Linter

## Description

Build a linting tool that inspects all Pydantic models in a given directory and checks that they follow Atlas conventions: consistent field ordering (required fields before optional), docstrings on every model class, proper type hints on all fields, no use of `Any` type, and snake_case field names. The tool reports violations with file path, line number, model name, and a description of the issue. This enforces code quality standards for the data model layer.

## Acceptance Criteria

- [ ] Scans all `.py` files in a given directory for Pydantic BaseModel subclasses
- [ ] Checks: field ordering (required before optional), class docstrings, type hints, no `Any`, snake_case names
- [ ] Reports violations with: file path, line number, model name, violation description
- [ ] Exit code 0 when no violations, exit code 1 when violations found
- [ ] Supports `--strict` flag that treats warnings as errors

## Files to Create

- `src/model_linter.py` — Main linter logic and CLI entry point
- `src/lint_rules.py` — Individual lint rule implementations
- `tests/test_model_linter.py` — Linter rule tests
- `tests/fixtures/clean_models.py` — Sample file with all conventions followed
- `tests/fixtures/dirty_models.py` — Sample file with multiple violations

## Files NOT to Touch

- `CLAUDE.md`
- `docs/scope-boundary.md`
- `tasks/` (any file)
- `pyproject.toml`
- `tests/test_baseline.py`

## Tests Required

- Test: Clean models file produces zero violations
- Test: Model without docstring is flagged
- Test: Model with optional field before required field is flagged
- Test: Field using `Any` type is flagged
- Test: Field with camelCase name is flagged
- Test: Field without type hint is flagged
- Test: `--strict` flag changes exit code for warnings
- Test: Non-BaseModel classes are skipped
- Test: Report includes correct file path and line number

## Estimated Effort

3-4 hours
