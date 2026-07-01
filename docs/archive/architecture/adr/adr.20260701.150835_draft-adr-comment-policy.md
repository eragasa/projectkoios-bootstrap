# ADR 20260701.150835: Draft ADR comment lifecycle

## Status

historic

## Context

ADR files have a defined Status lifecycle (draft / proposed / accepted /
completed / superseded / rejected). Until now, the "draft" phase had no formal
mechanism for agents to provide feedback, raise concerns, or propose
alternatives.

During the 20260701.150224 session, an ad-hoc policy was used: agents append
comments in their own section, leave existing text untouched, and only Zeus
(via Hermes) may change the Status field. This ADR codifies that policy so it
applies consistently across all agents and sessions.

The policy must satisfy four constraints:

1. Drafts should be reviewable without risking the author's original proposal.
2. Feedback must be attributable to the agent that raised it.
3. No agent may unilaterally change the lifecycle status of a decision.
4. The comment surface must be navigable for human readers and downstream
   agents.

## Decision

1. **Append-only comments.** Any agent may add comments to a draft ADR.
   Comments are appended to the end of the file. No existing text may be
   modified, including the Status field, headings, context, decision,
   consequences, open questions, or any other pre-existing section.

2. **Structured heading tree.** Comments are placed under this exact hierarchy:

   ```
   ## Phase I:

   ### Discussion

   #### <ROLE> comments
   - [YYMMDD:HHMMSS]: <comment body>
   ```

   - `<ROLE>` is the agent role that owns the comment (e.g. VULCAN, ATHENA, HERMES,
     KOIOS). It is never the ADR author's role unless they are commenting on their
     own draft as a reviewer.
   - The timestamp uses the format `YYMMDD:HHMMSS` in the agent's local timezone.
   - If no `## Phase I:` section exists yet, the commenting agent creates it.
   - If a `## Phase I:` section exists but has no `#### <ROLE> comments`
     subsection, the commenting agent creates it.
   - Multiple agents comment independently under their own `#### <ROLE> comments`
     heading. Each agent's comments are grouped, not interleaved.

3. **Status is Zeus-only.** Only Zeus (the human user) acting through Hermes
   may change the Status line of any ADR. No agent may promote, demote, accept,
   reject, or otherwise mutate the lifecycle status of an ADR. This prevents
   unilateral review-capture and keeps the human in the decision loop.

4. **Status lifecycle.** The canonical sequence is:

   ```
   draft → proposed → accepted → completed
                                       → superseded → rejected
   ```

   - `draft`: open for agent comments, no architecture authority
   - `proposed`: comments collected, awaiting human acceptance decision
   - `accepted`: architecture decision is approved
   - `completed`: implementation is verified and merged
   - `superseded`: replaced by a later ADR
   - `rejected`: declined without replacement

   Status transitions may skip intermediate states (e.g. `draft → superseded`)
   when appropriate, but only Zeus via Hermes may execute them.

5. **This ADR is subject to its own comment rules.** This ADR codifies the
   comment lifecycle and is itself a draft. All agents (including Vulcan) may
   append comments under `#### <ROLE> comments` per the rules herein. Only Zeus
   via Hermes may promote it from draft.

## Consequences

- Draft ADRs become a durable record of agent review, not just the initial
  proposal. Feedback is preserved alongside the decision for future readers.
- Role attribution enables audit of who raised what and when.
- The append-only rule guarantees the original proposal remains inspectable
  regardless of how many agents comment.
- The Zeus-only Status rule creates a deliberate bottleneck that prevents
  unilateral promotion. This is a feature, not a bug: it ensures the human
  remains the final authority on lifecycle state.
- Future agents encountering a draft with existing comments add their own
  `#### <ROLE> comments` heading instead of interleaving. This keeps the
  doc navigable.
- ADRs that reach `accepted` or `completed` status may carry a long "Phase I"
  discussion tail. This is acceptable — the Status field is the authoritative
  lifecycle signal; the comment section is provenance.

## architecture-spec

Not separately stated in the original archive ADR.

## acceptance-criteria

Not separately stated in the original archive ADR.

## implementation-brief

Not separately stated in the original archive ADR.

## resolved-open-questions

None stated.

## non-goals

None stated.

## validation-expectations

