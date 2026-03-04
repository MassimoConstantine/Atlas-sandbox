"""Edge case tests for the Atlas governance engine."""

import time
from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from src.governance_edge_cases import GovernanceEngine, GovernanceRule, GovernanceVerdict


def test_missing_decision_field_raises_validation_error():
    """Verdict with missing 'decision' field raises ValidationError."""
    with pytest.raises(ValidationError):
        GovernanceVerdict(confidence=0.9, reason="test", trust_tier=1)  # type: ignore[call-arg]


def test_unknown_decision_value_rejected():
    """Verdict with an unknown decision value (not ALLOW/BLOCK) is rejected."""
    with pytest.raises(ValidationError):
        GovernanceVerdict(decision="MAYBE", confidence=0.9, reason="test", trust_tier=1)


def test_tier0_overrides_tier3(
    engine: GovernanceEngine,
    tier0_block_rule: GovernanceRule,
    tier3_allow_rule: GovernanceRule,
):
    """Trust tier 0 BLOCK always overrides tier 3 ALLOW."""
    result = engine.evaluate([tier0_block_rule, tier3_allow_rule], input_data="check")
    assert result.decision == "BLOCK"
    assert result.trust_tier == 0


def test_tier0_overrides_tier4(
    engine: GovernanceEngine,
    tier0_block_rule: GovernanceRule,
    tier4_allow_rule: GovernanceRule,
):
    """Trust tier 0 BLOCK always overrides tier 4 ALLOW."""
    result = engine.evaluate([tier4_allow_rule, tier0_block_rule], input_data="check")
    assert result.decision == "BLOCK"
    assert result.trust_tier == 0


def test_tier2_vs_tier3_boundary(
    engine: GovernanceEngine,
    tier2_block_rule: GovernanceRule,
    tier3_allow_rule: GovernanceRule,
):
    """Tier 2 BLOCK takes precedence over tier 3 ALLOW (lower tier wins)."""
    result = engine.evaluate([tier3_allow_rule, tier2_block_rule], input_data="check")
    assert result.decision == "BLOCK"
    assert result.trust_tier == 2


def test_empty_rule_set_produces_allow(engine: GovernanceEngine):
    """Empty rule set produces ALLOW by default (no restrictions)."""
    result = engine.evaluate([], input_data="check")
    assert result.decision == "ALLOW"


def test_duplicate_rules_deduplicated(engine: GovernanceEngine):
    """Duplicate rules (same rule_id) are deduplicated without error."""
    rule = GovernanceRule(rule_id="dup", action="BLOCK", priority=5, trust_tier=1)
    deduped = engine.deduplicate_rules([rule, rule, rule])
    assert len(deduped) == 1
    assert deduped[0].rule_id == "dup"


def test_future_effective_date_not_active(engine: GovernanceEngine):
    """Rule with future effective_date is excluded from active rules."""
    future_rule = GovernanceRule(
        rule_id="future",
        action="BLOCK",
        priority=10,
        trust_tier=0,
        effective_date=datetime.now(timezone.utc) + timedelta(days=30),
    )
    active = engine.get_active_rules([future_rule])
    assert len(active) == 0


def test_none_input_returns_safe_default(engine: GovernanceEngine):
    """Governance check with None input returns a safe default verdict."""
    rule = GovernanceRule(rule_id="r1", action="BLOCK", priority=5, trust_tier=1)
    result = engine.evaluate([rule], input_data=None)
    assert result.decision == "ALLOW"
    assert result.reason == "None input — safe default"


def test_extremely_long_reason_string():
    """Extremely long reason string is handled without truncation crash."""
    long_reason = "x" * 1_000_000
    verdict = GovernanceVerdict(
        decision="ALLOW", confidence=0.8, reason=long_reason, trust_tier=1
    )
    assert len(verdict.reason) == 1_000_000


def test_confidence_zero_flagged_unreliable():
    """Verdict with confidence=0 is flagged as unreliable via is_reliable property."""
    verdict = GovernanceVerdict(
        decision="ALLOW", confidence=0.0, reason="low confidence", trust_tier=1
    )
    assert verdict.is_reliable is False


def test_circular_rule_dependencies_detected(engine: GovernanceEngine):
    """Circular rule dependencies (A->B->A) are detected and raise ValueError."""
    rule_a = GovernanceRule(
        rule_id="A", action="ALLOW", trust_tier=1, depends_on=["B"]
    )
    rule_b = GovernanceRule(
        rule_id="B", action="ALLOW", trust_tier=1, depends_on=["A"]
    )
    with pytest.raises(ValueError, match="Circular dependency"):
        engine.detect_circular_deps([rule_a, rule_b])


def test_governance_check_returns_within_timeout(engine: GovernanceEngine):
    """Governance check with a slow handler exceeding timeout raises TimeoutError."""

    def slow_handler() -> GovernanceVerdict:
        time.sleep(5)
        return GovernanceVerdict(
            decision="ALLOW", confidence=1.0, reason="slow", trust_tier=0
        )

    with pytest.raises(TimeoutError, match="exceeded timeout"):
        engine.check_with_timeout(slow_handler, timeout=0.1)


def test_multiple_simultaneous_checks_no_interference():
    """Multiple simultaneous governance checks on separate engines don't interfere."""
    import concurrent.futures

    def run_check(decision: str) -> str:
        eng = GovernanceEngine()
        rule = GovernanceRule(
            rule_id=f"rule-{decision}",
            action=decision,
            priority=10,
            trust_tier=0,
        )
        result = eng.evaluate([rule], input_data="parallel")
        return result.decision

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(run_check, "ALLOW"),
            executor.submit(run_check, "BLOCK"),
            executor.submit(run_check, "ALLOW"),
            executor.submit(run_check, "BLOCK"),
        ]
        results = [f.result() for f in futures]

    assert results[0] == "ALLOW"
    assert results[1] == "BLOCK"
    assert results[2] == "ALLOW"
    assert results[3] == "BLOCK"


def test_rule_priority_ordering_deterministic(engine: GovernanceEngine):
    """Equal-priority rules are ordered deterministically by rule_id."""
    rules = [
        GovernanceRule(rule_id="C", action="ALLOW", priority=5, trust_tier=1),
        GovernanceRule(rule_id="A", action="ALLOW", priority=5, trust_tier=1),
        GovernanceRule(rule_id="B", action="ALLOW", priority=5, trust_tier=1),
    ]
    sorted_rules = engine.sort_rules(rules)
    assert [r.rule_id for r in sorted_rules] == ["A", "B", "C"]


def test_audit_log_records_all_attempts(engine: GovernanceEngine):
    """Governance audit log records all check attempts including failures."""
    # Successful check
    engine.evaluate([], input_data="test")
    assert len(engine.audit_log) == 1
    assert engine.audit_log[0].success is True

    # Check that triggers circular dep error
    rule_a = GovernanceRule(
        rule_id="X", action="ALLOW", trust_tier=1, depends_on=["Y"]
    )
    rule_b = GovernanceRule(
        rule_id="Y", action="ALLOW", trust_tier=1, depends_on=["X"]
    )
    with pytest.raises(ValueError):
        engine.evaluate([rule_a, rule_b], input_data="circular")
    assert len(engine.audit_log) == 2
    assert engine.audit_log[1].success is False
