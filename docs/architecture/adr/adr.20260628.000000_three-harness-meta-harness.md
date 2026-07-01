# ADR 20260628.000000: Establish projectkoios-bootstrap as the three-harness meta-harness

## Status

Completed

## Supersedes

ADR20260611 — retroactively. The mothership no longer defines the sole
repository structure for agent-operation logic.

## Context

Project Koios has been split into multiple component repositories per
ADR20260626. Each component repo owns its domain code. However, there is no
dedicated place for the cross-cutting agent infrastructure needed to build,
operate, and maintain the system.

Three distinct agent workflows have emerged, each best served by a different
tool:

- Architecture and design decisions benefit from DAG-based orchestration
  with isolated worktrees and parallel agent dispatch.
- Interactive build and runtime work (implementing code, running tests,
  validation) benefits from a session-based agent with project rules and
  permission policies.
- Knowledge management (vault curation, source ingestion, UI bootstrapping)
  benefits from a general-purpose agent with MCP extensions for filesystem
  and memory.

No single agent framework is optimal for all three. Mixing them in a single
tool's config creates confusion and prevents each from being used to its
strength.

## Decision

Create `projectkoios-bootstrap` as a single meta-harness repository containing
three independent harness directories, plus shared context.

```
projectkoios-bootstrap/
├── docs/architecture/adr/ ← shared design docs and ADRs (single source of truth)
├── maps/                  ← shared workspace layout (repos, packages, vault)
│
├── archon/                ← Archon harness: architecture and design
│   ├── workflows/
│   │   ├── create-adr.yaml
│   │   ├── design-review.yaml
│   │   └── plan-feature.yaml
│   └── prompts/
│
├── opencode/              ← opencode harness: build and runtime
│   ├── rules/
│   │   ├── build.md
│   │   ├── validation.md
│   │   ├── specification_gate.md
│   │   └── tool_policy.md
│   ├── env.example
│   ├── sessions/
│   └── sandbox/
│
└── goose/                 ← Goose harness: knowledge management
    ├── AGENT.md
    ├── .mcp.json
    ├── prompts/
    │   ├── ingest.md
    │   ├── curate.md
    │   ├── search.md
    │   └── ui-bootstrap.md
    └── sessions/
```

### Harness responsibilities

| Harness | Tool | Domain | Workflow style |
|---------|------|--------|----------------|
| archon/ | Archon (archon.diy) | Architecture design, ADRs, planning | DAG-based YAML workflows, parallel dispatch, isolated worktrees |
| opencode/ | opencode | Code implementation, tests, validation, runtime sessions | Interactive sessions, project rules, permission gates |
| goose/ | Goose (aaif-goose/goose) | Knowledge curation, vault ops, ingestion, UI bootstrap | MCP-based tool execution, AGENT.md hints, task prompts |

### Shared context

`docs/architecture/adr/` contains durable design documents and ADRs that all three
harnesses reference.

`maps/` contains the authoritative workspace layout:
- `maps/repositories.md` — physical repo locations
- `maps/packages.md` — package-to-responsibility mapping
- `maps/vault_paths.md` — vault directory structure

Each harness may read maps, but no harness owns them. Maps are updated when
the workspace changes.

### Boundaries

Project Koios component repos own scientific domain logic and executable code.
`projectkoios-bootstrap` owns agent-operation logic:
- YAML workflow definitions (Archon)
- Agent rules, prompts, and policies (opencode, Goose)
- Validation gate descriptions
- Provider configuration examples
- Workspace maps

No Project Koios component repo imports from or depends on
`projectkoios-bootstrap`.

## Rationale

**Three tools, three strengths.** Archon's DAG model suits multi-agent
architecture workflows that benefit from parallel dispatch and isolation.
opencode's session model suits interactive development with tight feedback
loops. Goose's MCP ecosystem suits knowledge tasks that need filesystem,
memory, and future custom extensions.

**One repo, not three.** The harnesses share architecture context and maps.
Keeping them in one repo avoids synchronization overhead and gives a single
place to understand the entire agent infrastructure.

**No agent config leak.** Each harness's configuration stays in its own
directory. Archon YAML workflows don't mix with opencode AGENTS.md, which
don't mix with Goose .mcp.json. This keeps each tool's config valid and
focused.

## Consequences

The existing `projectkoios-bootstrap` Python stub repo needs its directory
structure replaced with the harness layout above.

The `src/python/projectkoios/bootstrap/` directory becomes unused if no
Python code is needed. It may be kept for future shared utilities or removed.

Shared `docs/architecture/` and `maps/` must be kept in sync with the actual
workspace. Outdated maps defeat their purpose.

Each harness must define its own scope clearly to prevent overlap or
confusion about which tool to use for a given task.

## Alternatives considered

### Everything in one agent tool (opencode only)

Rejected. opencode does not support DAG-based parallel workflow orchestration
out of the box, and forcing knowledge management into a coding-oriented
harness creates friction.

### Separate repos per harness

Rejected. The shared architecture docs and maps would need to be synchronized
across three repos, adding overhead without meaningful benefit.

### Keep everything in the mothership

Rejected (per ADR20260626). The mothership owns architecture notes and ADRs,
not agent-operation configuration.
