# Code Baseline

## Purpose

This document records code-review policy for Python code touched by Project
Koios review flows.

It is a review baseline, not an implementation plan.

## Authority

- **Vulcan** owns the coding standard for package implementation work.
- **Koios** performs adversarial code review against that standard, the
  accepted ADR, and obvious review gaps.
- **Athena** validates architecture alignment against the ADR.
- **Tooling** handles mechanical formatting and linting where possible.

Koios review is intentionally adversarial and bounded. Koios may flag obvious
style, documentation, type, test, traceability, and ADR-alignment issues, but
Koios must not invent implementation standards from scratch.

## Code Principles

### CP-005: PEP 8 Style Compliance

Python code should follow PEP 8 style conventions.

Formatting, imports, naming, and line length should be enforced with project
tooling where possible.

Preferred tools:

- `ruff`
- `ruff format`
- `black`
- `mypy` or `pyright`
- `pytest`

The review should not spend human attention on formatting issues that tooling
can fix automatically.

### CP-006: Public Code Documentation

All public modules, classes, functions, methods, and CLI entry points should
have docstrings.

Docstrings should explain:

- purpose
- parameters
- return values
- raised exceptions
- side effects
- mutation behavior
- I/O behavior
- important invariants

The required documentation level depends on visibility:

| code type | documentation requirement |
|---|---|
| public module | module docstring required |
| public class | class docstring required |
| public function/method | function docstring required |
| CLI command | command behavior and arguments documented |
| private helper | docstring required only if logic is nontrivial |
| test function | descriptive test name usually sufficient |
| architecture-sensitive code | docstring or comment explaining the invariant |
| adapter code | docstring must identify the external dependency and boundary |

Private helpers may have shorter documentation, but nontrivial private logic
must still be understandable.

Use comments to explain why something is done, not to restate what the code
already says.

### CP-007: Type Annotations

Public functions and methods should have explicit type annotations.

Schema objects, workflow objects, action objects, and adapter boundaries should
be typed.

Avoid untyped dictionaries for domain objects when a typed model would clarify
the boundary.

### CP-008: Examples For Public APIs

Important public APIs should include at least one of:

- a docstring example
- a test that functions as an executable example
- a short usage note in documentation

For Project Koios, tests are preferred as executable documentation.

### CP-009: Separate Data Objects From Action Objects

Implementation should preserve the separation between state-bearing data
objects and state-transforming action objects.

### CP-010: Avoid Dangling Functions

Functions that mutate state or affect control surfaces should have explicit
ownership, typed inputs, and clear names. Avoid unowned helper functions that
blur the control surface.

## Documentation And Style Review Rules

Review agents should check whether Python code is PEP 8 compliant.

Review agents should check whether public modules, classes, functions, methods,
and CLI entry points are documented.

Review agents should check whether docstrings identify mutation, I/O,
exceptions, parameters, return values, and invariants.

Review agents should prefer automated tooling for formatting and linting. They
should not produce excessive review comments for issues that `ruff`, `black`, or
a formatter can fix.

Review agents should flag missing documentation when the code is public,
architecture-sensitive, mutating, adapter-facing, or nontrivial.

Review agents should also check whether control-surface code preserves the
boundary between data objects and action objects.

## Review Template Additions

### C5: PEP 8 And Tooling

Result: pass / concern / fail / unknown

Evidence:

Tool result:

Required change:

### C6: Public Documentation

Result: pass / concern / fail / unknown

Evidence:

Missing docstrings:

Missing parameter documentation:

Missing return-value documentation:

Missing exception documentation:

Missing side-effect, mutation, or I/O documentation:

Required change:

### C7: Type Annotations

Result: pass / concern / fail / unknown

Evidence:

Missing or weak annotations:

Required change:

### C8: Public Examples

Result: pass / concern / fail / unknown

Evidence:

Example gap:

Required change:

## Default Docstring Shape

```python
def dry_run(self, state: WorkflowState, action_id: ActionId) -> DryRunResult:
    """Evaluate an action without mutating workflow state.

    Parameters
    ----------
    state
        Current workflow state.
    action_id
        Identifier of the action to evaluate.

    Returns
    -------
    DryRunResult
        Proposed state delta, failed guards, required permissions, and
        provenance preview.

    Raises
    ------
    UnknownActionError
        If `action_id` is not defined in the workflow specification.

    Notes
    -----
    This method must not mutate `state`.
    """
```

## Summary Rule

```text
PEP 8 is enforced by tooling.
Documentation is enforced by review.
Architecture-sensitive behavior must be documented explicitly.
```
