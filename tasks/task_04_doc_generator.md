# Task 04: Node Documentation Generator

## Description

Build a documentation generator that reads Atlas pipeline node configuration files (Python modules defining node functions, their inputs, outputs, and governance rules) and produces structured markdown documentation for each node. The generator extracts docstrings, type hints, input/output schemas, and governance metadata to create a standardized reference document. This automates the maintenance of pipeline documentation so it stays in sync with code.

## Acceptance Criteria

- [ ] Reads Python source files and extracts function signatures, docstrings, and type hints
- [ ] Generates one markdown file per node with: name, description, inputs, outputs, governance rules
- [ ] Handles missing docstrings gracefully (marks as "undocumented" rather than crashing)
- [ ] Output markdown follows a consistent template format
- [ ] Supports a `--output-dir` flag to specify where generated docs are written (within `src/` or `tests/`)

## Files to Create

- `src/doc_generator.py` — Main generator logic and CLI entry point
- `src/node_parser.py` — AST-based Python source file parser
- `tests/test_doc_generator.py` — Generator output tests
- `tests/fixtures/sample_node.py` — Sample node config file for testing
- `tests/fixtures/expected_node_doc.md` — Expected markdown output for comparison

## Files NOT to Touch

- `CLAUDE.md`
- `docs/scope-boundary.md`
- `tasks/` (any file)
- `pyproject.toml`
- `tests/test_baseline.py`

## Tests Required

- Test: Generator extracts function name and docstring correctly
- Test: Generator extracts parameter types from type hints
- Test: Generator handles function with no docstring (produces "undocumented" marker)
- Test: Generator handles function with no type hints gracefully
- Test: Output markdown matches expected template structure
- Test: Multiple functions in one file are all documented
- Test: Generator skips private functions (prefixed with `_`)
- Test: CLI `--output-dir` flag works correctly

## Estimated Effort

3-4 hours
