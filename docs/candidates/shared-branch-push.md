# Shared exact branch push candidate

## Lifecycle and intended owner

**Candidate.** This repository incubates the behavior because repeated
cross-repository pushes exposed the same preflight and verification sequence.
The contract is repository-agnostic. After validation through independent
repositories, the command should be extracted to one shared operator-installed
package. Repositories invoke that installation; they do not copy this source.

The installed command is `push-git-branch`.

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
upstream configuration:

```bash
push-git-branch \
  --repo-path /absolute/canonical/worktree \
  --remote origin \
  --branch feature/example \
  --expected-commit 0123456789abcdef0123456789abcdef01234567 \
  --apply
```

Before contacting the remote, the command requires:

- an absolute, canonical worktree root;
- a valid explicit remote and branch name;
- a full lowercase SHA-1 or SHA-256 commit object ID;
- attached `HEAD`, the named local branch, and the expected commit to agree;
- a clean tracked and untracked worktree; and
- no existing upstream that differs from `<remote>/<branch>`.

The push uses the expected object ID as the source of one exact heads refspec.
It is non-force, disables pre-push hooks, tag following, recursive submodule
pushes, configured push options, credential prompts, lazy fetching, background
maintenance, and inherited Git tracing or repository redirection. It does not
use implicit push configuration to select refs.

After the push, the command queries the remote directly and requires the remote
branch to equal the expected commit. It rechecks local branch identity and
cleanliness, sets the matching upstream, and requires the remote-tracking ref to
equal the expected commit. A failure triggers no cleanup, retry, force push, or
rollback because remote state may already have changed.

## Limits

The command does not:

- commit, stage, fetch, pull, merge, rebase, tag, or delete refs;
- create or merge a pull request;
- infer repository hosting identity;
- choose a branch or commit;
- authenticate a remote URL;
- guarantee that another actor cannot change the remote after verification; or
- establish that a branch is ready for review or merge.

Dry-run preflight executes `ls-remote`, so it may authenticate and contact the
explicit remote. The caller remains responsible for network authorization and
credentials.

## Validation and extraction gate

Tests use temporary repositories and local bare remotes. They cover dry-run
behavior, exact push and upstream evidence, dirty worktrees, expected-commit
mismatch, conflicting upstreams, non-fast-forward rejection, hook bypass, tag
non-publication, canonical roots, bounded CLI errors, and SHA-256-shaped object
IDs.

Run:

```bash
python3.14 -m pytest -q tests/git/test_push.py
python3.14 -m ruff check python tests
python3.14 -m ruff format --check python tests
python3.14 -m mypy python tests
```

One repository use validates a candidate, not extraction. Extract only after at
least one additional repository exercises the same unchanged contract and the
operator accepts a shared installation owner and versioning mechanism.
