# AAR 20260702.021842: Harness identity prose refactor

## Scope

Repo-wide prose cleanup to move from `pi`-centric wording toward encapsulated
harness identities, while preserving machine-facing paths and runtime names.

## What happened

- Swept markdown prose across active docs, archives, skills, handoffs, and AARs.
- Updated role wording so Hermes is treated as the identity in prose while
  `pi` remains in path/runtime references where appropriate.
- Normalized the Hermes workspace AGENT file and related templates.
- Ran `graphify update .` after the documentation edits.

## Process issues

- A broad text-replacement pass can overreach into historical provenance and
  produce awkward residue that needs a follow-up cleanup.
- Some archive and template files require line-by-line judgment instead of a
  pure regex sweep.

## Proposed follow-up improvements

- Add a small review checklist for repo-wide prose refactors: path tokens,
  provenance fields, and historical archives should be handled separately.
- Consider a dedicated identity/provenance glossary so future sweeps know which
  `pi` references are runtime identifiers versus prose-era role labels.

## Candidate ADR or implementation topics

- Prose/style rules for identity-vs-harness wording
- Historical archive preservation policy for role-name migrations

## Current status

Documentation sweep completed; repo still has intentionally preserved runtime
`pi` paths and provenance fields.
