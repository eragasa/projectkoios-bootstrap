# AAR 20260703.223117: Restore Vulcan workspace AGENTS

## Scope

HERMES restored `workspaces/vulcan/AGENTS.md` from repository history after the user reported that AGENTS files kept disappearing.

## What happened

The Vulcan workspace AGENTS file was missing from `HEAD` and only `.keep` remained in `workspaces/vulcan/`. Git history showed the file existed in commit `b916206` and was deleted by revert commit `5735b5f`.

## Process issues

- Workspace instruction files have churned between `AGENT.md` and `AGENTS.md` naming.
- A broad revert removed the Vulcan workspace instruction file.
- The repo did not have a validation check ensuring required workspace instruction files are present.

## Proposed follow-up improvements

- Add a lightweight validation check for required role workspace instruction files.
- Standardize workspace instruction naming across Hermes, Athena, Vulcan, and Koios.
- Avoid broad reverts that delete workspace state without explicitly checking required harness files.

## Candidate ADR or implementation topics

- Workspace instruction file presence validation.
- Canonical `AGENTS.md` vs `AGENT.md` naming decision for role workspaces.

## Current status

`workspaces/vulcan/AGENTS.md` was restored from git history and is being committed with this AAR.
