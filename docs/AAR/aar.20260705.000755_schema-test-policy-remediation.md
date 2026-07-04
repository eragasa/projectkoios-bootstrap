# AAR 20260705.000755: Schema test policy remediation

## Scope

VULCAN began applying the Python policy validator to test code and remediated the schema test package.

## What happened

- Ran `projectkoios bootstrap validate-python-policy --all` to establish the all-target test-code baseline.
- Remediated `tests/projectkoios/bootstrap/schema/` with docstrings, return annotations, local annotations, and purpose comments.
- Wrote `docs/implementation/implementation-report.20260705.000755_schema-test-policy-remediation.md`.
- Updated Vulcan workspace state and active files.

## Process issues

- Applying the source-oriented policy to tests creates a large findings baseline, mostly because test code historically did not require public docstrings and local annotations.
- Direct frozen dataclass assignment in tests triggered mypy even though it was intentionally inside `pytest.raises`; `setattr` better expresses that runtime immutability is under test.

## Proposed follow-up improvements

- Continue test remediation by bounded package/file group rather than one large patch.
- Consider whether test-specific rule relaxations are warranted for public test function docstrings or fixture helpers.

## Candidate ADR or implementation topics

- Implementation topic: ingestors test policy remediation.
- Implementation topic: root harness/bootstrap test policy remediation.
- Policy topic: source vs test Python policy profile distinction.

## Current status

Schema tests pass policy validation with zero findings. Remaining all-target policy baseline is 753 findings across 107 files.
