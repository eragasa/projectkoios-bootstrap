# AAR 20260702.181459: Architecture Index Table Normalization

## Scope

ATHENA session in `projectkoios-bootstrap` normalizing the `architecture.00` table so the left side is an `architecture.*` note and the right side is the controlling `adr.*` reference.

## What happened

- Converted the architecture index table from direct ADR entries to architecture-note entries
- Added wrapper architecture notes for the ADR-driven rows that did not already have note surfaces
- Kept `architecture.lifecycle.00`, `architecture.adr.template`, and `architecture.adr.names` as existing navigation notes
- Preserved `None` for rows that are not controlled by an ADR

## Process issues

- The initial partial update only changed one row, which did not match the requested table-wide convention
- The user clarified the table-wide rule explicitly, requiring full normalization rather than a single-row fix

## Proposed follow-up improvements

- Apply the same architecture-note / controlling-ADR split consistently across other index tables if they still mix note and ADR surfaces
- Prefer whole-table replacement when a convention change affects every row

## Candidate ADR or implementation topics

- Architecture index row convention for note/control separation
- Generation rules for wrapper `architecture.*` notes

## Current status

`architecture.00` table normalized to the requested pattern.
