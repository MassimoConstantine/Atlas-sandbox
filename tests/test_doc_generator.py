"""Tests for the Atlas node documentation generator."""

from pathlib import Path

from src.doc_generator import build_parser, generate_file_doc, generate_node_doc, write_docs
from src.node_parser import parse_file

FIXTURES = Path(__file__).parent / "fixtures"
SAMPLE_NODE = FIXTURES / "sample_node.py"
EXPECTED_DOC = FIXTURES / "expected_node_doc.md"


def test_extracts_function_name_and_docstring():
    """Generator extracts function name and docstring correctly."""
    nodes = parse_file(SAMPLE_NODE)
    first = nodes[0]
    assert first.name == "validate_input"
    assert first.docstring is not None
    assert "Validate incoming pipeline data" in first.docstring


def test_extracts_parameter_types():
    """Generator extracts parameter types from type hints."""
    nodes = parse_file(SAMPLE_NODE)
    validate_node = nodes[0]
    param_types = {p.name: p.type_hint for p in validate_node.params}
    assert param_types["data"] == "dict"
    assert param_types["strict"] == "bool"


def test_handles_no_docstring():
    """Generator handles function with no docstring (produces 'Undocumented' marker)."""
    nodes = parse_file(SAMPLE_NODE)
    undoc = [n for n in nodes if n.name == "undocumented_node"][0]
    assert undoc.docstring is None
    doc = generate_node_doc(undoc)
    assert "Undocumented" in doc


def test_handles_no_type_hints():
    """Generator handles function with no type hints gracefully."""
    nodes = parse_file(SAMPLE_NODE)
    no_types = [n for n in nodes if n.name == "no_types_node"][0]
    for param in no_types.params:
        assert param.type_hint is None
    doc = generate_node_doc(no_types)
    assert "Not specified" in doc


def test_output_matches_expected_template():
    """Output markdown matches expected template structure."""
    generated = generate_file_doc(SAMPLE_NODE)
    expected = EXPECTED_DOC.read_text(encoding="utf-8")
    # Normalize trailing whitespace for comparison
    gen_lines = [line.rstrip() for line in generated.strip().splitlines()]
    exp_lines = [line.rstrip() for line in expected.strip().splitlines()]
    assert gen_lines == exp_lines


def test_multiple_functions_all_documented():
    """Multiple functions in one file are all documented."""
    nodes = parse_file(SAMPLE_NODE)
    names = [n.name for n in nodes]
    assert "validate_input" in names
    assert "transform_payload" in names
    assert "undocumented_node" in names
    assert "no_types_node" in names
    assert len(nodes) == 4


def test_skips_private_functions():
    """Generator skips private functions (prefixed with '_')."""
    nodes = parse_file(SAMPLE_NODE)
    names = [n.name for n in nodes]
    assert "_private_helper" not in names


def test_output_dir_flag(tmp_path):
    """CLI --output-dir flag works correctly and generates files."""
    parser = build_parser()
    args = parser.parse_args([str(SAMPLE_NODE), "--output-dir", str(tmp_path)])
    assert args.output_dir == tmp_path

    created = write_docs(SAMPLE_NODE, tmp_path)
    assert len(created) == 1
    assert created[0].name == "sample_node.md"
    assert created[0].exists()
    content = created[0].read_text(encoding="utf-8")
    assert "# Node: validate_input" in content
