# Offline artifact archive candidate

## Lifecycle

**Observed.** One PyFlamestk release-readiness cleanup motivated this
extraction. The source-specific selection policy remains in PyFlamestk;
independent reuse has not yet established recurrence.

## Purpose

This candidate verifies an explicitly selected offline-artifact staging tree
and publishes a deterministic tar bundle outside the source repository. It
preserves:

- original repository-relative paths;
- SHA-256 and byte-size identities;
- caller-supplied artifact classifications;
- the exact source Git commit and tree;
- the declared upstream repository URL; and
- the completed tar archive's SHA-256 identity.

The candidate does not decide which files should leave a repository. That
policy belongs to the source repository and may depend on authorship,
licensing, calculator behavior, generated-file conventions, and release scope.

## Interface

The implementation is
`python/projectkoios/bootstrap/harness/offline_artifacts.py`. Its primary entry
points are:

- `read_manifest(...)`;
- `verify_staging(...)`;
- `verify_git_source(...)`; and
- `create_archive(...)`.

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

The candidate rejects symlink roots, symlink entries, non-regular entries,
extra or missing staged files, path traversal, duplicate records, identity
mismatches, and mutation detected during descriptor-bound reads. Git access is
limited to fixed `rev-parse` and `cat-file` commands against an explicit local
checkout and exact object ID. It never fetches, checks out, imports, evaluates,
or executes source content.

Archive creation performs full staging and Git verification first. While
writing, each artifact is hashed again and descriptor metadata is checked for
mutation. Publication is atomic at the destination-directory boundary. The
candidate never removes source or staged bytes.

The archive is private preservation evidence, not proof of redistribution
rights, reproducibility, numerical correctness, or scientific validity.

## Replay and validation

For identical artifact bytes, manifest records, source identity, and archive
prefix, archive bytes are deterministic. Tests construct sanitized temporary
Git history and synthetic artifacts; no PyFlamestk, calculator, or private data
is retained in this repository.

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

- Artifact selection and movement remain source-repository responsibilities.
- The verifier requires artifact paths to exist at the selected Git commit.
- Git SHA-1 and SHA-256 object IDs are accepted; other version-control systems
  are unsupported.
- The archive is intentionally uncompressed and unencrypted.
- Staging must remain quiescent. Descriptor checks detect file mutation, but the
  candidate does not claim protection against hostile concurrent replacement
  of parent directories.
- The candidate does not confirm that a cloud client completed remote sync.
- Do not add automatic uploads, credential handling, source fetching, history
  rewriting, workflow state, or artifact discovery.

## Revisit and extraction criteria

Use with PyPosPack or another independent repository is required before marking
this candidate `repeated`. Revisit limits and manifest semantics only when that
reuse produces concrete evidence. If the mechanics become useful outside
Project Koios, promotion requires an explicitly accepted generic-tool owner;
the bootstrap repository must not become a package manager or storage service.
