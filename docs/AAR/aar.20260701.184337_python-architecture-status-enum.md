# AAR 20260701.184337: Python architecture status enum

## Scope

Added the Python `ArchitectureDocumentStatus` enum under `src/python/projectkoios/bootstrap/architecture/documents.py`.

## What happened

The user chose the Python placement and requested the enum be written directly into the repo. I created the `architecture` package and exported the enum from its `__init__.py`.

## Process issues

- None observed.

## Proposed follow-up improvements

- If more architecture models are added, keep them grouped under the same package.
- Add tests or schema bindings once the Python model shape settles.

## Candidate ADR or implementation topics

- Python architecture document model
- Cross-language docs model bindings
- Active-vs-archived architecture document naming policy

## Current status

The enum is implemented in Python. Other language versions remain pending by design.
