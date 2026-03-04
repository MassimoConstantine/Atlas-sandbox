## Task 04 Pre-Flight Check

### Acceptance Criteria (echoed from task)

1. Reads Python source files and extracts function signatures, docstrings, and type hints
2. Generates one markdown file per node with: name, description, inputs, outputs, governance rules
3. Handles missing docstrings gracefully (marks as "undocumented" rather than crashing)
4. Output markdown follows a consistent template format
5. Supports a `--output-dir` flag to specify where generated docs are written (within `src/` or `tests/`)

### Files to Create

- `src/node_parser.py` — AST-based Python source file parser
- `src/doc_generator.py` — Main generator logic and CLI entry point
- `tests/fixtures/sample_node.py` — Sample node config file for testing
- `tests/fixtures/expected_node_doc.md` — Expected markdown output for comparison
- `tests/test_doc_generator.py` — 8 generator output tests

### Files NOT to Touch

- `CLAUDE.md`
- `docs/scope-boundary.md`
- `tasks/` (any file)
- `pyproject.toml`
- `tests/test_baseline.py`

### Scope Confirmation

All intended actions (create files in `src/`, `tests/`, `reports/`; run `pytest`; run `ruff`) fall within the CAN list.
