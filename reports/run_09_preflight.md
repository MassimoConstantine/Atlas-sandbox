# Run 09 Pre-Flight Check — Doc Generator Stress Tests (Variant)

## Task Understanding

This is a **variant run**. The doc generator (`src/doc_generator.py`, `src/node_parser.py`) already exists from Run 4. My job is to write **stress tests with edge-case Python files** that exercise the existing implementation without modifying it.

## Acceptance Criteria (from task assignment)

Write minimum 8 test cases:
1. Node class with no docstring — generates doc without crashing
2. Node class with no methods — minimal valid output
3. Node with 20 methods — all documented
4. Method with 10 parameters — all listed
5. Docstring with special markdown characters (`*`, `#`, `|`, `` ` ``) — check output
6. Class inheriting from multiple bases — verify method extraction
7. Empty Python file — produces empty/minimal output
8. Node with `__init__` that has complex type hints (`Optional`, `Union`, `dict[str, list[int]]`)

## Key Observations About Existing Code

- `parse_file` uses `ast.walk` → finds FunctionDef inside classes (methods)
- Names starting with `_` are skipped → `__init__`, `_private_helper` excluded
- Class-level metadata (bases, class docstring) is NOT extracted
- Empty files produce "No public node functions found." message
- Markdown special chars in docstrings are NOT escaped — passed through as-is

## Files to Create

| File | Purpose |
|------|---------|
| `reports/run_09_preflight.md` | This file |
| `tests/fixtures/edge_case_node.py` | Edge-case Python fixture file |
| `tests/test_doc_generator_stress.py` | 8+ stress tests |
| `reports/run_09_report.md` | Completion report |

## Scope Confirmation

- All files within allowed directories (`tests/`, `reports/`)
- No modifications to existing `src/` files
- No deletions
- No external API calls
