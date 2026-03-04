"""AST-based Python source file parser for Atlas pipeline node documentation."""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ParamInfo:
    """Information about a single function parameter."""

    name: str
    type_hint: str | None = None


@dataclass
class NodeInfo:
    """Extracted information about a single pipeline node function."""

    name: str
    docstring: str | None = None
    params: list[ParamInfo] = field(default_factory=list)
    return_type: str | None = None
    governance_rules: list[str] = field(default_factory=list)


def _annotation_to_str(annotation: ast.expr | None) -> str | None:
    """Convert an AST annotation node to its string representation."""
    if annotation is None:
        return None
    return ast.unparse(annotation)


def _extract_governance_rules(docstring: str | None) -> list[str]:
    """Extract governance rules from a docstring.

    Looks for a 'Governance:' section with lines starting with '-'.
    """
    if not docstring:
        return []
    rules: list[str] = []
    in_governance = False
    for line in docstring.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("governance:"):
            in_governance = True
            continue
        if in_governance:
            if stripped.startswith("-"):
                rules.append(stripped.lstrip("- ").strip())
            elif stripped == "":
                continue
            else:
                break
    return rules


def parse_function(func_node: ast.FunctionDef) -> NodeInfo:
    """Parse a single AST FunctionDef node into a NodeInfo."""
    docstring = ast.get_docstring(func_node)

    params: list[ParamInfo] = []
    for arg in func_node.args.args:
        if arg.arg == "self":
            continue
        type_hint = _annotation_to_str(arg.annotation)
        params.append(ParamInfo(name=arg.arg, type_hint=type_hint))

    return_type = _annotation_to_str(func_node.returns)
    governance_rules = _extract_governance_rules(docstring)

    return NodeInfo(
        name=func_node.name,
        docstring=docstring,
        params=params,
        return_type=return_type,
        governance_rules=governance_rules,
    )


def parse_file(file_path: Path) -> list[NodeInfo]:
    """Parse a Python source file and extract all public function definitions.

    Private functions (prefixed with '_') are skipped.
    """
    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(file_path))

    nodes: list[NodeInfo] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            nodes.append(parse_function(node))
    return nodes
