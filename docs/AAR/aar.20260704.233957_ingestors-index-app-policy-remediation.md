# AAR 20260704.233957: Ingestors index/app policy remediation

## Scope

VULCAN continued Python policy remediation by targeting `src/python/projectkoios/ingestors/index.py` and `src/python/projectkoios/ingestors/app.py`.

## What happened

- Added public docstrings, JSON aliases, and local purpose comments.
- Preserved app validation issue text by using typed `sys.exception()` variables instead of unannotated exception locals.
- Validated with policy validator, mypy, and full pytest.
- Recorded implementation evidence in `docs/implementation/implementation-report.20260704.233957_ingestors-index-app-policy-remediation.md`.

## Process issues

- An initial exception-message simplification broke an existing test; preserving original issue text is required for behavior compatibility.

## Proposed follow-up improvements

- Continue with `config.py` or `schemas.py` as focused slices.

## Candidate ADR or implementation topics

- Next implementation topic: bounded remediation of remaining ingestors files.

## Current status

Ingestors index/app remediation is complete from VULCAN's implementation side. Remaining `src/python` baseline is 97 findings.
