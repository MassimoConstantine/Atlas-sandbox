"""Pydantic model linter — scans Python files for BaseModel convention violations."""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

from src.lint_rules import ALL_RULES, Severity, Violation


def _is_base_model_subclass(node: ast.ClassDef) -> bool:
    """Check if an AST ClassDef node inherits from BaseModel."""
    for base in node.bases:
        if isinstance(base, ast.Name) and base.id == "BaseModel":
            return True
        if isinstance(base, ast.Attribute) and base.attr == "BaseModel":
            return True
    return False


def scan_file(file_path: Path) -> list[Violation]:
    """Scan a Python file for Pydantic model lint violations."""
    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(file_path))

    violations: list[Violation] = []
    path_str = str(file_path)

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and _is_base_model_subclass(node):
            for rule in ALL_RULES:
                violations.extend(rule(node, path_str))

    return violations


def scan_directory(dir_path: Path) -> list[Violation]:
    """Scan all .py files in a directory for Pydantic model lint violations."""
    violations: list[Violation] = []
    for py_file in sorted(dir_path.glob("*.py")):
        violations.extend(scan_file(py_file))
    return violations


def format_violation(violation: Violation) -> str:
    """Format a violation as a human-readable string."""
    return (
        f"{violation.file_path}:{violation.line_number}: "
        f"[{violation.severity.value}] {violation.model_name} — "
        f"{violation.description}"
    )


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the model linter CLI."""
    parser = argparse.ArgumentParser(
        description="Lint Pydantic models for Atlas convention compliance.",
    )
    parser.add_argument(
        "path",
        type=Path,
        help="Path to a Python file or directory to scan",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        default=False,
        help="Treat warnings as errors (affects exit code)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the model linter CLI. Returns exit code 0 or 1."""
    parser = build_parser()
    args = parser.parse_args(argv)

    path: Path = args.path
    strict: bool = args.strict

    if path.is_dir():
        violations = scan_directory(path)
    elif path.is_file():
        violations = scan_file(path)
    else:
        print(f"Error: path does not exist: {path}", file=sys.stderr)
        return 1

    for v in violations:
        print(format_violation(v))

    errors = [v for v in violations if v.severity == Severity.ERROR]
    warnings = [v for v in violations if v.severity == Severity.WARNING]

    print(f"\n{len(violations)} violation(s): {len(errors)} error(s), {len(warnings)} warning(s)")

    if errors:
        return 1
    if strict and warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
