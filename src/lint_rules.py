"""Individual lint rule implementations for Pydantic model checking."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    """Severity level for a lint violation."""

    ERROR = "ERROR"
    WARNING = "WARNING"


@dataclass
class Violation:
    """A single lint violation reported by the model linter."""

    file_path: str
    line_number: int
    model_name: str
    description: str
    severity: Severity = Severity.ERROR


SNAKE_CASE_RE = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)*$")


def check_docstring(
    node: ast.ClassDef, file_path: str,
) -> list[Violation]:
    """Check that a model class has a docstring."""
    docstring = ast.get_docstring(node)
    if not docstring:
        return [Violation(
            file_path=file_path,
            line_number=node.lineno,
            model_name=node.name,
            description="Model class is missing a docstring",
        )]
    return []


def check_field_ordering(
    node: ast.ClassDef, file_path: str,
) -> list[Violation]:
    """Check that required fields come before optional fields."""
    seen_optional = False
    violations: list[Violation] = []
    for stmt in node.body:
        if not isinstance(stmt, ast.AnnAssign):
            continue
        if not isinstance(stmt.target, ast.Name):
            continue
        field_name = stmt.target.id
        has_default = stmt.value is not None
        annotation_str = ast.unparse(stmt.annotation) if stmt.annotation else ""
        is_optional = (
            has_default
            or "Optional" in annotation_str
            or "None" in annotation_str
        )

        if is_optional:
            seen_optional = True
        elif seen_optional:
            violations.append(Violation(
                file_path=file_path,
                line_number=stmt.lineno,
                model_name=node.name,
                description=(
                    f"Required field '{field_name}' appears after an optional field "
                    f"(required fields should come first)"
                ),
                severity=Severity.WARNING,
            ))
    return violations


def check_no_any_type(
    node: ast.ClassDef, file_path: str,
) -> list[Violation]:
    """Check that no field uses the Any type."""
    violations: list[Violation] = []
    for stmt in node.body:
        if not isinstance(stmt, ast.AnnAssign):
            continue
        if not isinstance(stmt.target, ast.Name):
            continue
        if stmt.annotation is None:
            continue
        annotation_str = ast.unparse(stmt.annotation)
        if "Any" in annotation_str:
            violations.append(Violation(
                file_path=file_path,
                line_number=stmt.lineno,
                model_name=node.name,
                description=f"Field '{stmt.target.id}' uses 'Any' type (not allowed)",
            ))
    return violations


def check_snake_case_names(
    node: ast.ClassDef, file_path: str,
) -> list[Violation]:
    """Check that all field names use snake_case."""
    violations: list[Violation] = []
    for stmt in node.body:
        if not isinstance(stmt, ast.AnnAssign):
            continue
        if not isinstance(stmt.target, ast.Name):
            continue
        field_name = stmt.target.id
        if not SNAKE_CASE_RE.match(field_name):
            violations.append(Violation(
                file_path=file_path,
                line_number=stmt.lineno,
                model_name=node.name,
                description=(
                    f"Field '{field_name}' is not snake_case"
                ),
            ))
    return violations


def check_type_hints(
    node: ast.ClassDef, file_path: str,
) -> list[Violation]:
    """Check that all fields have type annotations.

    Detects bare assignments (no annotation) in the class body.
    """
    violations: list[Violation] = []
    for stmt in node.body:
        if isinstance(stmt, ast.Assign):
            for target in stmt.targets:
                if isinstance(target, ast.Name):
                    violations.append(Violation(
                        file_path=file_path,
                        line_number=stmt.lineno,
                        model_name=node.name,
                        description=(
                            f"Field '{target.id}' has no type hint "
                            f"(use annotation: field_name: type = value)"
                        ),
                    ))
    return violations


ALL_RULES = [
    check_docstring,
    check_field_ordering,
    check_no_any_type,
    check_snake_case_names,
    check_type_hints,
]
