# AAR 20260702.201751: Deprecate Incubator and Spikes Directories

## Scope

ATHENA session in `projectkoios-bootstrap` deprecating the legacy `docs/incubator/` and `docs/spikes/` directories and migrating their contents out of those surfaces.

## What happened

- Rewrote the idea/spike workflow ADR to treat `docs/incubator/` and `docs/spikes/` as deprecated
- Rewrote the lifecycle ADR and promotion-mechanics ADR to use `reporoot/spike/<spike-id>/` and `reporoot/dev/<proposal-id>/`
- Rewrote the lifecycle index and policy consumption note to match the new active/historical/rejected model
- Moved the remaining incubator/spike content into archive locations and removed the legacy directories
- Updated the brainstorm template to describe brainstorm notes without relying on the deprecated incubator surface

## Process issues

- The repository had two legacy staging directories that were still being treated as active workflow surfaces
- The workflow needed a clearer split between durable ADR records and deprecated scratch surfaces

## Proposed follow-up improvements

- Decide whether the legacy brainstorm template should also be renamed to remove `incubator` from the filename
- Continue migrating any remaining historical references as needed, but keep new work out of the deprecated directories

## Candidate ADR or implementation topics

- Formal archive conventions for deprecated scratch surfaces
- Filename cleanup for remaining legacy brainstorm artifacts

## Current status

Legacy incubator/spike directories removed; active docs now point at the repo-root spike/dev surfaces and ADR-linked documents.
