# AAR: New-session ATHENA defaulting

## Scope
Athena workspace role selection in new sessions.

## What happened
A new session started in the Athena workspace was initially treated as HERMES. The root identity-resolution rules relied too heavily on generic fallback logic and did not explicitly prefer the workspace identity.

## Process issues
- Workspace-local default identity was implicit instead of explicit.
- The fallback path could override the expected ATHENA role during a blank session start.

## Proposed follow-up improvements
- Keep workspace-path identity defaults explicit in the root bootstrap rules.
- Mirror the same rule in the Athena workspace AGENT file so the expectation is visible near the workspace itself.
- Consider adding a startup check that reports the inferred workspace identity before any role-owned output.

## Candidate ADR or implementation topics
- Role inference precedence for workspace-bound sessions
- Startup diagnostics for harness identity selection

## Current status
Fixed with minimal doc updates in `AGENTS.md` and `workspaces/athena/AGENTS.md`; graphify updated. No code changes were required.
