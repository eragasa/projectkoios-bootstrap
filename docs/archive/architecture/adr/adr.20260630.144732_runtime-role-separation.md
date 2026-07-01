# ADR 20260630.144732: Separate Runtime identity from Role identity

## Status

historic

## Context

`Harness` in `src/python/projectkoios/bootstrap/models.py` conflates two
distinct concerns in a single frozen dataclass:

| Field | Example values | What it actually represents |
|---|---|---|
| `name` | `pi`, `archon`, `opencode`, `goose` | Infrastructure runtime — the tool that executes |
| `display_name` | `pi`, `Athena`, `Vulcan`, `Koios` | Domain role — the agent identity that acts |
| `config_dir` | `~/.pi`, `~/.archon`, etc. | Runtime config path |
| `role` | `"Agent runtime — executes Archon workflows"` | Blended description |

Three commands depend on `HARNESSES` (the module-level list of `Harness`
instances):

1. **`init`** — copies `agents/global/<name>/` to `~/.<harness>/`. This is a
   pure infrastructure operation: it needs the runtime name and config dir.
2. **`install`** — symlinks configs and materializes skills. Also pure
   infrastructure: needs runtime name, skills dir, and runtime skills dir.
3. **`validation/harnesses.py`** — checks canonical files and reference
   integrity per runtime. Infrastructure: needs runtime name and known paths.

The new `archon_run_watch` skill (implemented under
`agents/global/roles/ATHENA/archon_run_watch/`) and the handoff-topics projection
model both need to reference role identity — which harness is responsible for
what, which role produced an artifact, which role should receive it.

If we build these features on the current `Harness` abstraction, we cement
the coupling and make it harder to separate later.

## Decision

See the original ADR text below for the historical decision.

## Consequences

- **Immediate:** The `archon_run_watch` skill scripts can import `Role`
  without dragging in runtime-specific fields like `config_dir`.
- **Short-term:** `init`, `install`, and `validate_harnesses` were refactored
  to iterate `RUNTIMES` instead of `HARNESSES` (commit `ae91f14`). The change was
  mechanical and tested.
- **Medium-term:** The handoff parser and evaluator (which currently use
  inline `HERMES_IDS`, `CODEX_IDS` string sets in `guards.py`) can migrate to
  `Role` objects, replacing hardcoded identity checks with declarative data.
- **Long-term:** The `ROLE_TO_RUNTIME` mapping can be externalised to config
  or removed entirely when roles no longer imply a specific runtime.

## architecture-spec

Replace the single `Harness` with two distinct models in
`projectkoios.bootstrap.models`:

### `Runtime` — infrastructure identity

```python
@dataclass(frozen=True)
class Runtime:
    name: str          # "pi", "archon", "opencode", "goose"
    config_dir: Path   # ~/.pi, ~/.archon, ~/.opencode, ~/.local/share/goose

    @property
    def skills_dir(self) -> Path:
        return GLOBAL_DIR / self.name / "skills"

    @property
    def runtime_skills_dir(self) -> Path:
        ...
```

Used by: `init`, `install`, `validate_harnesses`.

### `Role` — domain identity

```python
@dataclass(frozen=True)
class Role:
    name: str            # "Hermes", "Athena", "Vulcan", "Koios"
    short_name: str      # "pi", "archon", "opencode", "goose" (or None if runtime-free)
    responsibilities: str
```

Used by: meta-harness handoff model (parsing, routing, guard rules), skill
scripts that need to know who does what.

### Mapping (transitional)

For the current state where each role runs on exactly one runtime:

```python
ROLE_TO_RUNTIME: dict[str, str] = {
    "Hermes": "pi",
    "Athena": "archon",
    "Vulcan": "opencode",
    "Koios": "goose",
}
```

This mapping can be removed in the future if roles become runtime-independent.

## acceptance-criteria

During implementation of the `archon_run_watch` skill, two structural
questions were decided:

1. **Script grouping:** All three scripts (`handoff_new.py`, `session_scan.py`,
   `archon_run_watch.py`) stay under one skill at
   `agents/global/roles/ATHENA/archon_run_watch/scripts/`. They share a
   `_utils.py` helper and are collectively scoped to meta-harness operations.
   No split into separate skills.

2. **Skill scope:** The SKILL.md retains full session-ops coverage (session
   start, routing, handoff creation, Archon run monitoring). It was not
   narrowed to Archon-focused only, because the routing decision table, session
   protocol, and handoff discipline are all part of a single operator workflow
   for Hermes/Codex.

Both decisions are reflected in the relocated skill at commit `0cc75c1`.

## implementation-brief

Not separately stated in the original archive ADR.

## resolved-open-questions

None stated.

## non-goals

- The runtime config layout `~/.<runtime>/` stays as-is. The
  `agents/global/<name>/` runtime-namespaced layout remains for runtime-level
  config; role-aligned skill paths under `agents/global/roles/<ROLE>/` are
  introduced alongside it.
