"""Tests for the Atlas schema validator."""

from pathlib import Path

from src.schema_validator import validate_directory, validate_file

FIXTURES = Path(__file__).parent / "fixtures"


def test_valid_task_intent_passes():
    """Valid TaskIntent JSON passes validation with no errors."""
    result = validate_file(FIXTURES / "valid_task_intent.json")
    assert result.valid is True
    assert result.errors == []
    assert result.error_message == ""


def test_invalid_task_intent_fails_with_errors():
    """Invalid TaskIntent JSON fails with correct error messages referencing field paths."""
    result = validate_file(FIXTURES / "invalid_task_intent.json")
    assert result.valid is False
    assert len(result.errors) > 0
    field_paths = [e.field_path for e in result.errors]
    # Should report errors for missing required fields and wrong types
    assert any("intent_type" in fp for fp in field_paths)


def test_valid_build_plan_passes():
    """Valid BuildPlan JSON passes validation with no errors."""
    result = validate_file(FIXTURES / "valid_build_plan.json")
    assert result.valid is True
    assert result.errors == []


def test_invalid_build_plan_fails_with_errors():
    """Invalid BuildPlan JSON fails with correct error messages referencing field paths."""
    result = validate_file(FIXTURES / "invalid_build_plan.json")
    assert result.valid is False
    assert len(result.errors) > 0
    field_paths = [e.field_path for e in result.errors]
    assert any("steps" in fp for fp in field_paths)


def test_missing_schema_type_handled_gracefully():
    """JSON without a schema_type field produces a clear error, not a crash."""
    import json
    import tempfile

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as f:
        json.dump({"task_id": "test", "confidence": 3}, f)
        tmp_path = Path(f.name)

    try:
        result = validate_file(tmp_path)
        assert result.valid is False
        assert "schema_type" in result.error_message
    finally:
        # Do not delete — sandbox rule. File is in temp dir, outside scope.
        pass


def test_batch_validation_reports_correct_counts(tmp_path):
    """Batch validation of a directory reports correct pass/fail counts."""
    import shutil

    # Copy valid and invalid fixtures into tmp_path
    for name in ["valid_task_intent.json", "invalid_task_intent.json"]:
        shutil.copy(FIXTURES / name, tmp_path / name)

    results = validate_directory(tmp_path)
    assert len(results) == 2
    passed = sum(1 for r in results if r.valid)
    failed = sum(1 for r in results if not r.valid)
    assert passed == 1
    assert failed == 1


def test_non_json_file_produces_clear_error(tmp_path):
    """Non-JSON file produces a clear error message, not a stack trace."""
    bad_file = tmp_path / "not_json.json"
    bad_file.write_text("this is not json {{{", encoding="utf-8")

    result = validate_file(bad_file)
    assert result.valid is False
    assert "Invalid JSON" in result.error_message


def test_empty_json_file_reported_as_invalid(tmp_path):
    """Empty JSON file is reported as invalid with a clear message."""
    empty_file = tmp_path / "empty.json"
    empty_file.write_text("", encoding="utf-8")

    result = validate_file(empty_file)
    assert result.valid is False
    assert "empty" in result.error_message.lower()
