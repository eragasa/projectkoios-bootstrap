# AAR 20260702.052145: Blind commit-all scope

## Scope
Repository commit/push operation.

## What happened
User requested a full commit and push without further checking. The operation used a force add across the repo, which captured ignored workspace content and generated artifacts in addition to the intended edits, then pushed them upstream.

## Process issues
- "Commit all" was treated too literally for a repo with ignored/generated surfaces.
- Force-adding the whole tree pulled in large numbers of generated and workspace files.
- The request did not leave room for scope trimming, but the resulting change set was much broader than the earlier targeted edit.

## Proposed follow-up improvements
- Define a safer default for bulk commit requests in repos with ignored workspaces.
- Distinguish intended tracked changes from generated/local artifacts before force-adding.
- If the user wants true everything, confirm that ignored/generated files are included.

## Candidate ADR or implementation topics
Bulk-commit guardrails for mixed-source bootstrap repositories.

## Current status
Completed and pushed; process lesson recorded.
