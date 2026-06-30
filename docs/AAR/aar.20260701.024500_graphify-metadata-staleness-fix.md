# AAR 20260701.024500: Graphify Metadata Staleness Fix

## Scope

Manual correction of stale Graphify freshness metadata for `projectkoios-bootstrap`.

## What happened

Graphify refresh runs reported no topology changes, but the stored build commit in
`graphify-out/graph.json` and `graphify-out/GRAPH_REPORT.md` remained on the old
commit. I updated both artifacts to reflect the current repository HEAD.

## Process issues

The no-op refresh path leaves the repo with a stale commit marker unless the
metadata is patched manually.

## Proposed follow-up improvements

Teach Graphify to refresh freshness metadata even when extraction is unchanged,
or emit an explicit stale-metadata warning when HEAD has advanced.

## Candidate ADR or implementation topics

Graphify metadata refresh semantics for unchanged graphs.

## Current status

The graph freshness metadata now matches the current HEAD commit. The refresh
behavior itself remains unchanged.
