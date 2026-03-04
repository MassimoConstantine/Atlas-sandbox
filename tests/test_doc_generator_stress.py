"""Stress tests for the Atlas doc generator with edge-case Python files."""

from pathlib import Path

from src.doc_generator import generate_file_doc, generate_node_doc
from src.node_parser import parse_file

FIXTURES = Path(__file__).parent / "fixtures"
EDGE_CASE = FIXTURES / "edge_case_node.py"


def test_class_no_docstring_does_not_crash() -> None:
    """Node class with no docstring — methods are extracted without crashing."""
    nodes = parse_file(EDGE_CASE)
    process_node = [n for n in nodes if n.name == "process"]
    assert len(process_node) == 1
    doc = generate_node_doc(process_node[0])
    assert "# Node: process" in doc
    assert "Process data and return result" in doc


def test_class_no_methods_minimal_output() -> None:
    """Node class with only __init__ (private) — no public nodes extracted from it."""
    nodes = parse_file(EDGE_CASE)
    names = [n.name for n in nodes]
    # __init__ starts with '_', so it should be skipped
    assert "__init__" not in names
    # ClassNoMethods has no public methods, so nothing from it appears
    # (process belongs to ClassNoDocstring, not ClassNoMethods)


def test_20_methods_all_documented() -> None:
    """Node with 20 methods — all are extracted and documented."""
    nodes = parse_file(EDGE_CASE)
    method_nodes = [n for n in nodes if n.name.startswith("method_")]
    assert len(method_nodes) == 20

    doc = generate_file_doc(EDGE_CASE)
    for i in range(1, 21):
        method_name = f"method_{i:02d}"
        assert f"# Node: {method_name}" in doc


def test_10_parameters_all_listed() -> None:
    """Method with 10 parameters — all names and types appear in output."""
    nodes = parse_file(EDGE_CASE)
    func = [n for n in nodes if n.name == "many_params_func"][0]
    assert len(func.params) == 10

    doc = generate_node_doc(func)
    expected_params = [
        ("alpha", "str"),
        ("beta", "int"),
        ("gamma", "float"),
        ("delta", "bool"),
        ("epsilon", "list[str]"),
        ("zeta", "dict[str, int]"),
        ("eta", "tuple[int, ...]"),
        ("theta", "bytes"),
        ("iota", "set[str]"),
        ("kappa", "Optional[str]"),
    ]
    for name, type_hint in expected_params:
        assert f"| {name} |" in doc
        assert type_hint in doc


def test_special_markdown_chars_in_docstring() -> None:
    """Docstring with special markdown characters — present in generated doc."""
    nodes = parse_file(EDGE_CASE)
    func = [n for n in nodes if n.name == "markdown_danger_func"][0]
    doc = generate_node_doc(func)

    # All special chars should appear in the output (passed through as-is)
    assert "*bold*" in doc
    assert "**double bold**" in doc
    assert "`code`" in doc
    assert "# heading-like" in doc
    assert "| pipe |" in doc
    assert "| Column A |" in doc


def test_multiple_inheritance_methods_extracted() -> None:
    """Class with multiple bases — methods are still found and documented."""
    nodes = parse_file(EDGE_CASE)
    do_work = [n for n in nodes if n.name == "do_work"]
    assert len(do_work) == 1

    doc = generate_node_doc(do_work[0])
    assert "# Node: do_work" in doc
    assert "Perform a task using multi-base capabilities" in doc
    assert "task" in doc
    assert "str" in doc


def test_empty_file_produces_minimal_output(tmp_path: Path) -> None:
    """Empty Python file — produces minimal 'No public node functions found' output."""
    empty_file = tmp_path / "empty_module.py"
    empty_file.write_text("", encoding="utf-8")

    nodes = parse_file(empty_file)
    assert nodes == []

    doc = generate_file_doc(empty_file)
    assert "No public node functions found" in doc


def test_init_complex_types_skipped_public_method_found() -> None:
    """__init__ with complex type hints is skipped; public method is found."""
    nodes = parse_file(EDGE_CASE)
    names = [n.name for n in nodes]

    # __init__ is private — must be skipped
    assert "__init__" not in names

    # Public method 'run' should be found with its complex types
    run_node = [n for n in nodes if n.name == "run"]
    assert len(run_node) == 1

    run = run_node[0]
    assert run.params[0].name == "payload"
    assert "dict[str, Union[str, list[int]]]" in (run.params[0].type_hint or "")
    assert run.return_type is not None
    assert "Optional" in run.return_type

    doc = generate_node_doc(run)
    assert "# Node: run" in doc
    assert "dict[str, Union[str, list[int]]]" in doc
