"""Stress tests for the Atlas schema validator with extreme inputs."""

from __future__ import annotations

import json
from pathlib import Path

from src.schema_validator import format_result, validate_file

FIXTURES = Path(__file__).parent / "fixtures"


# ---------------------------------------------------------------------------
# Test 1: TaskIntent with all optional fields set to null
# ---------------------------------------------------------------------------

def test_task_intent_null_optional_fields(tmp_path: Path) -> None:
    """TaskIntent has no truly optional fields — setting required fields to null must fail."""
    data = {
        "schema_type": "TaskIntent",
        "task_id": None,
        "intent_type": None,
        "scope": None,
        "constraints": None,
        "acceptance_criteria": None,
        "estimated_effort": None,
        "confidence": None,
    }
    f = tmp_path / "null_fields.json"
    f.write_text(json.dumps(data), encoding="utf-8")

    result = validate_file(f)
    assert result.valid is False
    assert len(result.errors) > 0
    # Each null field should produce an error
    field_paths = [e.field_path for e in result.errors]
    assert any("task_id" in fp for fp in field_paths)
    assert any("scope" in fp for fp in field_paths)
    assert any("confidence" in fp for fp in field_paths)


# ---------------------------------------------------------------------------
# Test 2: TaskIntent with 10000-character strings in every field
# ---------------------------------------------------------------------------

def test_task_intent_10k_char_strings() -> None:
    """TaskIntent with 10,000-character strings in every string field should pass."""
    result = validate_file(FIXTURES / "stress_task_intent.json")
    assert result.valid is True
    assert result.errors == []


# ---------------------------------------------------------------------------
# Test 3: BuildPlan with 50 steps (scale test)
# ---------------------------------------------------------------------------

def test_build_plan_50_steps() -> None:
    """BuildPlan with 50 steps should validate successfully — no list size limits."""
    result = validate_file(FIXTURES / "stress_build_plan.json")
    assert result.valid is True
    assert result.errors == []


# ---------------------------------------------------------------------------
# Test 4: BuildPlan with empty steps list
# ---------------------------------------------------------------------------

def test_build_plan_empty_steps(tmp_path: Path) -> None:
    """BuildPlan with an empty steps list should pass — empty list is valid list[str]."""
    data = {
        "schema_type": "BuildPlan",
        "steps": [],
        "files_to_create": [],
        "files_not_to_touch": [],
        "test_strategy": "none",
    }
    f = tmp_path / "empty_steps.json"
    f.write_text(json.dumps(data), encoding="utf-8")

    result = validate_file(f)
    assert result.valid is True


# ---------------------------------------------------------------------------
# Test 5: Deeply nested JSON (10 levels) in metadata fields
# ---------------------------------------------------------------------------

def test_deeply_nested_json_in_wrong_field(tmp_path: Path) -> None:
    """Passing a deeply nested dict where a string is expected should fail validation."""
    nested: dict | str = "leaf"
    for _ in range(10):
        nested = {"level": nested}

    data = {
        "schema_type": "TaskIntent",
        "task_id": "deep-nest-test",
        "intent_type": nested,  # should be str, not dict
        "scope": ["src/test.py"],
        "constraints": ["none"],
        "acceptance_criteria": ["it works"],
        "estimated_effort": "1 hour",
        "confidence": 3,
    }
    f = tmp_path / "deep_nested.json"
    f.write_text(json.dumps(data), encoding="utf-8")

    result = validate_file(f)
    assert result.valid is False
    field_paths = [e.field_path for e in result.errors]
    assert any("intent_type" in fp for fp in field_paths)


def test_deeply_nested_extra_field_ignored(tmp_path: Path) -> None:
    """Extra fields with deeply nested values are ignored by Pydantic (default mode)."""
    nested: dict | str = "leaf"
    for _ in range(10):
        nested = {"level": nested}

    data = {
        "schema_type": "BuildPlan",
        "steps": ["step 1"],
        "files_to_create": ["src/a.py"],
        "files_not_to_touch": ["CLAUDE.md"],
        "test_strategy": "unit tests",
        "metadata": nested,  # extra field — should be ignored
    }
    f = tmp_path / "deep_extra.json"
    f.write_text(json.dumps(data), encoding="utf-8")

    result = validate_file(f)
    assert result.valid is True


# ---------------------------------------------------------------------------
# Test 6: Unicode/emoji in field values
# ---------------------------------------------------------------------------