- Do not introduce dynamic role discovery or runtime registration.
- Do not touch `commands/harnesses.py` (tmux management) — it doesn't use
  the `HARNESSES` list.

## validation-expectations

Not separately stated in the original archive ADR.

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

# ADR 20260630.144732: Separate Runtime identity from Role identity

## Status

historic

## Context

`Harness` in `src/python/projectkoios/bootstrap/models.py` conflates two
distinct concerns in a single frozen dataclass:

| Field | Example values | What it actually represents |
|---|---|---|
| `name` | `pi`, `archon`, `opencode`, `goose` | Infrastructure runtime — the tool that executes |
| `display_name` | `pi`, `Athena`, `Vulcan`, `Koios` | Domain role — the agent identity that acts |
| `config_dir` | `~/.pi`, `~/.archon`, etc. | Runtime config path |
| `role` | `"Agent runtime — executes Archon workflows"` | Blended description |

Three commands depend on `HARNESSES` (the module-level list of `Harness`
instances):

1. **`init`** — copies `agents/global/<name>/` to `~/.<harness>/`. This is a
   pure infrastructure operation: it needs the runtime name and config dir.
2. **`install`** — symlinks configs and materializes skills. Also pure
   infrastructure: needs runtime name, skills dir, and runtime skills dir.
3. **`validation/harnesses.py`** — checks canonical files and reference
   integrity per runtime. Infrastructure: needs runtime name and known paths.

The new `archon_run_watch` skill (implemented under
`agents/global/roles/ATHENA/archon_run_watch/`) and the handoff-topics projection
model both need to reference role identity — which harness is responsible for
what, which role produced an artifact, which role should receive it.

If we build these features on the current `Harness` abstraction, we cement
the coupling and make it harder to separate later.

## Proposal

Replace the single `Harness` with two distinct models in
`projectkoios.bootstrap.models`:

### `Runtime` — infrastructure identity

```python
@dataclass(frozen=True)
class Runtime:
    name: str          # "pi", "archon", "opencode", "goose"
    config_dir: Path   # ~/.pi, ~/.archon, ~/.opencode, ~/.local/share/goose

    @property
    def skills_dir(self) -> Path:
        return GLOBAL_DIR / self.name / "skills"

    @property
    def runtime_skills_dir(self) -> Path:
        ...
```

Used by: `init`, `install`, `validate_harnesses`.

### `Role` — domain identity

```python
@dataclass(frozen=True)
class Role:
    name: str            # "Hermes", "Athena", "Vulcan", "Koios"
    short_name: str      # "pi", "archon", "opencode", "goose" (or None if runtime-free)
    responsibilities: str
```

Used by: meta-harness handoff model (parsing, routing, guard rules), skill
scripts that need to know who does what.

### Mapping (transitional)

For the current state where each role runs on exactly one runtime:

```python
ROLE_TO_RUNTIME: dict[str, str] = {
    "Hermes": "pi",
    "Athena": "archon",
    "Vulcan": "opencode",
    "Koios": "goose",
}
```

This mapping can be removed in the future if roles become runtime-independent.

## Consequences

- **Immediate:** The `archon_run_watch` skill scripts can import `Role`
  without dragging in runtime-specific fields like `config_dir`.
- **Short-term:** `init`, `install`, and `validate_harnesses` were refactored
  to iterate `RUNTIMES` instead of `HARNESSES` (commit `ae91f14`). The change was
  mechanical and tested.
- **Medium-term:** The handoff parser and evaluator (which currently use
  inline `HERMES_IDS`, `CODEX_IDS` string sets in `guards.py`) can migrate to
  `Role` objects, replacing hardcoded identity checks with declarative data.
- **Long-term:** The `ROLE_TO_RUNTIME` mapping can be externalised to config
  or removed entirely when roles no longer imply a specific runtime.

## Non-goals

- The runtime config layout `~/.<runtime>/` stays as-is. The
  `agents/global/<name>/` runtime-namespaced layout remains for runtime-level
  config; role-aligned skill paths under `agents/global/roles/<ROLE>/` are
  introduced alongside it.
- Do not introduce dynamic role discovery or runtime registration.
- Do not touch `commands/harnesses.py` (tmux management) — it doesn't use
  the `HARNESSES` list.

## Resolved decisions

During implementation of the `archon_run_watch` skill, two structural
questions were decided:

1. **Script grouping:** All three scripts (`handoff_new.py`, `session_scan.py`,
   `archon_run_watch.py`) stay under one skill at
   `agents/global/roles/ATHENA/archon_run_watch/scripts/`. They share a
   `_utils.py` helper and are collectively scoped to meta-harness operations.
   No split into separate skills.

2. **Skill scope:** The SKILL.md retains full session-ops coverage (session
   start, routing, handoff creation, Archon run monitoring). It was not
   narrowed to Archon-focused only, because the routing decision table, session
   protocol, and handoff discipline are all part of a single operator workflow
   for Hermes/Codex.

Both decisions are reflected in the relocated skill at commit `0cc75c1`.
