# Bun bin path fix

If `archon` (or other Bun-linked commands) is not found in your shell, add Bun's global bin directory to your PATH.

## Temporary for this terminal

```bash
export PATH="$HOME/.bun/bin:$PATH"
```

## Permanent for zsh

```bash
echo 'export PATH="$HOME/.bun/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## Verify

```bash
archon version
```

If you still get `command not found`, try running it directly:

```bash
~/.bun/bin/archon version
```
