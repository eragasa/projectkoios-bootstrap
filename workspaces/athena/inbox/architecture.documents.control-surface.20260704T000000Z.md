# Architecture document control surface

```json
{
  "title": "Architecture document control surface",
  "datetime": "20260704T000000Z",
  "status": "incubating",
  "origin": "user request",
  "from": "ATHENA",
  "acting_as": "ATHENA",
  "scope": "projectkoios-bootstrap",
  "repository": "projectkoios-bootstrap"
}
```

## Purpose

The repository needs a control surface that governs architecture documents themselves.
ADRs capture decision-backed guidance, best practices, and avoided pitfalls.
An architecture document captures best practices and avoided pitfalls while remaining explicit and inspectable across ADRs, briefs, and related architecture notes.

## Definitions

- Scope: the bounded concern area, repository region, decision space, or artifact family that the document governs.
- Owner: the role or harness responsible for the document’s authority and maintenance.
- Target domain: the architecture area the document addresses, such as workflow, review, ingestion, or control surfaces.

## Normative language

- MUST means an absolute requirement.
- SHOULD means a strong recommendation.
- MAY means an allowed option.
- SHOULD NOT means a strong recommendation against.
- MUST NOT means an absolute prohibition.
- Architecture documents MUST use RFC-style normative terms to separate requirements from commentary.
- Any non-normative background material SHOULD be clearly labeled as informational.

## Requirements

### Identity and scope
- An architecture document MUST declare its owner, scope, and target domain.
- An architecture document MUST address a bounded architectural concern.
- An architecture document SHOULD decompose that concern into the subordinate concerns.
- An architecture document MUST distinguish architecture from implementation.

### Structure
- An architecture document MUST include Context, Decision, and Consequences.
- An architecture document SHOULD include Acceptance Criteria.
- An architecture document SHOULD include Implementation Brief guidance when downstream work is expected.
- An architecture document MAY include resolved questions, non-goals, validation expectations, and routing metadata.

### Authority
- An architecture document MUST state what it controls.
- An architecture document MUST NOT present itself as the governing standard.
- An architecture document MAY cite the standards it follows.
- An architecture document MUST state what it does not control.
- An architecture document MUST NOT silently inherit authority from nearby files or directory placement.
- An architecture document MUST make provenance explicit when authorship or delegation matters.

### Reviewability
- A reviewer MUST be able to determine the intended decision from the document alone.
- A reviewer MUST be able to determine the acceptance boundary from the document alone.
- A reviewer MUST be able to determine the next expected artifact from the document alone.
- A reviewer MUST be able to identify whether implementation work is required, deferred, or out of scope.

### Language
- Normative requirements in architecture documents MUST use RFC 2119 terms such as MUST, SHOULD, MAY, and MUST NOT.
- Informational prose SHOULD be clearly separated from normative requirements.
- Ambiguous terms SHOULD be avoided unless the document defines them.

### Validation
- An architecture document SHOULD include validation expectations.
- An implementation-bearing architecture document MUST include a verification method.
- A reviewer MUST be able to tell when an implementation report is sufficient to close the loop.

- An architecture document MUST state whether it is draft, proposed, review, accepted, or archived.

## Consequences

- Architecture documents become easier to review and compare.
- Authority boundaries become explicit instead of inferred.
- Downstream implementation work can be traced back to a bounded decision.
- The repo can derive reusable skill or workflow rules from a stable document shape.

## Process notes

This note is local and incubating.
It is not yet a public repo policy.
It MAY be promoted later into docs if the control surface stabilizes.
