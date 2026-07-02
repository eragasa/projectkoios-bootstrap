# AAR — Hermes startup launcher

## Scope
Hermes startup autoprocess launcher and documentation wiring.

## What happened
Created `scripts/hermes-startup`, documented it in the repo README and scripts README, and updated Hermes workspace state files so the next restart has a stable startup surface.

## Process issues
The launcher needed to be documented in both the scripts index and the top-level README to be easy to find after a restart.

## Proposed follow-up improvements
Consider wiring the launcher into the workspace instructions so it is the default first step for Hermes restarts.

## Candidate ADR or implementation topics
Workspace startup launcher binding.

## Current status
No blocking issue observed.
