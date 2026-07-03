# Schema: process-chain note

## Status

Reusable schema, non-authoritative.

## Purpose

A process-chain note records how one inspectable software-development slice moved between roles through filesystem-visible artifacts.

A process-chain note preserves artifact order, predecessor links, expected successors, evidence links, and reusable process observations.

A process-chain note MUST NOT replace an implementation report, architecture review, AAR, ADR, or workflow policy.

## Required sections

```md
# Process chain: <slice title>

## Metadata

- Type: process-chain
- Scope:
- Repository:
- Roles:
- Status: observed | captured | reviewed | superseded
- Current step:
- Previous artifact:
- Next expected artifact:

## Artifact chain

| Step | Role | Artifact | Links backward to | Expected successor | Status |
|---|---|---|---|---|---|

## Architecture document links

## Implementation document links

## Validation links

## Review links

## Process observations

## Provenance gaps

## Reusable lessons

## Candidate follow-ups

## Non-authority statement

This note records process provenance only.

This note does not create architecture, implementation, or workflow authority.
```

## Status values

`observed` means the chain has been noticed but not fully captured.

`captured` means the chain has enough links and evidence to be useful as provenance.

`reviewed` means another role has inspected the capture for accuracy.

`superseded` means a newer process-chain note replaces this note.

## Linking rule

Each process-chain note MUST identify the previous artifact.

Each process-chain note SHOULD identify the next expected artifact.

Each row in the artifact chain SHOULD link backward to the artifact that enabled it.

## Evidence rule

Claims about implementation MUST link to implementation documents, commits, or validation output.

Claims about architecture review MUST link to architecture documents or review artifacts.

Claims about process quality SHOULD identify the artifact sequence that supports the observation.
