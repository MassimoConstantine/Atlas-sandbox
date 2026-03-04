# Task 03: Pydantic Schema Validator

## Description

Build a validation utility that takes JSON files representing Atlas data structures (TaskIntent, BuildPlan, and other pipeline schemas) and validates them against their corresponding Pydantic models. The tool reads a JSON file, identifies which schema it should conform to (via a `schema_type` field or CLI argument), runs Pydantic validation, and reports all errors in a structured, human-readable format. This supports Atlas pipeline integrity by catching malformed data before it enters the system.

## Acceptance Criteria

- [ ] Validates JSON files against Pydantic v2 models for TaskIntent and BuildPlan
- [ ] Reports all validation errors with field path, expected type, and actual value
- [ ] Supports batch validation of a directory of JSON files
- [ ] Exit code 0 when all files valid, exit code 1 when any file has errors
- [ ] Outputs a summary line: "X files validated, Y passed, Z failed"

## Files to Create

- `src/schema_validator.py` — Main validation logic and CLI entry point
- `src/schemas.py` — Pydantic v2 models for TaskIntent, BuildPlan, and related types
- `tests/test_schema_validator.py` — Validation logic tests
- `tests/fixtures/valid_task_intent.json` — Valid TaskIntent sample
- `tests/fixtures/invalid_task_intent.json` — Invalid TaskIntent sample (missing required fields)
- `tests/fixtures/valid_build_plan.json` — Valid BuildPlan sample
- `tests/fixtures/invalid_build_plan.json` — Invalid BuildPlan sample

## Files NOT to Touch

- `CLAUDE.md`
- `docs/scope-boundary.md`
- `tasks/` (any file)
- `pyproject.toml`
- `tests/test_baseline.py`

## Tests Required

- Test: Valid TaskIntent JSON passes validation
- Test: Invalid TaskIntent JSON fails with correct error messages
- Test: Valid BuildPlan JSON passes validation
- Test: Invalid BuildPlan JSON fails with correct error messages
- Test: Missing `schema_type` field is handled gracefully
- Test: Batch validation reports correct pass/fail counts
- Test: Non-JSON file produces clear error (not a stack trace)
- Test: Empty JSON file is reported as invalid

## Estimated Effort

2-3 hours
