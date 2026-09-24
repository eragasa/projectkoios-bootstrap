# Offline artifact archive candidate

## Lifecycle

**Repeated.** PyFlamestk first exercised exact staging verification,
deterministic private archive creation, and complete recovery for 161 artifacts
and 250,836,932 bytes. PyPosPack independently exercised the generic
declarative staging policy, verification, archive, and recovery path for 5,396
artifacts and 637,072,563 bytes. Both repositories retained source-specific
selection and licensing decisions.

## Purpose

This candidate applies a repository-owned declarative selection policy, stages
selected tracked artifacts, verifies an offline-artifact tree, publishes a
deterministic tar bundle outside the source repository, and safely recovers the
bundle. It preserves:

- original repository-relative paths;
- SHA-256 and byte-size identities;
- caller-supplied artifact classifications;
- the exact source Git commit and tree;
- the declared upstream repository URL; and
- the completed tar archive's SHA-256 identity.

The candidate does not decide which files should leave a repository. That
policy belongs to the source repository and may depend on authorship,
licensing, calculator behavior, generated-file conventions, and release scope.
A policy can select exact basenames, path prefixes, basename regular
expressions, or path regular expressions. Rules are ordered and the first match
owns the classification.

## Interface

The implementation is
`python/projectkoios/bootstrap/harness/offline_artifacts.py`. Its primary entry
points are:

- `read_selection_policy(...)`;
- `select_tracked_artifacts(...)`;
- `stage_artifacts(...)`;
- `read_manifest(...)`;
- `verify_staging(...)`;
- `verify_git_source(...)`;
- `create_archive(...)`; and
- `restore_archive(...)`.

Stage a clean source checkout using its tracked TOML policy:

```bash
PYTHONPATH=python python3.14 -m \
  projectkoios.bootstrap.harness.offline_artifacts stage \
  --repository-root /explicit/source/checkout \
  --policy offline-artifacts.toml \
  --destination .offline/release-readiness \
  --checksum-manifest OFFLINE_ARTIFACT_SHA256SUMS \
  --remove-originals
```

The destination must be ignored, absent, and repository-relative. Staging
copies and verifies every selected regular file before publishing the complete
staging tree and checksum manifest. `--remove-originals` is explicit; without
it, source files remain. Removal begins only after the verified copies and both
manifests exist.

The canonical manifest is path-sorted TSV:

```text
sha256<TAB>byte_size<TAB>reason<TAB>original_path
```

Every path is normalized, relative, unique, and bound to one regular file.
`MANIFEST.tsv` is reserved for metadata and cannot be selected as an artifact.

Verify a staging tree and its source revision:

```bash
PYTHONPATH=python python3.14 -m \
  projectkoios.bootstrap.harness.offline_artifacts verify \
  --staging-root /explicit/staging/root \
  --manifest /explicit/MANIFEST.tsv \
  --source-checkout /explicit/source/checkout \
  --source-revision 0123456789abcdef0123456789abcdef01234567 \
  --source-repository-url https://example.invalid/source.git
```

Create an external archive bundle:

```bash
PYTHONPATH=python python3.14 -m \
  projectkoios.bootstrap.harness.offline_artifacts archive \
  --staging-root /explicit/staging/root \
  --manifest /explicit/MANIFEST.tsv \
  --destination-directory /explicit/offline/destination \
  --archive-prefix source-offline-artifacts \
  --source-checkout /explicit/source/checkout \
  --source-revision 0123456789abcdef0123456789abcdef01234567 \
  --source-repository-url https://example.invalid/source.git
```

The destination must not already exist and must be outside both staging and the
source checkout. The candidate creates a sibling temporary directory and
atomically publishes the completed destination.

Recover into a new directory outside the evidence bundle:

```bash
PYTHONPATH=python python3.14 -m \
  projectkoios.bootstrap.harness.offline_artifacts restore \
  --archive /explicit/bundle/source-offline-artifacts-git-0123456789ab.tar \
  --archive-checksum \
    /explicit/bundle/source-offline-artifacts-git-0123456789ab.tar.sha256 \
  --manifest /explicit/bundle/MANIFEST.tsv \
  --destination-directory /explicit/new/recovery-directory
```

