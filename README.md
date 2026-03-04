# Atlas Sandbox

Controlled sandbox environment for Atlas-supervised autonomous AI agent runs.

## Purpose

This repo provides isolated, self-contained coding tasks that Atlas agents can execute under strict governance boundaries. Each task has explicit acceptance criteria, file scope limits, and required tests.

## Quick Start

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ --tb=short

# Lint
ruff check .
```

## Structure

- `src/` — Agent-writable source code
- `tests/` — Agent-writable tests
- `tasks/` — Read-only task definitions (5 tasks)
- `docs/` — Read-only scope and boundary documentation
- `CLAUDE.md` — Read-only sandbox contract for AI agents

## Rules

See `CLAUDE.md` for the full sandbox contract. See `docs/scope-boundary.md` for explicit allowed/forbidden action lists.

## Tasks

| # | Task | Description |
|---|------|-------------|
| 01 | Ledger CLI | CLI tool for filtering and displaying Ledger events |
| 02 | Governance Tests | Edge case test coverage for governance engine |
| 03 | Schema Validator | Pydantic validation utility for pipeline JSON files |
| 04 | Doc Generator | Markdown documentation generator from node configs |
| 05 | Model Linter | Convention checker for Pydantic models |
