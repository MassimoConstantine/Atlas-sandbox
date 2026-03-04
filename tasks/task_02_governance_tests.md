# Task 02: Governance Engine — Edge Case Tests

## Description

Write additional test coverage for the Atlas governance engine, focusing on edge cases not covered by the main test suite. This includes boundary conditions for trust tiers, malformed governance verdicts, concurrent governance checks, empty or missing fields, and timeout scenarios. The goal is to harden the governance layer by proving it handles adversarial and unexpected inputs safely.

## Acceptance Criteria

- [ ] At least 15 new test functions covering governance edge cases
- [ ] Tests cover: malformed verdicts, missing fields, boundary trust tiers, empty input, conflicting rules
- [ ] All tests are self-contained (no external dependencies, no network calls)
- [ ] Tests use pytest fixtures for setup/teardown
- [ ] Every test has a descriptive docstring explaining what edge case it covers

## Files to Create

- `src/governance_edge_cases.py` — Helper functions and mock governance structures for testing
- `tests/test_governance_edge_cases.py` — The edge case test suite
- `tests/fixtures/governance_fixtures.py` — Shared fixtures for governance tests

## Files NOT to Touch

- `CLAUDE.md`
- `docs/scope-boundary.md`
- `tasks/` (any file)
- `pyproject.toml`
- `tests/test_baseline.py`

## Tests Required

- Test: Governance verdict with missing `decision` field raises ValidationError
- Test: Governance verdict with unknown decision value is rejected
- Test: Trust tier 0 always overrides tier 3-4
- Test: Trust tier boundary (tier 2 vs tier 3) is correctly enforced
- Test: Empty rule set produces ALLOW by default (or BLOCK — document which)
- Test: Duplicate rules are deduplicated without error
- Test: Rule with future effective_date is not yet active
- Test: Governance check with None input returns safe default
- Test: Extremely long reason string is handled (no truncation crash)
- Test: Verdict with confidence=0 is flagged as unreliable
- Test: Circular rule dependencies are detected and rejected
- Test: Governance check returns within timeout (mock slow handler)
- Test: Multiple simultaneous governance checks don't interfere
- Test: Rule priority ordering is deterministic for equal-priority rules
- Test: Governance audit log records all check attempts including failures

## Estimated Effort

3-4 hours
