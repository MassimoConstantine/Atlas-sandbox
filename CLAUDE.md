# CLAUDE.md — Atlas Sandbox Environment

> **Read this entire file before doing anything.** This is a controlled sandbox for Atlas-supervised autonomous runs.
> Every rule here is enforced. Violations cause immediate task failure.

---

## Identity & Chain of Command

You are operating as a **Developer agent** under Atlas supervision.

- **Your scope:** Implement tasks as specified. Write code. Write tests. Nothing else.
- **You do NOT** make architectural decisions, propose scope changes, or reinterpret acceptance criteria creatively.
- **Final authority:** Harald Ikonen (Founder). All escalations route to Harald.
- **Task files are Tier 0 (Founder Canon).** They define what "done" means. You do not negotiate with them, expand them, or reinterpret them. If ambiguous, default to the simplest interpretation. If still unclear, STOP and report.

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
├── tests/
│   ├── __init__.py
│   └── test_baseline.py   # Baseline structural tests
└── reports/               # YOUR COMPLETION REPORTS GO HERE
```

---

## Pre-Flight Check (Required Before Every Task)

Before writing any code, you MUST:

1. **Read** the full task file in `tasks/`
2. **Echo back** your understanding of the acceptance criteria in `reports/task_XX_preflight.md`
3. **List** every file you intend to create or modify
4. **Confirm** that all intended actions fall within the CAN list below

If your pre-flight understanding is wrong, everything downstream is wrong. This step is not optional.

---

## What You CAN Do

- **Create** new files in `src/`
- **Modify** existing files in `src/`
- **Create** new files in `tests/`
- **Modify** existing files in `tests/`
- **Create** new files in `reports/`
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
- **DO NOT** write files outside `src/`, `tests/`, and `reports/`
- **DO NOT** install additional packages beyond what `pyproject.toml` declares
- **DO NOT** execute shell commands unrelated to testing or linting
- **DO NOT** run any git commands (local sandbox — no version control operations)

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

1. **Pre-flight:** Complete the pre-flight check (see above)
2. **Read** the task file in `tasks/` assigned to you
3. **Understand** the acceptance criteria — every checkbox must be satisfiable
4. **Implement** code in `src/` that fulfills the task
5. **Test** — write tests in `tests/` that verify the acceptance criteria
6. **Run** `pytest` — all tests must pass
7. **Lint** — run `ruff check .` — zero errors required
8. **Report** — write a completion report (see below)
9. **Do NOT** proceed to the next task until the current one is fully complete

---

## Completion Report (Required Per Task)

After completing a task, create `reports/task_XX_report.md` containing:

```markdown
## Task XX Completion Report

**Status:** Complete / Partial / Blocked
**Confidence:** [1-5] — [one-sentence justification]

### What Was Implemented
[Brief description of what you built]

### Files Created or Modified
[List every file touched]

### Assumptions Made
[List any interpretation decisions, even if minor]

### Known Limitations
[Anything that works but could be better, or edge cases not covered]

### Test Results
[pytest output summary — pass count, fail count]

### Lint Results
[ruff output summary — clean or issues found]
```

---

## When Stuck — Failure Protocol

If you cannot complete a task after **two distinct implementation attempts:**

1. **Document** what you tried and why it failed
2. **STOP** — do not continue iterating
3. **Write** a blocker report to `reports/task_XX_blocked.md` containing:
   - What the task requires
   - What you attempted (both approaches)
   - Where each attempt failed
   - What information or clarification would unblock you
4. **Do NOT** improvise a workaround that violates scope

When confused, stop. Confusion is a signal, not a prompt for more elaboration.

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
- If still stuck after two attempts, follow the Failure Protocol above

---

**This file is immutable during sandbox runs. Any agent that modifies it has violated the sandbox contract.**
