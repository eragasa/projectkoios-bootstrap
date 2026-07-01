# ADR 20260630.141231: Archon health PIV session

## Status

historic

## Context

Archon was not healthy enough to run a full Project Koios PIV loop from this
repo without local operator repair. The session started with three concrete
problems:

- `archon` was not reliably available on `PATH`.
- Full workflow validation failed because repo-local Archon MCP runtime config
  expected `.archon/mcp/ntfy.json`, but that file is installation-specific.
- `archon-piv-loop` referenced model names that were not usable in the current
  operator environment.

The user also clarified broader direction during PIV exploration:

- Athena should encapsulate Archon with the Petri-net/meta-harness stack.
- ADR message schema should be deferred until Koios is up and running.
- Human-readable docs should live under a docs-like architecture, with ADRs as
  provenance records and Graphify as the current semantic representation path.
- Dot-prefixed paths are installation-specific, not simply "ignored".

Only the Archon-health bootstrap slice was implemented in this repo during this
session. The broader documentation and schema restructuring remains future
architecture work.

## Decision

Treat Archon health as a bootstrap-owned operational capability and make the
repo validate that capability without committing machine-local runtime state.

Concretely:

1. Keep `.archon/mcp/` local-only and ignored by git.
2. Validate repo-owned Archon assets through
   `projectkoios bootstrap validate-harnesses --root .`.
3. Align harness validation with the current AGENTS.md headings:
   `Hermes (pi)`, `Athena (archon)`, and `Vulcan (opencode)`.
4. Document Archon health checks in README:
   `archon doctor`, `archon validate workflows`, `archon workflow runs`, and
   `archon isolation list`.
5. Pin this repo's PIV workflow model settings to `gpt-5.5` so the workflow
   uses the available Codex path rather than unavailable model aliases or the
   unauthenticated Pi/Anthropic path.
6. Preserve the PIV implementation report as a Vulcan-to-Hermes handoff.
7. When GitHub PR creation is blocked by token scope after validation passes,
   pushing the validated branch to `master` is acceptable with explicit
   reporting.

## Consequences

- Future Archon workflow runs have a documented health-check path.
- Machine-local MCP config can exist locally without becoming a committed
  bootstrap artifact.
- Harness validation now catches missing repo-local Archon workflow/config
  assets and outdated AGENTS heading expectations.
- PIV can run in the current operator environment without falling through to
  unavailable provider/model paths.
- PR creation still depends on GitHub token scope. The failed PIV finalization
  was caused by `createPullRequest` permission denial, not by code validation.

## architecture-spec

Not separately stated in the original archive ADR.

## acceptance-criteria

Not separately stated in the original archive ADR.

## implementation-brief

The PIV loop produced and merged these commits:

```text
7570364 chore: ignore Archon MCP runtime config
e823f71 feat: validate Archon bootstrap assets
517ffe9 test: cover Archon harness validation assets
916c09a docs: document Archon health checks
0661667 docs: add Archon health hardening handoff
89c3331 fix: update Archon PIV workflow model defaults
f90e855 Merge Archon health bootstrap hardening
```

Primary files changed:

- `.gitignore`
- `archon/workflows/archon-piv-loop.yaml`
- `README.md`
- `src/python/projectkoios/bootstrap/validation/harnesses.py`
- `tests/test__validate_harnesses.py`
- `docs/archive/handoffs/opencode/20260630.135327_archon-health-bootstrap-hardening.md`

The work was pushed to `origin/master` at `f90e855`.

## resolved-open-questions

None stated.

## non-goals

None stated.

## validation-expectations

The final merged state passed:

- `projectkoios bootstrap validate-harnesses --root .`
- `archon validate workflows`

The PIV implementation handoff also records:

- `mypy` passed via ephemeral `uv run --with mypy`
- `compileall` passed
- focused pytest passed with `10 passed`
- full pytest passed with `52 passed`
- `archon doctor` ended with all checks passed
- `.archon/mcp/ntfy.json` is ignored by `.gitignore`

`bun run validate` and related Bun script checks are not applicable for this
repo because it has no Bun project scripts.

## routing

- Owner: Athena
- Next phase: completed
- Notes: Historic archived ADR normalized to the template; original text preserved below.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None

---

## original

