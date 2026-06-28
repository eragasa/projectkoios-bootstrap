# projectkoios-bootstrap

The three-harness meta-harness for building and operating Project Koios.

```
projectkoios-bootstrap/
├── architecture/   ← design docs and ADRs
├── maps/           ← workspace layout (repos, packages, vault)
├── archon/         ← Archon — architecture and design workflows
├── opencode/       ← opencode — build and runtime
└── goose/          ← Goose — knowledge management
```

## Harnesses

| Harness | Tool | Domain |
|---------|------|--------|
| **archon/** | [Archon](https://archon.diy) | Architecture decisions, ADRs, planning, design review |
| **opencode/** | opencode | Code implementation, tests, validation, runtime sessions |
| **goose/** | [Goose](https://goose-docs.ai) | Knowledge curation, vault ops, source ingestion, UI bootstrap |

## Prerequisites

```bash
brew install python uv
# opencode: https://opencode.ai
# Archon CLI:
mkdir -p ~/.local/bin
curl -fsSL https://github.com/coleam00/Archon/releases/latest/download/archon-darwin-arm64 \
  -o ~/.local/bin/archon
chmod +x ~/.local/bin/archon
# Goose CLI: https://goose-docs.ai/docs/quickstart
```

## Commands

### opencode — build and runtime

```bash
cd ~/repos/projectkoios-bootstrap

# Start an opencode session with the build harness rules
opencode

# Then within the session:
# - Read maps/ to understand the workspace
# - Read opencode/rules/ for build policies
# - Implement code in the correct component repo (maps/packages.md)
# - Run validation gates before finishing
```

### Goose — knowledge management

```bash
cd ~/repos/projectkoios-bootstrap

# Start a Goose session with the KM harness
goose run

# Or with explicit config path:
goose run --hints goose/AGENT.md

# Then within the session:
# - Read maps/ for vault and repo locations
# - Use prompts from goose/prompts/ for common tasks
# - Run ingest.md, curate.md, search.md, or ui-bootstrap.md
```

### Archon — architecture and design

Project workflows in this repo default to Pi.

```bash
cd ~/repos/projectkoios-bootstrap

# List workflows
archon workflow list

# Run a design review workflow
archon workflow run design-review "architecture/some-doc.md"

# Create a new ADR
archon workflow run create-adr "decision summary"

# Plan a feature
archon workflow run plan-feature "feature request"
```

## Workspace

Read `maps/repositories.md`, `maps/packages.md`, and `maps/vault_paths.md`
before touching any code. These are the authoritative source for where
everything lives.

All component repos are siblings under `~/repos/`.

## Architecture

See `architecture/adr.20260628.md` for the decision record behind this
three-harness structure.