Recovery requires an absent destination and refuses to write inside the
evidence directory. It verifies the archive SHA-256, canonical manifest,
complete archive member set, safe relative paths, entry types, declared sizes,
and every recovered file identity. Artifacts are written as `0600`, directories
as `0700`, and the completed recovery directory is published atomically. It
never uses a general-purpose tar extraction operation and never writes into a
source checkout automatically.

## Output contract

A completed destination contains:

- an uncompressed deterministic `.tar` archive;
- `MANIFEST.tsv` in canonical form;
- `<archive>.sha256`; and
- `SOURCE.json` with the repository, commit, tree, collection size, and archive
  identity.

The tar contains only canonical `MANIFEST.tsv`, selected artifacts, and required
directory entries. Ownership and timestamps are normalized. Artifact and
manifest modes are `0600`; directory modes are `0700`. No absolute path,
symlink, hard link, or unselected file enters the archive.

Uncompressed tar is intentional: it is widely readable and separates byte
preservation from optional storage compression. Compression, encryption,
Dropbox synchronization, publication, and offline-media management remain
operator actions.

## Safety and limits

Default limits are:

- 10,000 artifact records;
- 100,000,000,000 bytes per artifact;
- 1,000,000,000,000 bytes total;
- 10,000,000 manifest bytes; and
- 4,096 UTF-8 bytes per relative path.

The candidate requires a clean repository before staging and rejects invalid
or ambiguous policy structures, symlink roots, symlink entries, non-regular
entries, extra or missing staged files, path traversal, duplicate records,
identity
mismatches, and mutation detected during descriptor-bound reads. Git access is
limited to fixed `rev-parse` and `cat-file` commands against an explicit local
checkout and exact object ID. It never fetches, checks out, imports, evaluates,
or executes source content.

Archive creation performs full staging and Git verification first. While
writing, each artifact is hashed again and descriptor metadata is checked for
mutation. Recovery performs an independent archive-to-new-directory round trip
and rechecks every identity. Publication is atomic at each destination-directory boundary. Source removal
occurs only when the staging caller supplies `--remove-originals`, and only
after verified staging and checksum manifests exist. The candidate never
removes staged, archive, or recovered bytes.

The archive is private preservation evidence, not proof of redistribution
rights, reproducibility, numerical correctness, or scientific validity.

## Replay and validation

For identical artifact bytes, manifest records, source identity, and archive
prefix, archive bytes are deterministic. Tests construct sanitized temporary
Git history and synthetic artifacts, perform a complete archive-and-recovery
round trip, and reject a mismatched archive checksum. No PyFlamestk, calculator,
or private data is retained in this repository.

Run:

```bash
PYTHONPATH=python python3.14 -m unittest \
  tests.harness.test_offline_artifacts
ruff check python tests
ruff format --check python tests
PYTHONPATH=python mypy \
  python/projectkoios/bootstrap/harness tests/harness
```

## Limitations and stop conditions

- The source repository owns and reviews the declarative selection policy; the
  generic tool applies it but cannot determine authorship or licensing.
- Original removal is multi-file and cannot be filesystem-atomic. Verified
  staging remains available if removal is interrupted.
- The verifier requires artifact paths to exist at the selected Git commit.
- Git SHA-1 and SHA-256 object IDs are accepted; other version-control systems
  are unsupported.
- The archive is intentionally uncompressed and unencrypted.
- Recovery restores selected artifact bytes and relative paths only; it does not
  restore Git tracking, repository history, original timestamps, ownership, or
  source-specific execution context.
- Staging and recovery evidence must remain quiescent. Descriptor checks detect
  file mutation, but the candidate does not claim protection against hostile
  concurrent replacement of parent directories.
- The candidate does not confirm that a cloud client completed remote sync.
- Do not add automatic uploads, credential handling, source fetching, history
  rewriting, workflow state, or artifact discovery.

## Revisit and extraction criteria

Independent PyPosPack reuse established recurrence. The full generic staging
path still has one production use, so the candidate remains `repeated` rather
than `validated`. Revisit validation after another independent repository uses
policy-driven staging and completes recovery, or after a concrete failure
changes the contract. If the mechanics become useful outside Project Koios,
promotion requires an explicitly accepted generic-tool owner; the bootstrap
repository must not become a package manager or storage service.