# ADR 20260630.141231: Archon health PIV session

## Status

historic

## Context

Archon was not healthy enough to run a full Project Koios PIV loop from this
repo without local operator repair. The session started with three concrete
problems:

- `archon` was not reliably available on `PATH`.
- Full workflow validation failed because repo-local Archon MCP runtime config
  expected `.archon/mcp/ntfy.json`, but that file is installation-specific.
- `archon-piv-loop` referenced model names that were not usable in the current
  operator environment.

The user also clarified broader direction during PIV exploration:

- Athena should encapsulate Archon with the Petri-net/meta-harness stack.
- ADR message schema should be deferred until Koios is up and running.
- Human-readable docs should live under a docs-like architecture, with ADRs as
  provenance records and Graphify as the current semantic representation path.
- Dot-prefixed paths are installation-specific, not simply "ignored".

Only the Archon-health bootstrap slice was implemented in this repo during this
session. The broader documentation and schema restructuring remains future
architecture work.

## Decision

Treat Archon health as a bootstrap-owned operational capability and make the
repo validate that capability without committing machine-local runtime state.

Concretely:

1. Keep `.archon/mcp/` local-only and ignored by git.
2. Validate repo-owned Archon assets through
   `projectkoios bootstrap validate-harnesses --root .`.
3. Align harness validation with the current AGENTS.md headings:
   `Hermes (pi)`, `Athena (archon)`, and `Vulcan (opencode)`.
4. Document Archon health checks in README:
   `archon doctor`, `archon validate workflows`, `archon workflow runs`, and
   `archon isolation list`.
5. Pin this repo's PIV workflow model settings to `gpt-5.5` so the workflow
   uses the available Codex path rather than unavailable model aliases or the
   unauthenticated Pi/Anthropic path.
6. Preserve the PIV implementation report as a Vulcan-to-Hermes handoff.
7. When GitHub PR creation is blocked by token scope after validation passes,
   pushing the validated branch to `master` is acceptable with explicit
   reporting.

## Implementation

The PIV loop produced and merged these commits:

```text
7570364 chore: ignore Archon MCP runtime config
e823f71 feat: validate Archon bootstrap assets
517ffe9 test: cover Archon harness validation assets
916c09a docs: document Archon health checks
0661667 docs: add Archon health hardening handoff
89c3331 fix: update Archon PIV workflow model defaults
f90e855 Merge Archon health bootstrap hardening
```

Primary files changed:

- `.gitignore`
- `archon/workflows/archon-piv-loop.yaml`
- `README.md`
- `src/python/projectkoios/bootstrap/validation/harnesses.py`
- `tests/test__validate_harnesses.py`
- `docs/archive/handoffs/opencode/20260630.135327_archon-health-bootstrap-hardening.md`

The work was pushed to `origin/master` at `f90e855`.

## Validation

The final merged state passed:

- `projectkoios bootstrap validate-harnesses --root .`
- `archon validate workflows`

The PIV implementation handoff also records:

- `mypy` passed via ephemeral `uv run --with mypy`
- `compileall` passed
- focused pytest passed with `10 passed`
- full pytest passed with `52 passed`
- `archon doctor` ended with all checks passed
- `.archon/mcp/ntfy.json` is ignored by `.gitignore`

`bun run validate` and related Bun script checks are not applicable for this
repo because it has no Bun project scripts.

## Consequences

- Future Archon workflow runs have a documented health-check path.
- Machine-local MCP config can exist locally without becoming a committed
  bootstrap artifact.
- Harness validation now catches missing repo-local Archon workflow/config
  assets and outdated AGENTS heading expectations.
- PIV can run in the current operator environment without falling through to
  unavailable provider/model paths.
- PR creation still depends on GitHub token scope. The failed PIV finalization
  was caused by `createPullRequest` permission denial, not by code validation.

## Deferred Work

- Define the Athena/Archon/Petri-net encapsulation model as a separate
  architecture decision.
- Rename or rationalize `doc/` versus `docs/` and move any current
  architecture hub material deliberately. *(Completed: ADR consolidation
  moved everything to `docs/architecture/adr/`.)*
- Define the ADR/message append schema after Koios is operational.
- Decide how Graphify output becomes the semantic representation of docs and
  ADR provenance without committing machine-local generated state.
