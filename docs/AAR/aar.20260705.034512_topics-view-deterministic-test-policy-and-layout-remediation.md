# AAR 20260705.034512: Topics view deterministic test policy and layout remediation

## Scope

VULCAN bounded remediation of the topics-view deterministic/read-only tests against `docs/policies/python-coding.md`, `docs/policies/python-testing.md`, and the continuing direction to process remaining findings one file at a time.

## What happened

- Moved `tests/harness/handoffs/__TopicsView__build_topics_view__deterministic_and_readonly.py` to `tests/projectkoios/bootstrap/harness/handoffs/test__TopicsView__build_topics_view__deterministic_and_readonly.py`.
- Remediated the moved file with generated-docs-compatible docstrings, local annotations, and purpose comments.
- Validated the focused file with policy validation, mypy, focused pytest, full pytest, and refreshed Graphify.

## Process issues

- No new process issue beyond the ongoing partial migration of legacy test layout.

## Proposed follow-up improvements

- Continue policy remediation one file at a time, preserving package-mirroring test layout for each touched file.

## Candidate ADR or implementation topics

- No ADR is created by this AAR. Possible implementation topic: complete package-mirroring test layout migration for legacy `tests/harness/` files.

## Current status

The remediation slice is complete and recorded in `docs/implementation/implementation-report.20260705.034512_topics-view-deterministic-test-policy-and-layout-remediation.md`. Whole-repo policy validation remains incomplete at `143 finding(s), 107 file(s)`.
