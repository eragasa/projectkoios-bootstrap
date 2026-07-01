# AAR 20260701.131900: Architecture frontmatter conversion

## Scope

Converted the bootstrap `architecture.*` notes to frontmatter-based metadata.

## What happened

Rewrote the `architecture.*` notes so each file now starts with YAML frontmatter
containing `status` and `date`, followed by the note title.

## Process issues

- The status/date metadata was easy to read in prose but harder to parse
  uniformly.
- Frontmatter is a better fit for machine-consumable note metadata.

## Proposed follow-up improvements

- Add a note template that emits the frontmatter block automatically.
- Decide whether additional fields such as `aliases` or `kind` should be added
  to the architecture note frontmatter.

## Candidate ADR or implementation topics

- Bootstrap note template for architecture documents.
- Standard frontmatter schema for durable note metadata.

## Current status

Complete.
