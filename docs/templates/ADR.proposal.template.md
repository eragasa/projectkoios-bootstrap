```json
{
  "record_id": "adr.<topic>",
  "schema_id": "https://projectkoios.local/schemas/schema.record-base.json",
  "schema_version": "0.1.0-draft",
  "record_version": "0.1.0-draft",
  "title": "<Title>",
  "status": "draft",
  "created_on": "<YYYYMMDD.HHMMSSZ>",
  "updated_on": "<YYYYMMDD.HHMMSSZ>",
  "origin": {
    "type": "<user_request|agent_proposal|migration>",
    "method": "manual",
    "actor": "<ATHENA|VULCAN|KOIOS|HERMES>",
    "authority": "<user|accepted_adr|draft>"
  },
  "scope": "<repository-or-scope>",
  "repository": "<repository-name>",
  "domain": {
    "domain_type": "architecture",
    "domain_subtype": "<domain-subtype>",
    "domain_scope": "<bounded-scope>"
  },
  "source_artifacts": [],
  "derived_from": [],
  "evidence": [],
  "projections": [
    {
      "path": "docs/adr/adr.<topic>.md",
      "projection_type": "editable_markdown",
      "source_record_id": "adr.<topic>",
      "source_schema_id": "https://projectkoios.local/schemas/schema.record-base.json",
      "source_schema_version": "0.1.0-draft",
      "projection_method": "manual",
      "generated_by": "<ATHENA|VULCAN|KOIOS|HERMES>",
      "editable": true,
      "source_of_truth": "projection"
    }
  ]
}
```

# ADR: <Title>

> Legacy Markdown render example. Canonical ADR metadata and provenance live in the leading JSON block.
> Controlled by: [adr.adr-template-contract](../adr/adr.adr-template-contract.md).
> Template index: [templates.00](templates.00.md).

## Status

<proposal | draft | accepted | active | superseded>

## Normative language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** in this ADR are to be interpreted as described in RFC 2119 and RFC 8174 when, and only when, they appear in all capitals.

## Context

<Describe the problem, why it matters, and the current state. Do not duplicate metadata/provenance that belongs in the leading JSON block.>

## Decision

<State the proposal or active decision. Use descriptive prose first, then normative bullets if the section contains requirements.>

## Consequences

<Describe trade-offs, follow-on work, and validation impact. Use normative bullets when listing requirements.>

## Architecture spec

<Bounded architecture decision for one domain.>

## Acceptance criteria

- MUST <Criterion 1>
- SHOULD <Criterion 2>
- MAY <Criterion 3>

## Implementation brief

<Describe downstream follow-up expected, or state that no implementation is requested.>

### Verification method

<How Vulcan validates completion — e.g., `pytest tests/foo.py`, AST check, manual inspection, Graphify diff. Required for any implementation-bearing ADR.>

## Comments

Comments remain open while this ADR is in draft status. When the ADR is promoted, comments are resolved, preserved as provenance, or moved to follow-up artifacts.

- ATHENA: <comment or concern>
- VULCAN: <comment or concern>
- KOIOS: <comment or concern>
- HERMES: <comment or concern>

## Resolved open questions

- MUST <Question or decision point 1>
- SHOULD <Question or decision point 2>

## Non-goals

- MUST NOT <Non-goal 1>
- SHOULD NOT <Non-goal 2>

## Validation expectations

- MUST <How the resulting ADR, workflow, or artifact should be validated>

## Document state

- MUST treat Owner as <Hermes | Athena | Vulcan | Koios>.
- MUST treat Current phase as <proposal | draft | accepted | active | superseded>.
- MAY include additional document-domain consistency guidance.
