# AGENTS.md — opencode harness

You are the build and runtime harness for Project Koios. Your job is to
implement code, run tests, run validation, and operate the system.

## Workspace layout

Read `../maps/repositories.md` and `../maps/packages.md` before touching code.
They are the authoritative source for where things live.

All component repos are siblings under `~/repos/`.

## Rules

For codebase, architecture, file-relationship, and impact questions, use `graphify` first. If `graphify-out/graph.json` exists, prefer `graphify query`, `graphify path`, or `graphify explain` before manual grepping or browsing.

Rules in `rules/` are incorporated by reference:
- `rules/build.md` — implementation flow
- `rules/validation.md` — gates to run before finishing
- `rules/specification_gate.md` — consult vs execute
- `rules/handoff.md` — what an implementation-ready handoff must contain
- `rules/tool_policy.md` — permissions
- `rules/session.md` — session start/end protocol

## Checklists

- `checklists/multi-repo-execution-readiness.md` — execution checklist for the approved multi-repo ownership and extraction plan

## Setup per repo

```bash
python3 -m venv --prompt projectkoios-bootstrap .venv && source .venv/bin/activate && pip install -e ".[dev]"
```

## Common commands

| Action | Command |
|--------|---------|
| Run tests | `pytest` |
| Lint | `ruff check .` |
| Typecheck | `mypy src/python` |

## Conventions

- **`from __future__ import annotations`** at top of every module
- **Pydantic at boundaries only** — internal DTOs use `@dataclass(frozen=True)`
- **ruff**: line-length=80, double quotes, lint=E/F/I/UP/B, target py312
- **Tests**: see `doc/testing.md`
