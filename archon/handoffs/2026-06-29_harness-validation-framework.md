# Task: Harness validation framework

## Origin

Pi → Archon. The user raised the question "should we have a testing framework to make sure all the harnesses are correct?"

## Context

This repo (`projectkoios-bootstrap`) manages shared agent configs across four harnesses (pi, archon, opencode, goose). Each harness has an `AGENTS.md` that defines its role, scope, and behavior. There are also:

- Root `AGENTS.md` — shared rules, meta-harness framework, routing guide
- `doc/meta-harness.md` — skill model, completion gates, escalation rules
- `agents/global/<harness>/AGENTS.md.example` — example configs
- `opencode/rules/` — granular rule files for opencode
- `opencode/checklists/` — execution checklists

There is currently no automated way to validate that:
- Harness AGENTS.md files are consistent with the root AGENTS.md
- Cross-references (e.g., "see opencode/AGENTS.md") are valid
- Required sections exist per harness type
- The routing guide matches actual harness capabilities
- Agent-specific rules don't contradict shared rules

## What we need

An **architecture-spec** and **acceptance criteria** from archon that defines:

1. **What "correct" means** — what properties should a harness configuration satisfy? (structural, cross-referential, behavioral)
2. **Validation dimensions** — lint-like checks vs. semantic checks vs. behavioral tests
3. **Scope** — which files are in scope (AGENTS.md files, rules/, checklists/, example configs?) and what is out of scope
4. **Tooling approach** — should this be a Python CLI check (extending the existing `projectkoios` bootstrap CLI), a standalone script, or something else?
5. **Failure model** — hard errors vs. warnings vs. informational
6. **Non-goals** — what this framework should explicitly NOT do

## Constraints

- Existing toolchain: Python 3.12, pytest, ruff, mypy
- The `projectkoios.bootstrap` CLI package already exists in `src/python/`
- All harness configs are markdown files
- Harnesses may be read by different agent tools; the validation should be tool-agnostic
- AGENTS.md is the source of truth; do not invent a parallel config format

## Output

Place `architecture-spec` and `acceptance-criteria` artifacts in `archon/handoffs/` for opencode (Vulcan) to implement.
