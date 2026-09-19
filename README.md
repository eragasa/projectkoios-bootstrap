# Project Koios Bootstrap

A minimal operational cockpit for coordinating work across Project Koios
repositories and incubating the Project Koios-specific Pi coordination
harness.

This repository may contain bounded coordination helpers, project-specific Pi
skills or prompt templates, sanitized fixtures, tests, and experimental harness
candidates. It contains no product code, generic workflow engine, named agent
roles, or persistent orchestration state. Pi provides sessions and tools; Git,
GitHub, and the owning repositories provide durable product and task state.

## Start the coordinator

Start Herdr **before** Pi so the coordinator inherits the pane context required
to open visible repository sessions:

```bash
cd path/to/projectkoios-bootstrap
herdr
```

Then, inside the Herdr pane:

```bash
pi
```

See the [operator environment guide](docs/operator-environment.md) for setup,
verification, repository-pane conventions, and recovery guidance. Starting Pi
outside Herdr cannot be repaired by installing or launching Herdr afterward;
start a new Pi session inside a managed pane instead.

Optionally name the session:

```text
/alias bootstrap
```

Useful requests include:

```text
List the active Project Koios sessions.
Open visible sessions for projectkoios-api and projectkoios-web.
Send each session its bounded task and report their progress.
Show which sessions are idle, thinking, blocked, or using a tool.
Reconcile the resulting commits against the mothership decision.
```

## Operating model

1. The bootstrap session reads `maps/repositories.md`.
2. It uses `pi-intercom` to find or message repository sessions.
3. Long-lived work runs in visible Herdr project panes.
4. Bounded parallel work may use Pi subagents with explicit repository working
   directories.
5. Each repository validates and commits its own changes.
6. Cross-repository architecture and decisions are recorded in the
   `projectkoios` mothership.
7. Bounded coordination patterns may be preserved as harness candidates under
   the [incubation policy](docs/harness-incubation.md); one observation does not
   establish recurrence or production readiness.

The optional, observed issue-inventory candidate can check all mapped GitHub
repositories without treating a failed query as zero issues:

```bash
./scripts/koios_issues.py
```

It is not yet mandatory coordination infrastructure. See its
[candidate documentation](docs/candidates/issue-inventory.md) for prerequisites,
JSON and replay modes, exit behavior, and limitations.

A separate
[adversarial architecture review agent candidate](docs/candidates/adversarial-architecture-review.md)
preserves one fresh-context, tool-less review pattern without introducing a
persistent architect role or second writer. Its agent source remains under
`docs/candidates/` and is not installed automatically.

`pi-intercom` shows each connected session's repository and live state. Full
independent-session transcripts remain visible in their Herdr panes; intercom
is for status and communication rather than transcript replication.

## Repository contents

```text
AGENTS.md
README.md
docs/harness-incubation.md
docs/operator-environment.md
docs/candidates/issue-inventory.md
docs/candidates/adversarial-architecture-review.md
docs/candidates/agents/adversarial-architecture-reviewer.md
maps/repositories.md
scripts/candidates/adversarial_architecture_packet.py
scripts/koios_issues.py
tests/test_adversarial_architecture_packet.py
tests/test_adversarial_architecture_review_agent.py
tests/test_koios_issues.py
```

`LICENSE` and `.gitignore` are retained as repository metadata. Historical
bootstrap machinery remains recoverable from Git history but is not part of the
active working tree. The incubation boundary permits small evidence-driven
coordination candidates; it does not restore the former meta-harness monolith.
