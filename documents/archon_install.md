# Archon install for pi

This guide is for someone actually installing Archon on their machine and using it from **pi**.

**Note:** if a step is interactive, run it yourself in your terminal. This guide will not try to automate interactive prompts.

## What you need

- **git**
- **bun**
- **pi** installed and logged in
- A target project repo you want Archon to work on

## 1) Clone Archon

```bash
mkdir -p ~/src
cd ~/src
git clone https://github.com/coleam00/Archon.git
cd Archon
```

If you already cloned it somewhere else, just `cd` there instead.

## 2) Install the CLI

```bash
bun install
cd packages/cli
bun link
```

If `archon` is not found, see `documents/bin_install.md` for the PATH fix.

Verify it works:

```bash
archon version
```

If that fails, try `~/.bun/bin/archon version` or re-run `bun link`.

## 3) Log in to pi

Archon uses your existing Pi login.

Run this yourself in your terminal:

```bash
pi /login
```

Check that Pi auth exists:

```bash
ls ~/.pi/agent/auth.json
```

## 4) Configure Archon to use pi

The easiest way is to run the setup wizard from the Archon repo.

Run this yourself in your terminal:

```bash
archon setup
```

When the wizard asks, choose **Pi (community)**.

If you want to set it manually in a repo, add this to `.archon/config.yaml`:

```yaml
assistant: pi
assistants:
  pi:
    model: anthropic/claude-sonnet-4-5
```

You can use any Pi model ref you have configured, including local models.

## 5) Go to your project and test it

```bash
cd /path/to/your/project
archon workflow list
```

Try a simple run:

```bash
archon workflow run archon-assist "Say hello"
```

## 6) Important notes

- You do **not** need an MCP server for basic Archon + pi use.
- Pi is already supported by Archon; there is no separate Archon-side install for it.
- If `archon` is not found, open a new terminal or re-run `bun link`.
- If `pi /login` has never been run on this machine, Archon will not have Pi auth to use.

## Recommended order

1. Clone Archon
2. `bun install`
3. `bun link`
4. `pi /login`
5. `archon setup`
6. Test from your target repo
