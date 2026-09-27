# Shared exact branch push extraction record

## Lifecycle and owner

**Extracted.** This repository incubated and validated a repository-agnostic
exact branch-push contract. After reviewed use in two repositories, version
`1.0.0` moved to the operator's shared Pi installation:

```text
source:     ~/.pi/agent/tools/push-git-branch
executable: ~/.pi/agent/bin/push-git-branch
commit:     b0fbe662a2e34d4179ceb1a7abe6d8ec6849c9ff
tag:        v1.0.0
```

Repositories invoke that installation. They do not copy or own the source. This
file preserves the extraction evidence and contract; the bootstrap repository
no longer exposes an implementation or console entry point.

## Contract

The caller supplies every authority and identity input:

```bash
push-git-branch \
  --repo-path /absolute/canonical/worktree \
  --remote origin \
  --branch feature/example \
  --expected-commit 0123456789abcdef0123456789abcdef01234567
```

The default is a dry run. `--apply` authorizes one push and the corresponding
upstream configuration. `--replace-upstream` is separately required when the
captured initial upstream differs from `<remote>/<branch>`.

Before contacting the remote, the command requires:

- an absolute, canonical worktree root;
- a valid explicit remote and branch name;
- a full lowercase SHA-1 or SHA-256 commit object ID;
- attached `HEAD`, the named local branch, and the expected commit to agree;
- a clean tracked and untracked worktree;
- compatible captured upstream authority;
- exactly one fetch endpoint and one identical push endpoint; and
- a fetch refspec mapping the branch to its standard remote-tracking ref.

The push uses the expected object ID as the source of one exact heads refspec.
It is non-force and disables pre-push hooks, tag following, recursive submodule
pushes, configured push options, and configured push signing. Git terminal
prompting, credential interactivity, and stdin are disabled; callers must
provide already noninteractive credential, SSH, and remote helpers. Lazy
fetching, background maintenance, inherited Git tracing, and repository
redirection are disabled.

After the push, the command queries the same validated endpoint and requires the
remote branch to equal the expected commit. It rechecks local branch identity,
cleanliness, and upstream authority before setting the matching upstream, then
requires the remote-tracking ref to equal the expected commit. A failure causes
no cleanup, retry, force push, or rollback because remote state may already have
changed. Callers must exclude concurrent local ref, worktree, and configuration
writers.

## Limits

The command does not commit, stage, fetch, pull, merge, rebase, tag, delete refs,
create or merge pull requests, infer hosting identity, choose a branch or
commit, authenticate a remote, or establish merge readiness. Remote state can
change after verification. Dry-run preflight uses `ls-remote`, so callers remain
responsible for network authorization and credentials. Git 2.45 or newer is
required.

## Extraction evidence

The reviewed bootstrap implementation comprised commits:

- `85f45ab3199080fff5f718084acf37abcf3766a8`
- `3c57dc8f6751b96530e886bacd425d77f9e6b0f7`
- `335beec05c198d3e227a399416e5226fa666d9a7`
- `0d14115d9ac1cf2afc300c081855d65bda7c2c2d`

PR #9 merged it at `c9018d7b6fa14bbb806ccd2dfd23261d27e203bf`.
The command first pushed its own exact feature tip, then ran unchanged against
`projectkoios-ingestion`, where it pushed
`fe0051a45629bc133bbcf1691965a55679377b7b`. That independent branch merged at
`a1f50256313f002554c36520851f6dc39e70cb8e`.

The extracted installation retains the Apache-2.0 license, provenance metadata,
temporary-repository/local-bare-remote tests, SHA-1 and SHA-256 coverage, and the
reviewed fail-closed behavior. Its 19 tests, Ruff, formatting, Mypy, public API
import, launcher help, and installed executable local push all passed before
activation.
