# ADR Kernel

## Status

active

## Purpose

This kernel defines the minimum control rules for ADR-driven implementation.

## Core Objects

The system uses three control objects:

* ADR
* Implementation
* USER approval

## ADR Rule

An ADR defines authority.

An ADR may be in one state:

* `draft`
* `proposed`
* `active`
* `deprecated`
* `archived`

Filename rule:

* `adr.<name>.draft.md`
* `adr.<name>.proposed.md`
* `adr.<name>.md`

`adr.<name>.md` means `active`.

## Implementation Rule

An implementation record defines bounded implementation work.

Implementation surface:

* `implementation.<name>.md`

Machine record:

* `implementation.<name>.json`

Working directory:

* `implementation/<name>/`

Production target:

* `src/python/projectkoios/bootstrap/*`

## Promotion Path

| Stage | State      | Surface                                                                              | Allowed Work                       | Forbidden Work                 |
| ----- | ---------- | ------------------------------------------------------------------------------------ | ---------------------------------- | ------------------------------ |
| 1     | `draft`    | `adr.<name>.draft.md`                                                                | comment, review, feasibility notes | implementation                 |
| 2     | `draft`    | `adr.<name>.draft.md` + `spike/<name>/`                                              | exploratory spike                  | production code                |
| 3     | `proposed` | `adr.<name>.proposed.md` + `implementation.<name>.md` + `implementation.<name>.json` | implementation planning            | unapproved implementation      |
| 4     | `proposed` | `implementation/<name>/`                                                             | USER-approved plan items           | scope expansion                |
| 5     | `active`   | `adr.<name>.md` + `src/python/projectkoios/bootstrap/*`                              | productionized implementation      | unapproved production movement |

## VULCAN Rules

VULCAN MUST implement only from an approved source.

Approved sources are:

* explicit USER instruction
* active ADR
* proposed ADR with USER-approved implementation item
* implementation brief
* acceptance criterion
* failing test being fixed

VULCAN MUST NOT treat its own plan as approval.

VULCAN MUST NOT invent architecture.

VULCAN MUST NOT expand scope while implementing.

VULCAN MUST stop and report if the task requires architecture clarification.

VULCAN MUST separate `DataObject` from `ActionObject`.

VULCAN MUST preserve YAGNI.

## DataObject Rule

A `DataObject` represents structured state.

A `DataObject` MUST NOT orchestrate workflows, mutate files, call external commands, or approve decisions.

## ActionObject Rule

An `ActionObject` represents an operation or transition.

An `ActionObject` MUST declare what it reads, what it writes, whether it mutates state, and how it is validated.

## USER Approval Rule

The USER is the human terminal operator.

Only the USER approves canonical repository mutation.

A generated plan is not approval.

A proposal is not approval.

An implementation record is not approval unless it records explicit USER approval.

## Deviation Rule

If implementation reveals that the approved plan is wrong, incomplete, too broad, or requires architecture clarification, VULCAN MUST stop and write a deviation report.

VULCAN MUST NOT silently continue through a deviation.
