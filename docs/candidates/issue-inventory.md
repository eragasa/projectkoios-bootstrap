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

The command reads canonical GitHub host/owner/repository identities from
`maps/repositories.md`, verifies that each sibling checkout's `origin` matches,
and queries only those canonical repositories. A local origin is consistency
evidence, not authority. The command uses the GraphQL issue connection to
retrieve only issue numbers, titles, URLs, and pagination metadata; pull
requests are excluded by construction. Queries
are read-only, fetch at most 10,000 issues per repository, reject repeated
pagination cursors and inconsistent totals, write no cache, and store no
generated inventory.

Live and replay JSON reject duplicate fields throughout. Replay objects and
normalized issue records also reject unknown fields; extra fields in the live
GraphQL envelope are ignored because the query selects and validates only the
required connection values. Every issue URL must be an HTTPS URL for the
resolved host, owner, repository, issue path, and
issue number, with no controls, credentials, port, query, or fragment. Output
uses a canonical URL reconstructed from the validated identity rather than the
supplied string. Human-readable summary output points to `--details` whenever
issue rows are omitted.

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

A replay fixture must exactly cover its selected map, carry a canonical UTC
observation time (`YYYY-MM-DDTHH:MM:SSZ`), use an integer schema version, and
provide either one or more normalized page arrays of issue records (an empty
result is `[[]]`) or one bounded error kind for every repository. It is not a
raw live GraphQL capture format. The file is
limited to 16 MiB; page, issue, title, and URL bounds mirror the live contract.
Duplicate or unknown fields, boolean schema values, mismatched issue URLs, and
malformed timestamps fail closed. The command has no capture or record mode. Live
responses and generated reports must not be committed as fixtures; tracked
fixtures must remain synthetic or sanitized.

## Limitations

- This inventories open issues; it does not infer priority, dependencies, or the
  next task.
- Live mode requires every mapped sibling checkout and an `origin` matching the
  map's canonical GitHub identity. Missing or divergent checkouts make the
  report incomplete even when GitHub itself is reachable.
- GitHub issue visibility follows the operator's existing `gh` authentication.
- Sequential per-repository queries favor simple failure attribution over speed.
  `observed_at` is collection start, and `COMPLETE` means full protocol coverage,
  not a transactionally atomic cross-repository snapshot.
- A repository with more than 10,000 open issues is reported as incomplete
  rather than consuming unbounded normalized issue memory. The human-reviewed
  map and trusted local `gh` process output are not process-level byte-stream
  capped; add such caps before accepting arbitrary maps, executables, or hosts.
- This first observation does not establish recurrence or production readiness.

## Promotion condition

Do not make this command mandatory in `AGENTS.md`, install it, or present it as
validated tooling until an independent second use and the promotion evidence in
`docs/harness-incubation.md` are recorded on the owner issue.
