## Run 08 Pre-Flight — Schema Validator Stress Tests (Variant Run)

**Run ID:** sandbox-run-08
**Base:** Run 3 (Task 03 — Pydantic Schema Validator)
**Variant type:** Stress/edge-case testing of existing implementation

### Understanding

This is a VARIANT run. The schema validator (`src/schema_validator.py`, `src/schemas.py`) already exists from Run 3 with full passing tests. My job is to write **stress tests with extreme inputs** to probe the validator's behavior under adversarial and edge-case conditions.

The existing schemas define:
- **TaskIntent**: schema_type (Literal), task_id (str), intent_type (str), scope (list[str]), constraints (list[str]), acceptance_criteria (list[str]), estimated_effort (str), confidence (int, 1-5)
- **BuildPlan**: schema_type (Literal), steps (list[str]), files_to_create (list[str]), files_to_modify (list[str], optional), files_not_to_touch (list[str]), test_strategy (str), dependencies (list[str], optional), stop_conditions (list[str], optional)

### Test Cases (minimum 8)

1. TaskIntent with all optional fields set to null → should fail (TaskIntent has no optional fields; all are required)
2. TaskIntent with 10,000-character strings in every string field → should pass (no length constraints in schema)
3. BuildPlan with 50 steps → should pass (no list-length constraints)
4. BuildPlan with empty steps list → should pass (empty list is valid `list[str]`)
5. Deeply nested JSON (10 levels) in metadata fields → should fail (extra fields not in schema are ignored by default in Pydantic, but the nested structure won't map to any field)
6. Unicode/emoji in field values → should pass (str accepts any unicode)
7. Duplicate step IDs in BuildPlan → should pass (steps is `list[str]`, duplicates allowed)
8. Schema validation error messages are human-readable → verify error formatting contains field paths and readable messages

### Files to Create

| File | Purpose |
|------|---------|
| `reports/run_08_preflight.md` | This pre-flight report |
| `tests/fixtures/stress_task_intent.json` | Stress fixture: TaskIntent with 10k-char strings |
| `tests/fixtures/stress_build_plan.json` | Stress fixture: BuildPlan with 50 steps |
| `tests/test_schema_stress.py` | All 8+ stress test cases |
| `reports/run_08_report.md` | Completion report |

### Files NOT Touched

- `src/schema_validator.py` — read only
- `src/schemas.py` — read only
- `CLAUDE.md`, `docs/`, `tasks/`, `pyproject.toml` — forbidden

### Scope Confirmation

All intended actions are within the CAN list: creating files in `tests/`, `tests/fixtures/`, and `reports/`. No modifications to `src/` files.
