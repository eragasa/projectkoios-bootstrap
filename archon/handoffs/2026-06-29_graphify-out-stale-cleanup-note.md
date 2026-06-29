# Task: Document stale graphify-out cleanup for existing clones

## Origin

Pi → Archon.

## Context

`graphify-out/` is now ignored and untracked in `projectkoios-bootstrap`, but existing clones can still retain local stale files after a pull. The repo already tells agents to use graphify first; the remaining gap is user-facing guidance for clearing old local graph output.

## Smallest change

Add a short note in the bootstrap docs (preferably `README.md`, or `doc/architecture.00.md` if that is the canonical place) stating:

- `graphify-out/` is local-only and ignored by git
- fresh clones will not receive it
- existing clones may still have stale local files
- if needed, clean it with `git clean -fdX graphify-out/` or delete the directory manually

## Non-goals

- No new automation
- No bootstrap CLI changes
- No git hook changes
- No behavior change to graphify itself

## Acceptance

- The repo documents the stale-local-state behavior clearly
- The cleanup command is explicit and copy-pastable
- No tracked `graphify-out/` files are reintroduced
