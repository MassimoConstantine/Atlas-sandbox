"""Adversarial stress tests for the Atlas GovernanceEngine.

Run 07 variant: push the engine beyond normal edge cases with scale,
boundary conditions, and adversarial inputs.
"""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from src.governance_edge_cases import GovernanceEngine, GovernanceRule, GovernanceVerdict


@pytest.fixture()
def engine() -> GovernanceEngine:
    """Provide a fresh GovernanceEngine for each stress test."""
    return GovernanceEngine()


def test_100_rules_correct_precedence(engine: GovernanceEngine) -> None:
    """100 rules evaluated — the single tier-0 rule wins over 99 higher-tier rules."""
    rules: list[GovernanceRule] = []
    # 99 BLOCK rules at tiers 1-4
    for i in range(99):
        rules.append(
            GovernanceRule(
                rule_id=f"block-{i:03d}",
                action="BLOCK",
                priority=i,
                trust_tier=(i % 4) + 1,  # tiers 1-4
            )
        )
    # One tier-0 ALLOW with low priority
    rules.append(
        GovernanceRule(
            rule_id="tier0-allow",
            action="ALLOW",
            priority=0,
            trust_tier=0,
        )
    )
    result = engine.evaluate(rules, input_data="scale-test")
    assert result.decision == "ALLOW"
    assert result.trust_tier == 0
    assert "tier0-allow" in result.reason


def test_effective_date_exactly_now_is_active(engine: GovernanceEngine) -> None:
    """Rule with effective_date exactly equal to now (boundary) is treated as active.

    The engine uses `<=` comparison, so a rule effective at this instant should be included.
    """
    now = datetime.now(timezone.utc)
    rule = GovernanceRule(
        rule_id="exact-now",
        action="BLOCK",
        priority=10,
        trust_tier=0,
        effective_date=now,
    )
    active = engine.get_active_rules([rule])
    assert len(active) == 1
    assert active[0].rule_id == "exact-now"


def test_confidence_upper_boundary() -> None:
    """Verdict with confidence=1.0 is valid and flagged as reliable."""
    verdict = GovernanceVerdict(
        decision="ALLOW",
        confidence=1.0,
        reason="max confidence",
        trust_tier=0,
    )
    assert verdict.confidence == 1.0
    assert verdict.is_reliable is True


def test_confidence_near_zero_boundary() -> None:
    """Verdict with confidence=0.001 is valid and still flagged as reliable (>0)."""
    verdict = GovernanceVerdict(
        decision="BLOCK",
        confidence=0.001,
        reason="near-zero confidence",
        trust_tier=2,
    )
    assert verdict.confidence == 0.001
    assert verdict.is_reliable is True


def test_confidence_above_max_rejected() -> None:
    """Verdict with confidence > 1.0 is rejected by Pydantic validation."""
    with pytest.raises(ValidationError):
        GovernanceVerdict(
            decision="ALLOW",
            confidence=1.01,
            reason="over max",
            trust_tier=0,
        )


def test_all_block_one_tier0_allow_wins(engine: GovernanceEngine) -> None:
    """Engine with all BLOCK rules and one tier-0 ALLOW — ALLOW wins.

    Tier-0 has lowest trust_tier value, so it takes precedence regardless
    of how many BLOCK rules exist at higher tiers.
    """
    block_rules = [
        GovernanceRule(
            rule_id=f"block-t{tier}",
            action="BLOCK",
            priority=100,
            trust_tier=tier,
        )
        for tier in range(1, 5)
    ]
    allow_rule = GovernanceRule(
        rule_id="tier0-allow",
        action="ALLOW",
        priority=1,  # low priority — tier still wins
        trust_tier=0,
    )
    result = engine.evaluate([*block_rules, allow_rule], input_data="allow-wins")
    assert result.decision == "ALLOW"
    assert result.trust_tier == 0


def test_audit_log_order_rapid_sequential(engine: GovernanceEngine) -> None:
    """Audit log preserves insertion order across 50 rapid sequential evaluations."""
    for i in range(50):
        rule = GovernanceRule(
            rule_id=f"rapid-{i:03d}",
            action="ALLOW" if i % 2 == 0 else "BLOCK",
            priority=i,
            trust_tier=1,
        )
        engine.evaluate([rule], input_data=f"seq-{i}")

    assert len(engine.audit_log) == 50
    # Verify order by checking input_summary matches sequence
    for i, entry in enumerate(engine.audit_log):
        assert entry.input_summary == f"seq-{i}"
        assert entry.success is True


def test_empty_string_rule_id_handled(engine: GovernanceEngine) -> None:
    """Rule with empty string rule_id is accepted and processed gracefully."""
    rule = GovernanceRule(
        rule_id="",
        action="BLOCK",
        priority=10,
        trust_tier=0,
    )
    result = engine.evaluate([rule], input_data="empty-id-test")
    assert result.decision == "BLOCK"
    assert result.trust_tier == 0


def test_empty_reason_string_valid() -> None:
    """GovernanceVerdict with empty reason string is valid (reason defaults to '')."""
    verdict = GovernanceVerdict(
        decision="ALLOW",
        confidence=0.5,
        reason="",
        trust_tier=1,
    )
    assert verdict.reason == ""
    assert verdict.decision == "ALLOW"


def test_duplicate_detection_identical_except_rule_id(
    engine: GovernanceEngine,
) -> None:
    """Rules identical in content but with different rule_ids are all kept.

    Deduplication is by rule_id only, so structurally identical rules
    with distinct IDs must all survive.
    """
    rules = [
        GovernanceRule(
            rule_id=f"clone-{i}",
            action="BLOCK",
            priority=5,
            trust_tier=2,
        )
        for i in range(5)
    ]
    deduped = engine.deduplicate_rules(rules)
    assert len(deduped) == 5
    assert {r.rule_id for r in deduped} == {f"clone-{i}" for i in range(5)}
