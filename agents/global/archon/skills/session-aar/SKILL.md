---
name: session-aar
description: |
  Use at the end of every Project Koios agent session. Also use when the user
  asks for an AAR, after-action report, retrospective, process review, lessons
  learned, or session improvement capture. Sessions with protocol failures,
  workflow friction, unclear routing, repeated corrections, tool/Graphify/Archon
  confusion, or improvement ideas should capture those lessons explicitly.
  Produces a durable process AAR for any harness role: Hermes, Athena, Vulcan,
  Koios, or delegated Codex operator.
metadata:
  agent: all
  harness_role: process-capture
  consumes:
    - session-transcript
    - changed-files
    - workflow-runs
    - user-corrections
  produces:
    - after-action-report
    - improvement-candidates
---

# Session AAR

## When to use this skill

Use this skill at every session end. Sessions with process learning should
capture it, not only task output. Trigger examples:

- "do an AAR"
- "after action report"
- "what could be improved"
- "capture process problems"
- "lessons learned"
- "store this retrospective"
- any repeated user correction of protocol or role behavior
- every Project Koios session stop or final closeout

Any agent role may use this skill. The AAR is not an ADR, handoff, completion
decision, or implementation report. It is a process observation artifact that
may later become an ADR, skill update, workflow change, or implementation task.

## Responsibility

Capture what should improve about the process. Do not merely summarize what was
built. Focus on friction, protocol misses, ambiguous ownership, tool mismatch,
handoff gaps, validation gaps, and concrete improvement candidates.

For trivial clean sessions with no durable process issue, still write a brief
AAR that records the scope, what happened, that no durable process issue was
observed, and the current status.

Do not change ADR status, route implementation, or claim architecture authority
from an AAR. If an AAR implies architecture or workflow changes, list them as
candidate follow-ups.

## Inputs

- user corrections and preferences from the session
- files changed or artifacts produced
- Archon workflow run IDs and outcomes, when relevant
- validation results and Graphify refresh behavior
- process friction, repeated mistakes, or unclear conventions

## Procedure

1. Identify the session scope in one or two sentences.
2. List the process issues, ordered by impact.
3. For each issue, state:
   - what happened
   - why it mattered
   - a concrete improvement
4. List follow-up improvements as actionable candidates.
5. State whether any follow-up should become an ADR, skill update, workflow
   update, documentation update, or implementation task.
6. Save the AAR under:

   ```text
   docs/AAR/aar.YYYYMMDD.HHMMSS_kebab-topic.md
   ```

7. After writing the AAR, run the smallest reasonable verification:
   - read back the file header and issue list
   - check `git status --short`
   - run `graphify update .` after meaningful repo file changes unless the
     user explicitly says not to or urgent handoff would be blocked

## Required AAR structure

```markdown
# AAR YYYYMMDD.HHMMSS: <topic>

## Scope

## What happened

## Process issues

### <issue>

Improvement:

## Proposed follow-up improvements

## Candidate ADR or implementation topics

## Current status
```

## Content guidance

- Prefer process observations over task-output narration.
- Include user corrections verbatim or closely paraphrased when they reveal a
  protocol expectation.
- Keep AAR claims grounded in the session artifacts and live repo state.
- Name affected skills, workflows, docs, or ADRs when practical.
- Mark AARs as non-authoritative unless promoted through the normal
  architecture or implementation lifecycle.

## Failure modes

- If no durable process issue exists, create a brief AAR that says so.
- If the session is too broad to summarize safely, create a narrow AAR focused
  on the top three process issues and list the rest as follow-up review items.
- If writing the AAR would mix secrets, local runtime state, or sensitive
  transcript content into git, redact or omit those details and note the
  redaction.
