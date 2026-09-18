# Project Koios issue inventory candidate

## Status

`OBSERVED_UNVALIDATED` candidate owned by
[`ISSUE-INVENTORY-01`](https://github.com/eragasa/projectkoios-bootstrap/issues/3).
It is optional, is not installed automatically, and must not yet be treated as
mandatory coordination infrastructure.

## Observation

A query scoped only to `projectkoios-bootstrap` was incorrectly generalized to
all Project Koios repositories. A subsequent map-wide query found open issues
in several owning repositories. This candidate tests whether a bounded helper
can prevent that false all-clear without copying GitHub task state locally.

## Command

The candidate requires Python 3 and an authenticated GitHub CLI with GraphQL
API support.

```bash
./scripts/koios_issues.py
./scripts/koios_issues.py --details
./scripts/koios_issues.py --json
```

The command reads repository names from `maps/repositories.md`, resolves each
sibling checkout's `origin`, and queries every resolved GitHub repository. It
uses the GraphQL issue connection to retrieve only issue numbers, titles, URLs,
and pagination metadata; pull requests are excluded by construction. Queries
are read-only, fetch at most 10,000 issues per repository, write no cache, and
store no generated inventory.

## Completeness and exit behavior

A report is `COMPLETE` only when every mapped repository resolves, authenticates,
returns a valid and internally consistent paginated response within the safety
limit, and contributes an issue count. Failed
repositories have a null JSON count and never contribute an inferred zero.

| Exit | Meaning |
|---|---|
| `0` | Complete inventory; open issues may still exist. |
| `2` | Fatal map, replay, or GitHub CLI setup error; no report is emitted. |
| `3` | A report was emitted, but at least one repository failed. |

The normalized JSON report has schema version 1 and includes:

- one observation time and `live` or `replay` source mode;
- explicit whole-report completeness;
- mapped and GitHub repository identities;
- per-repository `ok` or `error` status;
- a nullable open-issue count and bounded error kind;
- normalized issue number, title, and URL records; and
- successful, failed, repository, and known-open-issue totals.

Issue titles are stripped of terminal control and formatting characters. Raw
GitHub CLI errors are not copied into the report.

## Deterministic replay

Replay accepts an explicitly supplied synthetic fixture and performs no Git or
GitHub calls:

```bash
./scripts/koios_issues.py \
  --map tests/fixtures/issues/repositories.md \
  --replay tests/fixtures/issues/mixed-replay.json \
  --json
```

A replay fixture must exactly cover its selected map, carry a fixed observation
time, and provide either paginated API-shaped issue data or one bounded error
kind for every repository. The command has no capture or record mode. Live
responses and generated reports must not be committed as fixtures; tracked
fixtures must remain synthetic or sanitized.

## Limitations

- This inventories open issues; it does not infer priority, dependencies, or the
  next task.
- Live mode requires every mapped sibling checkout and a matching GitHub
  `origin`. Missing or divergent checkouts make the report incomplete even when
  GitHub itself is reachable.
- GitHub issue visibility follows the operator's existing `gh` authentication.
- Sequential per-repository queries favor simple failure attribution over speed.
- A repository with more than 10,000 open issues is reported as incomplete
  rather than consuming unbounded API and memory resources.
- This first observation does not establish recurrence or production readiness.

## Promotion condition

Do not make this command mandatory in `AGENTS.md`, install it, or present it as
validated tooling until an independent second use and the promotion evidence in
`docs/harness-incubation.md` are recorded on the owner issue.