Not separately stated in the original archive ADR.

## routing

- Owner: Athena
- Next phase: completed
- Notes: Historic archived ADR normalized to the template; original text preserved below.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None

---

## original

# ADR 20260701.150835: Draft ADR comment lifecycle

## Status

historic

## Provenance

- Origin: 20260701.150224 session (ad-hoc policy)
- From: Zeus (human user)
- Acting-As: Zeus
- Proposed-By: Vulcan, under direction of Zeus
- Delegated-Operator: opencode (Vulcan runtime)

## Context

ADR files have a defined Status lifecycle (draft / proposed / accepted /
completed / superseded / rejected). Until now, the "draft" phase had no formal
mechanism for agents to provide feedback, raise concerns, or propose
alternatives.

During the 20260701.150224 session, an ad-hoc policy was used: agents append
comments in their own section, leave existing text untouched, and only Zeus
(via Hermes) may change the Status field. This ADR codifies that policy so it
applies consistently across all agents and sessions.

The policy must satisfy four constraints:

1. Drafts should be reviewable without risking the author's original proposal.
2. Feedback must be attributable to the agent that raised it.
3. No agent may unilaterally change the lifecycle status of a decision.
4. The comment surface must be navigable for human readers and downstream
   agents.

## Decision

1. **Append-only comments.** Any agent may add comments to a draft ADR.
   Comments are appended to the end of the file. No existing text may be
   modified, including the Status field, headings, context, decision,
   consequences, open questions, or any other pre-existing section.

2. **Structured heading tree.** Comments are placed under this exact hierarchy:

   ```
   ## Phase I:

   ### Discussion

   #### <ROLE> comments
   - [YYMMDD:HHMMSS]: <comment body>
   ```

   - `<ROLE>` is the agent role that owns the comment (e.g. VULCAN, ATHENA, HERMES,
     KOIOS). It is never the ADR author's role unless they are commenting on their
     own draft as a reviewer.
   - The timestamp uses the format `YYMMDD:HHMMSS` in the agent's local timezone.
   - If no `## Phase I:` section exists yet, the commenting agent creates it.
   - If a `## Phase I:` section exists but has no `#### <ROLE> comments`
     subsection, the commenting agent creates it.
   - Multiple agents comment independently under their own `#### <ROLE> comments`
     heading. Each agent's comments are grouped, not interleaved.

3. **Status is Zeus-only.** Only Zeus (the human user) acting through Hermes
   may change the Status line of any ADR. No agent may promote, demote, accept,
   reject, or otherwise mutate the lifecycle status of an ADR. This prevents
   unilateral review-capture and keeps the human in the decision loop.

4. **Status lifecycle.** The canonical sequence is:

   ```
   draft → proposed → accepted → completed
                                       → superseded → rejected
   ```

   - `draft`: open for agent comments, no architecture authority
   - `proposed`: comments collected, awaiting human acceptance decision
   - `accepted`: architecture decision is approved
   - `completed`: implementation is verified and merged
   - `superseded`: replaced by a later ADR
   - `rejected`: declined without replacement

   Status transitions may skip intermediate states (e.g. `draft → superseded`)
   when appropriate, but only Zeus via Hermes may execute them.

5. **This ADR is subject to its own comment rules.** This ADR codifies the
   comment lifecycle and is itself a draft. All agents (including Vulcan) may
   append comments under `#### <ROLE> comments` per the rules herein. Only Zeus
   via Hermes may promote it from draft.

## Consequences

- Draft ADRs become a durable record of agent review, not just the initial
  proposal. Feedback is preserved alongside the decision for future readers.
- Role attribution enables audit of who raised what and when.
- The append-only rule guarantees the original proposal remains inspectable
  regardless of how many agents comment.
- The Zeus-only Status rule creates a deliberate bottleneck that prevents
  unilateral promotion. This is a feature, not a bug: it ensures the human
  remains the final authority on lifecycle state.
- Future agents encountering a draft with existing comments add their own
  `#### <ROLE> comments` heading instead of interleaving. This keeps the
  doc navigable.
- ADRs that reach `accepted` or `completed` status may carry a long "Phase I"
  discussion tail. This is acceptable — the Status field is the authoritative
  lifecycle signal; the comment section is provenance.
