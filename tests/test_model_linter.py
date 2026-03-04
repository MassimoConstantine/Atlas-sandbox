"""Tests for the Pydantic model linter."""

from pathlib import Path

from src.lint_rules import Severity
from src.model_linter import main, scan_file

FIXTURES = Path(__file__).parent / "fixtures"
CLEAN = FIXTURES / "clean_models.py"
DIRTY = FIXTURES / "dirty_models.py"


def test_clean_models_zero_violations():
    """Clean models file produces zero violations."""
    violations = scan_file(CLEAN)
    assert violations == []


def test_model_without_docstring_flagged():
    """Model without docstring is flagged."""
    violations = scan_file(DIRTY)
    docstring_violations = [v for v in violations if "docstring" in v.description.lower()]
    assert len(docstring_violations) >= 1
    assert docstring_violations[0].model_name == "BadModel"


def test_optional_before_required_flagged():
    """Model with optional field before required field is flagged."""
    violations = scan_file(DIRTY)
    ordering_violations = [v for v in violations if "optional" in v.description.lower()]
    assert len(ordering_violations) >= 1
    assert ordering_violations[0].severity == Severity.WARNING


def test_any_type_flagged():
    """Field using Any type is flagged."""
    violations = scan_file(DIRTY)
    any_violations = [v for v in violations if "Any" in v.description]
    assert len(any_violations) >= 1


def test_camel_case_name_flagged():
    """Field with camelCase name is flagged."""
    violations = scan_file(DIRTY)
    case_violations = [v for v in violations if "snake_case" in v.description]
    assert len(case_violations) >= 1
    assert any("dataPayload" in v.description for v in case_violations)


def test_field_without_type_hint_flagged():
    """Field without type hint is flagged."""
    violations = scan_file(DIRTY)
    hint_violations = [v for v in violations if "type hint" in v.description.lower()]
    assert len(hint_violations) >= 1
    assert any("untyped" in v.description for v in hint_violations)


def test_strict_flag_changes_exit_code(tmp_path):
    """--strict flag treats warnings as errors, changing exit code."""
    # Create a file with only a WARNING violation (field ordering) but no ERRORs
    model_file = tmp_path / "warn_only.py"
    model_file.write_text(
        'from pydantic import BaseModel\n'
        '\n'
        '\n'
        'class WarnModel(BaseModel):\n'
        '    """Has a docstring."""\n'
        '\n'
        '    optional_field: str = "default"\n'
        '    required_field: str\n',
        encoding="utf-8",
    )

    # Without --strict: only warnings, exit code 0
    exit_code_normal = main([str(model_file)])
    assert exit_code_normal == 0

    # With --strict: warnings become errors, exit code 1
    exit_code_strict = main([str(model_file), "--strict"])
    assert exit_code_strict == 1


def test_non_base_model_classes_skipped():
    """Non-BaseModel classes are skipped by the linter."""
    violations = scan_file(DIRTY)
    model_names = {v.model_name for v in violations}
    assert "RegularClass" not in model_names


def test_report_includes_file_path_and_line_number():
    """Report includes correct file path and line number."""
    violations = scan_file(DIRTY)
    assert len(violations) > 0
    for v in violations:
        assert str(DIRTY) in v.file_path
        assert v.line_number > 0
