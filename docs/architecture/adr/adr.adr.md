---
status: active
created_datetime: 20260702.213500Z
creator: user(Eugene Joseph M. Ragasa)
submitted by: HERMES
repository: projectkoios-bootstrap
"scope:": "[projectkoios-bootstrap.*]"
architecture-domain:
---

# ADR 20260702.213500Z: ADR Namespace Authority

## Status

active
date: 20260702.213500Z

## Context

Origin: user request
From: HERMES
Acting-As: HERMES on behalf of user(Eugene)
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Architecture-Domain: software

The repository needs one top-level authority for the `adr.adr-*` family so naming, lifecycle, binding, and template rules do not drift into separate competing surfaces. Without a single root authority, the ADR namespace splits into overlapping local conventions that are hard to review consistently.

adr.adr
  ├── defines: ADR syntax
  ├── defines: ADR lifecycle
  └── constrains: all other ADRs


## Language
Language in ADRs is governed by [RFC2119](https://www.rfc-editor.org/info/rfc2119/)
## Definitions

#### Definition: ADR name space authority
- the root ADR that governs the a family of ADR documents.


#### Definition: ADR namespace family
the linked ADRs that define naming, lifecycle, workflow binding, template contract, and related meta-rules for ADRs.
- Root authority: the top-level ADR that other `adr.adr-*` files reference as their shared authority surface.

##### Implementation: .md
For a family of documents with the name
- `adr.<topic>-<subtopic>-<subsubtopic>-*.md`
- The ADR name space authority is `adr.<topic>.md`
- The

#### Defintion: ADR Status
enumerated statuses

## Rules

##### Rule


## Decision

Adopt `adr.adr.md` as the top-level authority for the ADR namespace family.

`adr.adr.md` is the root authority for:
- ADR naming rules
- ADR lifecycle rules
- ADR workflow binding rules
- ADR template contract rules
- ADR namespace structure and navigation rules

The root authority does not replace the linked child ADRs. Instead, it establishes the shared authority surface that those child ADRs must align with.

## DOC CONTROL NUMBER

Every ADR in the repository must declare a DOC CONTROL NUMBER in the form:

`ADR-<UPPERCASE-PARENT-NAMESPACE>-<DATETIME>`

Example:

`ADR-UI-CORE-20260702.213000Z`

This standard is defined by `adr.adr.md` and all child ADRs must follow it.

Rules:
- the prefix is always `ADR-`
- the parent namespace is written in uppercase kebab form
- the timestamp uses the same `YYYYMMDD.HHMMSSZ` style used elsewhere in ADR status metadata
- the DOC CONTROL NUMBER must be stable enough to identify the ADR surface across reviews and edits
- the `dcn` field is the canonical record of the DOC CONTROL NUMBER
- filenames may echo the same control number, but the field in the ADR body remains authoritative

## Family

- [adr.adr-filename-naming-convention](adr.adr-filename-naming-convention.draft.md)
- [adr.adr-lifecycle](adr.adr-lifecycle.draft.md)
- [adr.adr-lifecycle-promotion-mechanics](adr.adr-lifecycle-promotion-mechanics.md)
- [adr.adr-names](adr.adr-names.draft.md)
- [adr.adr-template-contract](adr.adr-template-contract.md)
- [adr.adr-title-naming-convention](adr.adr-title-naming-convention.draft.md)
- [adr.adr-workflow](adr.adr-workflow.draft.md)

## Consequences

- the ADR meta-surface has a single root authority
- naming, lifecycle, and binding rules can be reviewed against one top-level file
- child ADRs can specialize without inventing competing authority
- architecture notes can point to one obvious ADR root

## architecture-spec

The `adr.adr.md` authority surface should define:
- the scope of the ADR namespace family
- the rule that `adr.adr-*` files remain aligned with the root authority
- the relationship between the root authority and the child meta-ADRs
- the boundary between namespace authority and instance-level ADR content

It should not define:
- ordinary product architecture decisions
- implementation internals
- runtime behavior outside ADR management

## acceptance-criteria

- a reviewer can identify `adr.adr.md` as the ADR namespace root
- the linked meta-ADRs can be treated as children of a single authority surface
- the root authority is narrow enough to stay about ADR namespace governance
- instance-level ADRs do not have to repeat namespace authority language

## implementation-brief

If accepted, update the ADR namespace index and related guidance so `adr.adr.md` is the top-level authority for the `adr.adr-*` family and child meta-ADRs link back to it.

verification_method: review the ADR namespace family and confirm that the naming, lifecycle, workflow binding, and template rules all point back to one root authority instead of several competing roots.

## resolved_open_questions

- Should the root authority remain one file or be split into a root plus child authority set?
- Should `architecture.adr.00` explicitly link to the root authority?
- Should the root authority govern only meta-ADRs or also related architecture notes?

## non_goals

- replacing the ADR schema
- redefining product architecture decisions
- collapsing child ADRs into one file
- changing runtime behavior outside the ADR namespace

## validation_expectations

- the ADR namespace family can be traced back to one top-level authority file
- child ADRs remain independently readable
- namespace rules do not need to be re-invented in each child file

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Top-level authority for the `adr.adr-*` family.

## links

- back_to: architecture.00
- related: [ADR 20260702.182000: ADR Lifecycle Policy](adr.adr-lifecycle.draft.md)
- related: [ADR 20260702.180215: ADR Names](adr.adr-names.draft.md)
- related: [ADR 20260701.131629: Canonical ADR proposal template](adr.adr-template-contract.md)
- related: [ADR 20260702.125257Z: ADR-to-Workflow Binding](adr.adr-workflow.draft.md)
- supersedes: None
- superseded_by: None
