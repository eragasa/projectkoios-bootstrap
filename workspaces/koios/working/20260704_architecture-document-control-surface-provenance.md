# Knowledge note: architecture document control surface

## Metadata

- Type: knowledge-note
- Status: captured
- Captured: 20260704T022900Z
- Captured by: KOIOS
- Source role: ATHENA
- Source artifact: `workspaces/athena/handoffs/incoming/architecture.documents.control-surface.20260704T000000Z.md`
- Source status: incubating
- Repository: projectkoios-bootstrap

## Provenance summary

ATHENA provided an incubating control-surface note for architecture documents.

The note defines architecture documents as controlled blueprints for bounded architectural concerns.

The note explicitly says the control surface is not yet public repo policy.

The note may be promoted later if the document shape stabilizes.

## Durable captured rules

Architecture documents MUST declare owner, scope, and target domain.

Architecture documents MUST address a bounded architectural concern.

Architecture documents SHOULD decompose that concern into subordinate concerns.

Architecture documents MUST distinguish architecture from implementation.

Architecture documents MUST use RFC-style normative language for requirements.

Architecture documents SHOULD label informational background separately from normative requirements.

Architecture documents MUST state what they control.

Architecture documents MUST state what they do not control.

Architecture documents MUST NOT present themselves as the governing standard.

Architecture documents MUST NOT silently inherit authority from nearby files or directory placement.

Architecture documents MUST make provenance explicit when authorship or delegation matters.

Architecture documents SHOULD include validation expectations.

Implementation-bearing architecture documents MUST include a verification method.

Architecture documents MUST state whether they are draft, proposed, review, accepted, or archived.

## Reviewability requirements

A reviewer MUST be able to determine the intended decision from the document alone.

A reviewer MUST be able to determine the acceptance boundary from the document alone.

A reviewer MUST be able to determine the next expected artifact from the document alone.

A reviewer MUST be able to identify whether implementation work is required, deferred, or out of scope.

A reviewer MUST be able to tell when an implementation report is sufficient to close the loop.

## Skill-derivation observations

This note suggests a reusable architecture-document authoring skill.

The skill would likely require frontmatter or metadata for owner, scope, target domain, status, provenance, and next expected artifact.

The skill would likely enforce section checks for Context, Decision, Consequences, authority boundaries, and validation expectations.

The skill should distinguish controlled blueprint documents from governing standards.

The skill should prevent directory placement from being treated as implicit authority.

## Separation from authority

This KOIOS note preserves provenance and reusable rule candidates only.

This KOIOS note does not promote the ATHENA incubating note into repo policy.

This KOIOS note does not create architecture-document standards by itself.

Promotion would require the appropriate architecture, policy, ADR, or workflow authority surface.

## Candidate follow-up

ATHENA should decide whether to promote the incubating control-surface note into a durable architecture-document convention.

KOIOS should compare future architecture-document examples against this captured shape before recommending a reusable skill.
