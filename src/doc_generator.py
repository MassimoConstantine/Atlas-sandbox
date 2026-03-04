"""Documentation generator for Atlas pipeline node configuration files."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.node_parser import NodeInfo, parse_file


def generate_node_doc(node: NodeInfo) -> str:
    """Generate a markdown section for a single node function."""
    lines: list[str] = []

    lines.append(f"# Node: {node.name}")
    lines.append("")

    # Description
    lines.append("## Description")
    lines.append("")
    if node.docstring:
        # Use only the first paragraph (before governance section) as description
        desc_lines: list[str] = []
        for line in node.docstring.splitlines():
            if line.strip().lower().startswith("governance:"):
                break
            desc_lines.append(line)
        description = "\n".join(desc_lines).strip()
        lines.append(description if description else "Undocumented")
    else:
        lines.append("Undocumented")
    lines.append("")

    # Inputs
    lines.append("## Inputs")
    lines.append("")
    if node.params:
        lines.append("| Parameter | Type |")
        lines.append("|---|---|")
        for param in node.params:
            type_str = param.type_hint if param.type_hint else "Not specified"
            lines.append(f"| {param.name} | {type_str} |")
    else:
        lines.append("No parameters.")
    lines.append("")

    # Outputs
    lines.append("## Outputs")
    lines.append("")
    return_str = node.return_type if node.return_type else "Not specified"
    lines.append(f"**Returns:** {return_str}")
    lines.append("")

    # Governance Rules
    lines.append("## Governance Rules")
    lines.append("")
    if node.governance_rules:
        for rule in node.governance_rules:
            lines.append(f"- {rule}")
    else:
        lines.append("None specified.")
    lines.append("")

    return "\n".join(lines)


def generate_file_doc(file_path: Path) -> str:
    """Generate full markdown documentation for all public nodes in a Python file."""
    nodes = parse_file(file_path)
    if not nodes:
        return f"# {file_path.stem}\n\nNo public node functions found.\n"

    sections: list[str] = []
    for node in nodes:
        sections.append(generate_node_doc(node))

    return "\n---\n\n".join(sections)


def write_docs(source_path: Path, output_dir: Path) -> list[Path]:
    """Generate documentation for a Python source file and write to output directory.

    Returns list of created markdown file paths.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    if source_path.is_file() and source_path.suffix == ".py":
        files = [source_path]
    elif source_path.is_dir():
        files = sorted(source_path.glob("*.py"))
    else:
        return created

    for py_file in files:
        doc_content = generate_file_doc(py_file)
        out_path = output_dir / f"{py_file.stem}.md"
        out_path.write_text(doc_content, encoding="utf-8")
        created.append(out_path)

    return created


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the doc generator CLI."""
    parser = argparse.ArgumentParser(
        description="Generate markdown documentation from Atlas pipeline node files.",
    )
    parser.add_argument(
        "source",
        type=Path,
        help="Path to a Python file or directory of Python files",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory where generated markdown docs will be written",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    """Run the doc generator CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    created = write_docs(args.source, args.output_dir)
    for path in created:
        print(f"Generated: {path}")
    print(f"\n{len(created)} documentation file(s) generated.")


if __name__ == "__main__":
    main()
