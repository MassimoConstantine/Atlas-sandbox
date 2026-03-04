## Task 02 Pre-Flight Check

### Acceptance Criteria (echoed from task)

1. At least 15 new test functions covering governance edge cases
2. Tests cover: malformed verdicts, missing fields, boundary trust tiers, empty input, conflicting rules
3. All tests are self-contained (no external dependencies, no network calls)
4. Tests use pytest fixtures for setup/teardown
5. Every test has a descriptive docstring explaining what edge case it covers

### Files to Create

- `src/governance_edge_cases.py` — Helper functions and mock governance structures
- `tests/fixtures/governance_fixtures.py` — Shared pytest fixtures
- `tests/test_governance_edge_cases.py` — 15+ edge case test functions

### Files NOT to Touch

- `CLAUDE.md`
- `docs/scope-boundary.md`
- `tasks/` (any file)
- `pyproject.toml`
- `tests/test_baseline.py`

### Scope Confirmation

All intended actions (create files in `src/`, `tests/`, `reports/`; run `pytest`; run `ruff`) fall within the CAN list in CLAUDE.md.
