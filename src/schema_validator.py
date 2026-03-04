"""Schema validation utility for Atlas pipeline JSON files."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

from pydantic import ValidationError

from src.schemas import SCHEMA_REGISTRY


@dataclass
class ValidationErrorDetail:
    """A single validation error with field path, expected type, and actual value."""

    field_path: str
    expected_type: str
    actual_value: str
    message: str


@dataclass
class ValidationResult:
    """Result of validating a single JSON file."""

    file_path: str
    valid: bool
    errors: list[ValidationErrorDetail] = field(default_factory=list)
    error_message: str = ""


def _extract_errors(exc: ValidationError) -> list[ValidationErrorDetail]:
    """Extract structured error details from a Pydantic ValidationError."""
    details: list[ValidationErrorDetail] = []
    for err in exc.errors():
        field_path = " -> ".join(str(loc) for loc in err["loc"])
        expected = err.get("type", "unknown")
        actual = str(err.get("input", "N/A"))
        details.append(ValidationErrorDetail(
            field_path=field_path,
            expected_type=expected,
            actual_value=actual[:200],
            message=err["msg"],
        ))
    return details


def validate_file(file_path: Path) -> ValidationResult:
    """Validate a single JSON file against the appropriate Pydantic schema.

    The schema is determined by the 'schema_type' field in the JSON data.
    Returns a ValidationResult with error details if validation fails.
    """
    path_str = str(file_path)

    try:
        content = file_path.read_text(encoding="utf-8")
    except OSError as e:
        return ValidationResult(
            file_path=path_str,
            valid=False,
            error_message=f"Could not read file: {e}",
        )

    if not content.strip():
        return ValidationResult(
            file_path=path_str,
            valid=False,
            error_message="File is empty",
        )

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        return ValidationResult(
            file_path=path_str,
            valid=False,
            error_message=f"Invalid JSON: {e}",
        )

    if not isinstance(data, dict):
        return ValidationResult(
            file_path=path_str,
            valid=False,
            error_message="JSON root must be an object",
        )

    schema_type = data.get("schema_type")
    if schema_type is None:
        return ValidationResult(
            file_path=path_str,
            valid=False,
            error_message="Missing 'schema_type' field — cannot determine schema",
        )

    model_class = SCHEMA_REGISTRY.get(schema_type)
    if model_class is None:
        return ValidationResult(
            file_path=path_str,
            valid=False,
            error_message=f"Unknown schema_type: '{schema_type}'",
        )

    try:
        model_class.model_validate(data)
    except ValidationError as e:
        return ValidationResult(
            file_path=path_str,
            valid=False,
            errors=_extract_errors(e),
        )

    return ValidationResult(file_path=path_str, valid=True)


def validate_directory(dir_path: Path) -> list[ValidationResult]:
    """Validate all .json files in a directory."""
    results: list[ValidationResult] = []
    json_files = sorted(dir_path.glob("*.json"))
    for json_file in json_files:
        results.append(validate_file(json_file))
    return results


def format_result(result: ValidationResult) -> str:
    """Format a ValidationResult as human-readable text."""
    lines: list[str] = []
    if result.valid:
        lines.append(f"PASS: {result.file_path}")
    else:
        lines.append(f"FAIL: {result.file_path}")
        if result.error_message:
            lines.append(f"  Error: {result.error_message}")
        for err in result.errors:
            lines.append(
                f"  - {err.field_path}: {err.message} "
                f"(expected: {err.expected_type}, got: {err.actual_value})"
            )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the schema validator CLI."""
    parser = argparse.ArgumentParser(
        description="Validate Atlas JSON files against Pydantic schemas.",
    )
    parser.add_argument(
        "path",
        type=Path,
        help="Path to a JSON file or directory of JSON files",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the schema validator CLI. Returns exit code 0 or 1."""
    parser = build_parser()
    args = parser.parse_args(argv)

    path: Path = args.path

    if path.is_dir():
        results = validate_directory(path)
    elif path.is_file():
        results = [validate_file(path)]
    else:
        print(f"Error: path does not exist: {path}", file=sys.stderr)
        return 1

    for result in results:
        print(format_result(result))

    total = len(results)
    passed = sum(1 for r in results if r.valid)
    failed = total - passed

    print(f"\n{total} files validated, {passed} passed, {failed} failed")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
