## Run 07 — Pre-Flight Check (Variant: Governance Stress Tests)

**Task:** Write adversarial stress tests against the existing `GovernanceEngine` in `src/governance_edge_cases.py`.

### Understanding of Acceptance Criteria

This is a VARIANT run. The GovernanceEngine already exists from Run 2. My job is to write **8+ adversarial stress tests** that push the engine beyond normal edge cases:

1. **100 rules at scale** — correct precedence maintained when evaluating 100 rules
2. **effective_date exactly now** — boundary test: rule with effective_date == now is active
3. **confidence boundaries** — confidence=1.0 and confidence=0.001 both behave correctly
4. **All BLOCK + one tier-0 ALLOW** — the tier-0 ALLOW wins over all BLOCK rules
5. **Audit log order under rapid sequential checks** — order preserved across many fast evaluations
6. **Empty string rule_id** — engine handles rule_id="" gracefully
7. **Empty reason string** — GovernanceVerdict with reason="" is valid
8. **Duplicate detection (identical except rule_id)** — rules with same content but different IDs are kept

### Files to Create

| File | Purpose |
|------|---------|
| `reports/run_07_preflight.md` | This file |
| `tests/test_governance_stress.py` | Adversarial stress test suite |
| `reports/run_07_report.md` | Completion report |

### Files NOT Touched

- `src/governance_edge_cases.py` (read-only for this run)
- `CLAUDE.md`, `docs/`, `tasks/`, `pyproject.toml`
- No existing test files modified

### Confirmation

All intended actions fall within the CAN list:
- Creating files in `tests/` and `reports/` only
- Running `pytest` and `ruff` for verification
- Reading existing files for context
