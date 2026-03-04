# CLAUDE.md — Atlas Sandbox Environment

> **Read this entire file before doing anything.** This is a controlled sandbox for Atlas-supervised autonomous runs.
> Every rule here is enforced. Violations cause immediate task failure.

---

## What This Repo Is

This is a **sandbox environment** where Atlas supervises autonomous AI agent runs on isolated, self-contained coding tasks. Each task is defined in `tasks/` with explicit acceptance criteria, file boundaries, and test requirements.

The sandbox is intentionally minimal. There are no external dependencies beyond what `pyproject.toml` declares. There is no production data. There is no connection to external services.

---

## Project Structure

```
Atlas-sandbox/
├── CLAUDE.md              # THIS FILE — sandbox rules (DO NOT MODIFY)
├── README.md              # Project overview
├── pyproject.toml         # Python project config
├── .gitignore             # Git ignore rules
├── docs/
│   └── scope-boundary.md  # Explicit allowed/forbidden actions (DO NOT MODIFY)
├── tasks/
│   ├── task_01_ledger_cli.md
│   ├── task_02_governance_tests.md
│   ├── task_03_schema_validator.md
│   ├── task_04_doc_generator.md
│   └── task_05_model_linter.md
├── src/
│   └── __init__.py        # YOUR CODE GOES HERE
└── tests/
    ├── __init__.py
    └── test_baseline.py   # Baseline structural tests
```

---

## What You CAN Do

- **Create** new files in `src/`
- **Modify** existing files in `src/`
- **Create** new files in `tests/`
- **Modify** existing files in `tests/`
- **Run** `pytest` to validate your work
- **Run** `ruff check .` to lint your code
- **Read** any file in the repo

---

## What You CANNOT Do

These are hard boundaries. No exceptions. No workarounds.

- **DO NOT** delete any file — ever
- **DO NOT** make external API calls (no HTTP requests, no network access)
- **DO NOT** modify `CLAUDE.md` (this file)
- **DO NOT** modify anything in `docs/`
- **DO NOT** modify anything in `tasks/`
- **DO NOT** modify `pyproject.toml`
- **DO NOT** write files outside the `src/` and `tests/` directories
- **DO NOT** run `git push` without explicit human approval
- **DO NOT** install additional packages beyond what `pyproject.toml` declares
- **DO NOT** execute shell commands unrelated to testing or linting

---

## How to Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with short traceback
pytest tests/ --tb=short

# Run a specific test file
pytest tests/test_baseline.py -v
```

---

## How to Lint

```bash
# Check for lint errors
ruff check .

# Auto-fix safe lint errors
ruff check . --fix
```

---

## Task Workflow

1. Read the task file in `tasks/` assigned to you
2. Understand the acceptance criteria — every checkbox must be satisfiable
3. Write code in `src/` that implements the task
4. Write tests in `tests/` that verify the acceptance criteria
5. Run `pytest` — all tests must pass
6. Run `ruff check .` — zero errors required
7. Do NOT proceed to the next task until the current one is fully complete

---

## Code Standards

- Python 3.12
- Type hints on all function signatures
- Docstrings on all public functions and classes
- Follow PEP 8 (enforced by ruff)
- Pydantic v2 for all data models
- No global mutable state
- No side effects in module imports

---

## When In Doubt

- If a task is ambiguous, implement the simplest interpretation
- If you are unsure whether an action is allowed, check `docs/scope-boundary.md`
- If the action is not explicitly listed as allowed, do not do it
- If a test fails, fix your code — do not modify the test expectations unless the task explicitly requires new tests

---

**This file is immutable during sandbox runs. Any agent that modifies it has violated the sandbox contract.**
