# Scripts

All scripts in this directory should be:
- self-describing at the top of the file
- safe to run repeatedly when practical
- explicit about their inputs, outputs, and tmux behavior
- documented here when they become part of the normal workflow

## `koios`

Documented CLI for managing the koios tmux session and its four windows.

### Commands

```bash
./scripts/koios harnesses start
./scripts/koios harnesses show
./scripts/koios harnesses connect [archon|opencode|goose|scratch]
./scripts/koios harnesses stop
./scripts/koios install
```

`install` syncs the repo-managed pi harness config into `~/pi/agent/` and `~/.pi/agent/`.

Bootstrap architecture notes: `docs/architecture.00.md`

### Workspace layout

- tmux session: `koios`
- windows: `archon`, `opencode`, `goose`, `scratch`

### Behavior

- `start` creates the koios session and missing windows
- `start` also runs `./scripts/hermes-startup new` to write the Hermes session marker
- `show` lists the koios session and its windows
- `connect` focuses one window
- `stop` kills the koios session
- `start`/`stop` should be run outside tmux
- `connect` works inside tmux and outside tmux
- the `archon` window launches `pi`
- the `goose` window launches `goose run --instructions goose/AGENT.md`

## `start-harnesses.sh`

Compatibility wrapper for `./scripts/koios harnesses start`.

## `hermes-startup`

Hermes autoprocess launcher for restart/resume.

```bash
./scripts/hermes-startup new
```

Behavior:
- `new` writes a durable timestamped session note and prints `new session`
- reads `workspaces/hermes/state.md`
- reads `workspaces/hermes/active.md`
- reads the newest timestamped file in `workspaces/hermes/sessions/`
- lists Hermes inbox and outbox files
- prints the repo branch, status, and recent commits
- `new` mutates only the session-note surface