def test_unicode_emoji_in_fields(tmp_path: Path) -> None:
    """Unicode and emoji characters in string fields should pass validation."""
    data = {
        "schema_type": "TaskIntent",
        "task_id": "task-\u00fc\u00f1\u00ee\u00e7\u00f6\u00f0\u00e9-42",
        "intent_type": "\U0001f680 rocket launch \U0001f30d",
        "scope": ["\u2603 snowman.py", "\U0001f40d snake.py", "\u4f60\u597d\u4e16\u754c.py"],
        "constraints": ["\u26a0\ufe0f Do NOT touch \U0001f512 locked files"],
        "acceptance_criteria": ["\u2705 All tests pass", "\U0001f3af 100% coverage"],
        "estimated_effort": "\u221e hours \U0001f602",
        "confidence": 5,
    }
    f = tmp_path / "unicode_emoji.json"
    f.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    result = validate_file(f)
    assert result.valid is True
    assert result.errors == []


# ---------------------------------------------------------------------------
# Test 7: Duplicate step IDs in BuildPlan
# ---------------------------------------------------------------------------

def test_build_plan_duplicate_steps(tmp_path: Path) -> None:
    """Duplicate steps in BuildPlan should pass — list[str] allows duplicates."""
    data = {
        "schema_type": "BuildPlan",
        "steps": ["Create models"] * 20,
        "files_to_create": ["src/a.py"] * 10,
        "files_not_to_touch": ["CLAUDE.md", "CLAUDE.md"],
        "test_strategy": "unit tests",
    }
    f = tmp_path / "dupes.json"
    f.write_text(json.dumps(data), encoding="utf-8")

    result = validate_file(f)
    assert result.valid is True


# ---------------------------------------------------------------------------
# Test 8: Schema validation error messages are human-readable
# ---------------------------------------------------------------------------

def test_error_messages_are_human_readable(tmp_path: Path) -> None:
    """Validation errors should produce formatted, human-readable messages."""
    data = {
        "schema_type": "TaskIntent",
        "task_id": 12345,  # wrong type: int instead of str
        "intent_type": "build",
        "scope": "not-a-list",  # wrong type: str instead of list
        "constraints": [],
        "acceptance_criteria": [],
        "estimated_effort": "1h",
        "confidence": 99,  # out of range: must be 1-5
    }
    f = tmp_path / "bad_types.json"
    f.write_text(json.dumps(data), encoding="utf-8")

    result = validate_file(f)
    assert result.valid is False
    assert len(result.errors) >= 2

    formatted = format_result(result)
    # Should contain FAIL prefix
    assert "FAIL" in formatted
    # Should contain field paths
    assert "scope" in formatted
    assert "confidence" in formatted
    # Should not be a raw traceback
    assert "Traceback" not in formatted
    # Each error line should have readable structure
    for err in result.errors:
        assert err.field_path != ""
        assert err.message != ""


# ---------------------------------------------------------------------------
# Bonus: boundary values for confidence field
# ---------------------------------------------------------------------------

def test_confidence_boundary_values(tmp_path: Path) -> None:
    """Confidence field must be 1-5. Test boundary values 0 and 6."""
    base = {
        "schema_type": "TaskIntent",
        "task_id": "boundary-test",
        "intent_type": "test",
        "scope": ["src/x.py"],
        "constraints": [],
        "acceptance_criteria": ["pass"],
        "estimated_effort": "1h",
    }

    for bad_value in [0, 6, -1, 100]:
        data = {**base, "confidence": bad_value}
        f = tmp_path / f"conf_{bad_value}.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        result = validate_file(f)
        assert result.valid is False, f"confidence={bad_value} should fail"
        field_paths = [e.field_path for e in result.errors]
        assert any("confidence" in fp for fp in field_paths)

    # Valid boundaries: 1 and 5
    for good_value in [1, 5]:
        data = {**base, "confidence": good_value}
        f = tmp_path / f"conf_{good_value}.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        result = validate_file(f)
        assert result.valid is True, f"confidence={good_value} should pass"


def test_very_large_json_file(tmp_path: Path) -> None:
    """A valid but very large JSON file (many list items) should still validate."""
    data = {
        "schema_type": "BuildPlan",
        "steps": [f"Step {i}" for i in range(500)],
        "files_to_create": [f"src/gen_{i}.py" for i in range(500)],
        "files_not_to_touch": ["CLAUDE.md"],
        "test_strategy": "Automated",
    }
    f = tmp_path / "large.json"
    f.write_text(json.dumps(data), encoding="utf-8")

    result = validate_file(f)
    assert result.valid is True
