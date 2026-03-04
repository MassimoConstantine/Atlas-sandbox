"""Governance engine models, helpers, and mock structures for edge-case testing."""

from __future__ import annotations

import concurrent.futures
from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field


class GovernanceVerdict(BaseModel):
    """A governance check verdict with decision, confidence, and reason."""

    decision: Literal["ALLOW", "BLOCK"]
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str = ""
    trust_tier: int = Field(ge=0, le=4)

    @property
    def is_reliable(self) -> bool:
        """Return whether the verdict confidence is above zero."""
        return self.confidence > 0


class GovernanceRule(BaseModel):
    """A single governance rule with priority, tier, and optional dependencies."""

    rule_id: str
    action: Literal["ALLOW", "BLOCK"]
    priority: int = 0
    trust_tier: int = Field(ge=0, le=4)
    effective_date: datetime | None = None
    depends_on: list[str] = Field(default_factory=list)


class AuditEntry(BaseModel):
    """A single entry in the governance audit log."""

    action: str
    input_summary: str
    result: str
    success: bool


class GovernanceEngine:
    """Minimal governance engine for evaluating rules and producing verdicts."""

    def __init__(self) -> None:
        self.audit_log: list[AuditEntry] = []

    def get_active_rules(self, rules: list[GovernanceRule]) -> list[GovernanceRule]:
        """Return only rules whose effective_date is in the past or None."""
        now = datetime.now(timezone.utc)
        return [
            r for r in rules
            if r.effective_date is None or r.effective_date <= now
        ]

    def deduplicate_rules(self, rules: list[GovernanceRule]) -> list[GovernanceRule]:
        """Remove duplicate rules by rule_id, keeping first occurrence."""
        seen: set[str] = set()
        unique: list[GovernanceRule] = []
        for rule in rules:
            if rule.rule_id not in seen:
                seen.add(rule.rule_id)
                unique.append(rule)
        return unique

    def sort_rules(self, rules: list[GovernanceRule]) -> list[GovernanceRule]:
        """Sort rules by priority (desc), then rule_id (asc) for deterministic order."""
        return sorted(rules, key=lambda r: (-r.priority, r.rule_id))

    def detect_circular_deps(self, rules: list[GovernanceRule]) -> None:
        """Detect circular dependencies among rules. Raises ValueError if found."""
        rule_map = {r.rule_id: r for r in rules}

        def visit(rule_id: str, path: set[str]) -> None:
            if rule_id in path:
                raise ValueError(f"Circular dependency detected involving '{rule_id}'")
            if rule_id not in rule_map:
                return
            path.add(rule_id)
            for dep in rule_map[rule_id].depends_on:
                visit(dep, path.copy())

        for rule in rules:
            visit(rule.rule_id, set())

    def evaluate(
        self,
        rules: list[GovernanceRule],
        input_data: Any = None,
    ) -> GovernanceVerdict:
        """Evaluate governance rules and produce a verdict.

        - Empty rule set produces ALLOW (no restrictions).
        - None input_data is handled safely and returns ALLOW.
        - Lower trust tier takes precedence (tier 0 overrides tier 3-4).
        - Within same tier, higher priority wins.
        - BLOCK takes precedence over ALLOW at same tier+priority.
        """
        input_summary = str(input_data)[:100] if input_data is not None else "<None>"

        try:
            if not rules:
                verdict = GovernanceVerdict(
                    decision="ALLOW",
                    confidence=1.0,
                    reason="No rules — default ALLOW",
                    trust_tier=0,
                )
                self._log("evaluate", input_summary, "ALLOW", success=True)
                return verdict

            if input_data is None:
                verdict = GovernanceVerdict(
                    decision="ALLOW",
                    confidence=0.5,
                    reason="None input — safe default",
                    trust_tier=0,
                )
                self._log("evaluate", input_summary, "ALLOW", success=True)
                return verdict

            active = self.get_active_rules(rules)
            active = self.deduplicate_rules(active)
            self.detect_circular_deps(active)
            ordered = self.sort_rules(active)

            if not ordered:
                verdict = GovernanceVerdict(
                    decision="ALLOW",
                    confidence=1.0,
                    reason="No active rules",
                    trust_tier=0,
                )
                self._log("evaluate", input_summary, "ALLOW", success=True)
                return verdict

            # Lower trust tier wins; within tier, higher priority wins;
            # BLOCK wins ties at same tier+priority.
            best = ordered[0]
            for rule in ordered[1:]:
                if rule.trust_tier < best.trust_tier:
                    best = rule
                elif (
                    rule.trust_tier == best.trust_tier
                    and rule.priority > best.priority
                ):
                    best = rule
                elif (
                    rule.trust_tier == best.trust_tier
                    and rule.priority == best.priority
                    and rule.action == "BLOCK"
                ):
                    best = rule

            verdict = GovernanceVerdict(
                decision=best.action,
                confidence=1.0,
                reason=f"Determined by rule '{best.rule_id}'",
                trust_tier=best.trust_tier,
            )
            self._log("evaluate", input_summary, best.action, success=True)
            return verdict

        except Exception as e:
            self._log("evaluate", input_summary, str(e), success=False)
            raise

    def check_with_timeout(
        self,
        handler: Any,
        timeout: float,
    ) -> GovernanceVerdict:
        """Run a governance handler with a timeout. Raises TimeoutError if exceeded."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(handler)
            try:
                result = future.result(timeout=timeout)
            except concurrent.futures.TimeoutError:
                self._log("timeout_check", "handler", "TIMEOUT", success=False)
                raise TimeoutError("Governance check exceeded timeout")
            self._log("timeout_check", "handler", "OK", success=True)
            return result  # type: ignore[return-value]

    def _log(self, action: str, input_summary: str, result: str, *, success: bool) -> None:
        """Record an entry in the audit log."""
        self.audit_log.append(AuditEntry(
            action=action,
            input_summary=input_summary,
            result=result,
            success=success,
        ))
