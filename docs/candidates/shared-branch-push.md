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

A newly created feature branch may still track the branch from which it was
created. Replacing that known initial upstream requires separate explicit
authority:

```bash
push-git-branch \
  --repo-path /absolute/canonical/worktree \
  --remote origin \
  --branch feature/example \
  --expected-commit 0123456789abcdef0123456789abcdef01234567 \
  --replace-upstream \
  --apply
```

Before contacting the remote, the command requires:

- an absolute, canonical worktree root;
- a valid explicit remote and branch name;
- a full lowercase SHA-1 or SHA-256 commit object ID;
- attached `HEAD`, the named local branch, and the expected commit to agree;
- a clean tracked and untracked worktree;
- no existing upstream that differs from `<remote>/<branch>`, unless
  `--replace-upstream` explicitly authorizes replacing the captured value;
- exactly one fetch endpoint and one identical push endpoint; and
- a fetch refspec mapping the branch to
  `refs/remotes/<remote>/<branch>`.

The push uses the expected object ID as the source of one exact heads refspec.
It is non-force and disables pre-push hooks, tag following, recursive submodule
pushes, configured push options, and configured push signing. Git terminal
prompting, credential interactivity, and stdin are disabled; callers must
provide already noninteractive credential, SSH, and remote helpers. Lazy
fetching, background maintenance, and inherited Git tracing or repository
redirection are disabled. The command does not use implicit push configuration
to select refs.

After the push, the command queries the same validated endpoint directly and
requires the remote branch to equal the expected commit. It rechecks local
branch identity, cleanliness, and upstream authority before setting the matching
upstream, then requires the remote-tracking ref to equal the expected commit. A
failure triggers no cleanup, retry, force push, or rollback because remote state
may already have changed. Callers must exclude concurrent local ref, worktree,
and Git-configuration writers; the command detects but cannot atomically prevent
all such changes.

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
explicit remote. The caller remains responsible for network authorization,
credentials, and noninteractive helper configuration. The candidate requires
Git 2.45 or newer and is validated with both SHA-1 and SHA-256 repositories.

## Validation and extraction gate

Tests use temporary repositories and local bare remotes. They cover dry-run
behavior, exact push and upstream evidence, dirty worktrees, expected-commit
mismatch, rejected and explicitly authorized upstream replacement, concurrent
upstream changes, mismatched push URLs, unsupported fetch mappings,
non-fast-forward rejection, hook bypass, configured push-signing suppression,
tag non-publication, canonical roots, bounded CLI
errors, and real SHA-1 and SHA-256 pushes.

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
