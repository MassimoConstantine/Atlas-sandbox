"""Stress tests with pathological Pydantic models for the model linter."""

from pathlib import Path

import pytest

from src.model_linter import scan_file

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "pathological_models.py"


def _violations_for_model(model_name: str) -> list:
    """Helper: return violations for a specific model from the fixture file."""
    all_violations = scan_file(FIXTURE_PATH)
    return [v for v in all_violations if v.model_name == model_name]


def test_50_field_model_all_linted_correctly():
    """Model with 50 properly defined fields produces zero violations."""
    violations = _violations_for_model("FiftyFieldModel")
    assert violations == []


def test_empty_body_model_handled_gracefully():
    """Model with no fields (empty body, only docstring) produces zero violations."""
    violations = _violations_for_model("EmptyModel")
    assert violations == []


def test_extremely_long_field_name():
    """Field with a 200-character snake_case name is accepted without error."""
    violations = _violations_for_model("LongNameModel")
    assert violations == []


def test_non_base_model_class_skipped():
    """Model inheriting from a non-BaseModel class is skipped entirely by the linter."""
    all_violations = scan_file(FIXTURE_PATH)
    model_names = {v.model_name for v in all_violations}
    assert "NotPydantic" not in model_names


def test_validator_methods_not_flagged():
    """Model with @field_validator methods — validators are not flagged as violations."""
    violations = _violations_for_model("ValidatorModel")
    assert violations == []


def test_nested_model_references_clean():
    """Nested model field references (ChildModel, list[ChildModel]) produce no violations."""
    parent_violations = _violations_for_model("ParentModel")
    child_violations = _violations_for_model("ChildModel")
    assert parent_violations == []
    assert child_violations == []


def test_field_with_alias_description_examples():
    """Model using Field(...) with alias, description, and examples produces no violations."""
    violations = _violations_for_model("AliasModel")
    assert violations == []


def test_syntax_error_file_fails_gracefully(tmp_path):
    """File with syntax errors causes a SyntaxError from ast.parse (documented behavior)."""
    bad_file = tmp_path / "broken.py"
    bad_file.write_text(
        "from pydantic import BaseModel\n"
        "\n"
        "class Broken(BaseModel):\n"
        "    this is not valid python }{{\n",
        encoding="utf-8",
    )
    with pytest.raises(SyntaxError):
        scan_file(bad_file)
