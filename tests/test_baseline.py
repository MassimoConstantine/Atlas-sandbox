"""Baseline tests that verify the Atlas Sandbox project structure is intact."""

from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent


def test_claude_md_exists():
    """CLAUDE.md must exist at repo root."""
    assert (REPO_ROOT / "CLAUDE.md").is_file()


def test_readme_exists():
    """README.md must exist at repo root."""
    assert (REPO_ROOT / "README.md").is_file()


def test_pyproject_toml_exists():
    """pyproject.toml must exist at repo root."""
    assert (REPO_ROOT / "pyproject.toml").is_file()


def test_gitignore_exists():
    """.gitignore must exist at repo root."""
    assert (REPO_ROOT / ".gitignore").is_file()


def test_scope_boundary_exists():
    """docs/scope-boundary.md must exist."""
    assert (REPO_ROOT / "docs" / "scope-boundary.md").is_file()


def test_src_package_exists():
    """src/ directory must exist with __init__.py."""
    assert (REPO_ROOT / "src").is_dir()
    assert (REPO_ROOT / "src" / "__init__.py").is_file()


def test_src_imports():
    """src package must be importable."""
    import src  # noqa: F401


def test_tests_directory_exists():
    """tests/ directory must exist with __init__.py."""
    assert (REPO_ROOT / "tests").is_dir()
    assert (REPO_ROOT / "tests" / "__init__.py").is_file()


TASK_FILES = [
    "task_01_ledger_cli.md",
    "task_02_governance_tests.md",
    "task_03_schema_validator.md",
    "task_04_doc_generator.md",
    "task_05_model_linter.md",
]


def test_tasks_directory_exists():
    """tasks/ directory must exist."""
    assert (REPO_ROOT / "tasks").is_dir()


def test_all_task_files_exist():
    """Every defined task file must exist in tasks/."""
    for task_file in TASK_FILES:
        path = REPO_ROOT / "tasks" / task_file
        assert path.is_file(), f"Missing task file: {task_file}"


def test_all_task_files_non_empty():
    """Every task file must have content (not be empty)."""
    for task_file in TASK_FILES:
        path = REPO_ROOT / "tasks" / task_file
        content = path.read_text(encoding="utf-8")
        assert len(content.strip()) > 0, f"Task file is empty: {task_file}"


def test_task_files_have_acceptance_criteria():
    """Every task file must contain an Acceptance Criteria section with checkboxes."""
    for task_file in TASK_FILES:
        path = REPO_ROOT / "tasks" / task_file
        content = path.read_text(encoding="utf-8")
        assert "## Acceptance Criteria" in content, (
            f"Missing 'Acceptance Criteria' section in {task_file}"
        )
        assert "- [ ]" in content, f"No checkboxes found in {task_file}"


def test_docs_directory_exists():
    """docs/ directory must exist."""
    assert (REPO_ROOT / "docs").is_dir()
