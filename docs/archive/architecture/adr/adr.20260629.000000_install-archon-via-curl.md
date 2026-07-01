# ADR 20260629.000000: Install Archon via curl rather than Homebrew

## Status

historic

## Context

Archon is one of the three agent harnesses used by this meta-harness (see
ADR20260628). To use it, the Archon CLI must be installed on the developer
machine.

Two installation methods are available:

- **curl install**: `curl -fsSL https://archon.diy/install | bash` — the
  canonical upstream method, but requires sudo on macOS to write to
  `/usr/local/bin`.
- **Homebrew**: `brew install archon` — installs to `/opt/homebrew/bin/archon`
  and pulls in `icu4c` as a system-level dependency.
- **Manual binary install**: Download the release binary directly and place it
  in a user-writable directory on `PATH` (e.g. `~/.local/bin/`).

All methods install the same compiled binary build.

## Decision

Install Archon by downloading the binary directly to `~/.local/bin/`:

```bash
mkdir -p ~/.local/bin
curl -fsSL https://github.com/coleam00/Archon/releases/latest/download/archon-darwin-arm64 \
  -o ~/.local/bin/archon
chmod +x ~/.local/bin/archon
```

Ensure `~/.local/bin` is on `PATH` in the shell config if not already.

Do not use Homebrew.

## Rationale

**Avoids sudo dependency.** The curl installer requires sudo to write to
`/usr/local/bin`, which fails in non-interactive terminal sessions.
`~/.local/bin` is user-writable and already on PATH on many systems.

**No external Homebrew formula to maintain.** Avoids depending on a third-party
formula that may lag behind releases or behave differently.

**Self-contained runtime.** Does not pollute the Homebrew package graph with
transitive dependencies like `icu4c` that are unrelated to the project.

## Consequences

Developers setting up this repository must run:

```bash
mkdir -p ~/.local/bin
curl -fsSL https://github.com/coleam00/Archon/releases/latest/download/archon-darwin-arm64 \
  -o ~/.local/bin/archon
chmod +x ~/.local/bin/archon

# Ensure ~/.local/bin is on PATH
grep -q '$HOME/.local/bin\|~/.local/bin' ~/.zshrc 2>/dev/null || \
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
```

Then configure the tool via `archon setup`.

The previously Homebrew-installed Archon 0.5.0 has been uninstalled. No data
migration is needed since workflows and config live in this repo, not in the
Homebrew Cellar.
