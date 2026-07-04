```json
{
  "title": "Python coding rules",
  "artifact_type": "implementation-policy",
  "status": "draft",
  "datetime": "20260704.123845",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "scope": "Python implementation in projectkoios-bootstrap",
  "owner": "VULCAN",
  "review_roles": ["KOIOS", "ATHENA"],
  "controls": ["src/python/", "tests/"],
  "does_not_control": ["architecture decisions", "product domain policy", "non-Python implementation"]
}
```

# Python coding rules

## Status

Draft implementation policy.

## Purpose

This document defines Python coding rules for Vulcan-owned implementation work in `projectkoios-bootstrap`.

Python test and validation rules live in `docs/policies/python-testing.md`.

The key words `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, and `MAY` are normative.

## Scope

These rules apply to Python code under:

- `src/python/`
- `tests/`

These rules apply to existing Python implementation, new Python implementation, and touched Python code. Existing code that does not meet the rules is remediation work, not an accepted exception.

These rules do not create architecture authority. Architecture and specification authority remains with ATHENA-owned artifacts and accepted repo policy.

## General principles

- Python code MUST be small, explicit, and testable.
- Python code MUST prefer readability over cleverness.
- Python code MUST keep implementation details aligned with the controlling plan, brief, ADR, or accepted work item.
- Python code MUST NOT widen architecture scope to solve an implementation problem without a rebrief or explicit user approval.
- Python code SHOULD use standard library functionality before adding dependencies.
- Python code MUST NOT introduce runtime side effects at import time unless the module is explicitly an executable entrypoint.

## Module structure

- Modules SHOULD have one clear responsibility.
- Modules SHOULD keep data objects, action objects, and CLI adapters separate when the distinction is meaningful.
- CLI modules MUST be thin adapters over application/service objects.
- Application/service objects SHOULD orchestrate collaborators rather than embed unrelated parsing, I/O, and formatting logic in one method.
- Public module exports SHOULD be explicit when the package is used as an API surface.
- New modules MUST be placed under the existing package hierarchy unless the implementation source artifact explicitly requires a new package.

## Types and data modeling

- Python code MUST use type annotations for public functions, methods, dataclass fields, and variables.
- New Python code SHOULD use `from __future__ import annotations`.
- Structured data SHOULD use `@dataclass(frozen=True, slots=True)` when mutation is not required.
- Runtime enums SHOULD use `StrEnum` when values cross config, CLI, JSON, YAML, or other text boundaries.
- Code MUST NOT use untyped dictionaries as durable domain objects when a dataclass or explicit schema would make the contract clearer.
- Local variables inside functions and methods MUST have explicit type annotations when introduced.
- Local variables inside functions and methods MUST have nearby comments explaining their purpose unless the variable is a simple loop/index variable or an immediately returned value whose purpose is obvious from the expression.
- Local variable annotations inside functions and methods MUST NOT use `Any`.
- Function and method return values MUST be statically checked against their declared return types during validation.
- Code MUST NOT use private functions, private methods, private attributes, private variables, or private constants with leading underscores, excluding Python dunder names.
- Optional values MUST be represented explicitly with `T | None`.
- Action objects SHOULD consume and produce the relevant data objects for their operation rather than bypassing the data model with parallel primitive arguments.
- If an action object cannot use the existing data object cleanly, the implementation SHOULD revise the data object boundary or record the mismatch in the implementation report.

## Naming

- Class names SHOULD name the concept directly and SHOULD NOT include redundant project prefixes inside a project-scoped package.
- Names MUST distinguish data objects from action/service objects when both exist.
- Test names SHOULD describe the behavior under test using the repository's current test naming convention.
- File and module names SHOULD be lower-case and descriptive.
- Abbreviations SHOULD be avoided unless they are established in the surrounding code or source artifact.

## Configuration

- Variable behavior SHOULD be expressed in config rather than hardcoded in implementation code.
- Config-loaded enumerated values MUST be validated before use.
- Defaults MUST be explicit and discoverable.
- Config overlays MUST follow the repository's explicit replacement rule when used.
- Code MUST fail before ingest or mutation when config is malformed and strict validation is enabled.

## I/O and persistence

- File reads and writes MUST use `pathlib.Path` unless a library API requires otherwise.
- Text file reads and writes MUST specify `encoding="utf-8"`.
- Persisted JSON artifacts MUST be deterministic when the artifact is intended for review, tests, or reproducible pipeline output.
- Deterministic JSON artifacts SHOULD use stable key ordering and stable collection ordering.
- Implementation code MUST NOT write outside the configured or documented output surface.
- Code SHOULD avoid modifying source files during validation or review operations unless mutation is the explicit purpose of the command.

## Error handling

- Code MUST fail explicitly for unsupported modes, unsupported backends, invalid paths, and malformed config.
- Code MUST NOT silently swallow backend, parsing, validation, or persistence failures unless fallback behavior is explicitly configured and tested.
- Code MUST NOT use broad `try` / `except` blocks that convert errors into generic return values such as `None`, `False`, or empty collections.
- Expected recoverable errors SHOULD be represented with explicit result objects, typed domain exceptions, or narrow exception handling at the boundary that can add context and choose a documented fallback.
- Unexpected programmer errors SHOULD be allowed to fail fast after context is attached, rather than being hidden by catch-all handlers.
- Boundary layers such as CLI commands MAY catch typed domain exceptions and convert them into concise user-facing messages and non-zero exit status.
- Exceptions SHOULD include enough context for a reviewer to identify the failing field, file, backend, or path.
- User-facing CLI errors SHOULD be concise and actionable.

## CLI behavior

- CLI commands MUST delegate implementation behavior to reusable application/service objects.
- CLI commands MUST return non-zero exit status on validation or runtime failure.
- CLI commands SHOULD print concise success/failure summaries.
- CLI commands MUST NOT require code edits for normal config-driven operation.
- CLI flags SHOULD map directly to configuration, input, output, or execution mode choices.

## Testing

- New behavior MUST have focused tests.
- Tests MUST avoid external network or model-provider dependencies unless explicitly marked or isolated.
- Tests for deterministic artifacts MUST compare stable serialized output or stable parsed structures.
- Tests SHOULD use temporary directories for generated files.
- Tests SHOULD use fake adapters for backend behavior.
- Regression tests SHOULD be added when fixing a validation, path, serialization, or CLI behavior bug.
- Full validation SHOULD use the repository virtualenv interpreter: `.venv/bin/python3`.
- Python test and validation behavior SHOULD follow `docs/policies/python-testing.md`.

## Formatting and lint posture

- Code SHOULD follow PEP 8 unless local project convention differs.
- Imports SHOULD be grouped as standard library, third-party, then local imports.
- Code SHOULD be formatted by tooling when a formatter is configured.
- Manual formatting comments SHOULD NOT replace configured tooling checks.
- Long functions SHOULD be split when the split improves testability or separates concerns.

## Documentation

- Public classes and functions SHOULD be self-explanatory through names and type signatures.
- Public classes and methods SHOULD have docstrings when they are part of a reusable package surface or are constrained by a source artifact.
- Public class and method docstrings SHOULD be compatible with generated documentation tooling such as Sphinx autodoc or pydoc.
- Docstrings SHOULD use a consistent structured style with sections for arguments, return values, raised exceptions, and important side effects when those apply.
- Docstrings and documentation strings MUST be PEP 257 compliant.
- Documentation comments SHOULD be complete sentences when they explain behavior, constraints, or rationale.
- Docstrings MAY be added when behavior is non-obvious, externally consumed, or constrained by a source artifact.
- Implementation reports MUST list meaningful changed files and validation evidence after a slice lands.
- Inline comments SHOULD explain why a choice exists, not restate what the code says.
- Portions of a method that a human reviewer would have a hard time understanding MUST have inline comments near the relevant code.

## Dependency policy

- New dependencies MUST be justified by the implementation source artifact or by a clear reduction in maintenance risk.
- New dependencies MUST be added to `pyproject.toml` in the appropriate dependency group.
- Code SHOULD prefer standard-library implementations for first-slice prototypes when the missing dependency would become architectural commitment.
- Optional integrations SHOULD be isolated behind adapters.

## Review expectations

- Vulcan SHOULD self-review Python changes against this document before closeout.
- Koios MAY review implementation output for standards conformance and provenance quality.
- Athena MAY validate whether implementation behavior conforms to the controlling brief or architecture artifact.
- Reviewers SHOULD distinguish blocking violations from deferred improvements.

## Non-goals

This document does not define:

- product architecture
- domain modeling policy outside Python implementation
- TypeScript, Rust, or shell coding rules
- acceptance criteria for a specific feature slice
- architecture authority for GraphRAG or other systems

## Promotion path

This draft MAY be promoted into a stronger policy after it is tested against multiple implementation slices.

Repeated exceptions, review findings, or process-capture lessons SHOULD be used to revise this document before promotion.
