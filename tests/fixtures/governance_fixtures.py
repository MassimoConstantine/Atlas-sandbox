"""Shared pytest fixtures for governance edge case tests."""

import pytest

from src.governance_edge_cases import GovernanceEngine, GovernanceRule


@pytest.fixture()
def engine() -> GovernanceEngine:
    """Provide a fresh GovernanceEngine instance for each test."""
    return GovernanceEngine()


@pytest.fixture()
def tier0_block_rule() -> GovernanceRule:
    """A tier 0 BLOCK rule (highest authority)."""
    return GovernanceRule(
        rule_id="tier0-block",
        action="BLOCK",
        priority=10,
        trust_tier=0,
    )


@pytest.fixture()
def tier3_allow_rule() -> GovernanceRule:
    """A tier 3 ALLOW rule (lower authority)."""
    return GovernanceRule(
        rule_id="tier3-allow",
        action="ALLOW",
        priority=10,
        trust_tier=3,
    )


@pytest.fixture()
def tier4_allow_rule() -> GovernanceRule:
    """A tier 4 ALLOW rule (lowest authority)."""
    return GovernanceRule(
        rule_id="tier4-allow",
        action="ALLOW",
        priority=10,
        trust_tier=4,
    )


@pytest.fixture()
def tier2_block_rule() -> GovernanceRule:
    """A tier 2 BLOCK rule."""
    return GovernanceRule(
        rule_id="tier2-block",
        action="BLOCK",
        priority=5,
        trust_tier=2,
    )


@pytest.fixture()
def tier3_block_rule() -> GovernanceRule:
    """A tier 3 BLOCK rule."""
    return GovernanceRule(
        rule_id="tier3-block",
        action="BLOCK",
        priority=5,
        trust_tier=3,
    )
