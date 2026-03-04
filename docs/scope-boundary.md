# Scope Boundary — Atlas Sandbox

> This document defines the explicit permission boundary for any agent operating in this sandbox.
> If an action is not listed under **Allowed**, it is **Forbidden** by default.

---

## Allowed Actions

| Action | Scope | Notes |
|--------|-------|-------|
| Create files | `src/` | New modules, packages, utilities |
| Modify files | `src/` | Edit existing source code |
| Create files | `tests/` | New test files, test utilities |
| Modify files | `tests/` | Edit existing test code |
| Run `pytest` | Entire repo | Any pytest invocation |
| Run `ruff check` | Entire repo | Linting only |
| Run `ruff check --fix` | Entire repo | Auto-fix safe issues |
| Read files | Entire repo | Any file can be read |
| Create directories | `src/`, `tests/` | Subdirectories for organization |

---

## Forbidden Actions

| Action | Scope | Reason |
|--------|-------|--------|
| Delete any file | Entire repo | Sandbox is append/modify only — no deletions |
| External API calls | Any | No network access permitted |
| HTTP requests | Any | No outbound connections |
| Modify `CLAUDE.md` | Root | Immutable sandbox contract |
| Modify files in `docs/` | `docs/` | Documentation is read-only |
| Modify files in `tasks/` | `tasks/` | Task definitions are read-only |
| Modify `pyproject.toml` | Root | Project config is locked |
| Write outside sandbox | Outside `src/`, `tests/` | Strict directory containment |
| `git push` | Any | Requires explicit human approval |
| Install packages | Any | Only declared dependencies available |
| Run arbitrary shell commands | Any | Only `pytest` and `ruff` permitted |
| Access environment variables | Any | No env var reads for secrets/config |
| Spawn subprocesses | Any | Beyond pytest/ruff execution |

---

## Escalation

If a task requires an action not covered by the Allowed list:

1. **Stop** — do not attempt the action
2. **Document** — note what action was needed and why
3. **Wait** — human review is required before proceeding

---

## Enforcement

These boundaries are enforced by:
- Atlas governance checks during supervised runs
- Baseline tests that verify structural integrity
- Post-run audits that compare file system state before/after

Violations result in immediate task failure and are logged to the Atlas Ledger.
