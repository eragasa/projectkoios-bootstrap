# Handoff evaluator: colored Petri net model

The handoff validator in `src/python/projectkoios/bootstrap/harness/` implements
a read-only colored Petri net for the Project Koios meta-harness.

It does not build a general Petri net engine. It applies one fixed net — the
meta-harness handoff flow — to the repo-local `*/handoffs/*.md` artifact set
and reports violations.

## Why a Petri net

The meta-harness routes typed artifacts (colored tokens) between harness roles.
A plain DAG can order steps but cannot model:

- **ownership** — which harness owns each transition
- **provenance** — who mediated, who acted as whom
- **artifact type** — the "color" that determines which transitions apply
- **authority** — priority when artifacts disagree
- **invalid transitions** — e.g. Hermes completing implementation after routing to Vulcan
- **concurrent active handoffs** — multiple artifacts in flight simultaneously
- **revision loops** — rejected artifacts returning upstream

A colored Petri net models these as places, colored tokens, transitions,
guards, and markings. The evaluator is a read-only snapshot: it parses the
current handoff state, builds a marking, runs all guards, and reports
violations without mutating any file.

## Model

### Places

A place is a named inbox or state. The evaluator maps four handoff directories
to fixed places:

| Place | Directory (now archived) | Purpose |
|-------|--------------------------|---------|
| `archon_inbox` | `docs/archive/handoffs/archon/` | Athena's active work |
| `opencode_inbox` | `docs/archive/handoffs/opencode/` | Vulcan's active work |
| `pi_inbox` | `docs/archive/handoffs/pi/` | Hermes's active work |
| `goose_inbox` | `docs/archive/handoffs/goose/` | Koios's active work |

Each handoff file becomes a token in its directory's place.

### Colored tokens

A token is a `HandoffArtifact` — a frozen dataclass with these fields:

| Field | Color | Source |
|-------|-------|--------|
| `kind` | `str` — artifact type (e.g. `architecture-spec`, `implementation-brief`) | Inferred from title and headers |
| `origin` | Harness name | `Origin:` header |
| `sender` | Agent name | `From:` header |
| `recipient` | Agent name | `To:` header |
| `acting_as` | Harness or `None` | `Acting-As:` header |
| `delegated_operator` | Mediator or `None` | `Delegated-Operator:` header |
| `provenance` | Header subset | Collated from `Origin`/`From`/`Scope`/`Repository` headers |
| `path` | File path (not a color, identity) | Filesystem |

The color is everything except `path` — it determines which guard rules apply.

### Marking

A `Marking` is the current distribution of tokens across places. The evaluator
builds it once per `evaluate()` call by parsing all handoff directories, then
passes it to every guard.

### Guards (transitions)

A guard is a function `(Marking) → list[Violation]`. It inspects the marking
and returns zero or more violations. There is no transition firing — the
evaluator is read-only. Guards are the "enabledness check" half of a Petri net
transition.

The four active guards:

| Guard | Detects | Why |
|-------|---------|-----|
| `check_hermes_forwarded_without_decision` | Hermes forwarding raw inbox state without a routing-decision, revision-request, completion-decision, or blockage-report | Hermes must decide, not relay |
| `check_wrong_implementation_owner` | Non-Vulcan actors producing `patch`, `test-results`, or `implementation-report` artifacts | Only Vulcan implements after routing |
| `check_delegated_operator_missing` | Codex-mediated artifacts missing `Delegated-Operator` provenance | Mediation must be explicit |
| `check_codex_as_pi_identity_collapse` | Codex-produced artifacts claiming pi/Hermes origin without separation | Codex is not pi |

### Violation

A `Violation` is a frozen dataclass with a `ViolationCode` (StrEnum), actor,
path, reason, and optional `required_owner`/`suggested_next_action`. Violations
can be serialized to Markdown blocks for appending to handoff files.

## Code architecture

### DataObjects (state)

| Class | File | Petri net analog |
|-------|------|------------------|
| `HandoffArtifact` | `data/artifact.py` | Colored token |
| `Marking` | `data/marking.py` | Current marking |
| `Violation` / `ViolationCode` | `data/violation.py` | Guard output |

DataObjects are frozen dataclasses — immutable, hashable, comparable. They
carry state but no side effects.

### Activities (behavior)

| Class / function | File | Petri net analog |
|------------------|------|------------------|
| `HandoffParser` | `handoffs/parser.py` | Tokenizer — parses handoff files into `HandoffArtifact` instances |
| `HandoffEvaluator` | `handoffs/evaluator.py` | Orchestrator — builds marking, runs guards, collects violations |
| Guards (4 functions) | `handoffs/guards.py` | Guard predicates — check enabledness |
| `append_violations` | `handoffs/appender.py` | Output writer — serializes violations into files (mutation opt-in) |

Activities are stateless by design. `HandoffParser` has no instance state (only
methods). Guard functions take `Marking`, return `list[Violation]`. The
evaluator owns a parser and a guard list but stores no evaluation results.

### Flow

```
HandoffParser.parse_directory(path)
         ↓
   HandoffArtifact instances
         ↓
HandoffEvaluator.build_marking()
         ↓
   Marking (tokens_by_place)
         ↓
HandoffEvaluator.evaluate()
         ↓
   guard_fn(marking)  →  list[Violation]
         ↓
   Aggregated violations
         ↓
HandoffEvaluator.violations_by_file()
         ↓
   dict[Path, list[Violation]]
         ↓
append_violations(path, violations)   [opt-in mutation]
```

## CLI

```bash
projectkoios bootstrap handoff evaluate          # parse + guard + append violations
projectkoios bootstrap handoff evaluate --dry-run # read-only, print only
projectkoios bootstrap handoff evaluate --root    # custom repo root
```

The CLI is a thin wrapper. It creates an evaluator, runs evaluation, and either
prints violations or appends them to the triggering handoff files.

## Non-goals

- No general Petri net execution engine
- No transition firing or token consumption
- No automatic mutation of historical handoffs
- No state persistence between evaluations
- No distributed or cross-repo evaluation
