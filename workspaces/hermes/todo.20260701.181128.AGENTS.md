# TODO 20260701.181128: AGENTS.md precision pass

## Scope

Identify vague language in `AGENTS.md` that should be tightened before any rewrite.

## Vague language candidates

1. `Use the identity assigned to your harness when speaking, writing comments, or producing artifacts.`
   - Vague point: what counts as a `comment`, `artifact`, or `speaking` boundary in mixed/handoff sessions.

2. `If delegated access relays work for a harness, preserve the harness identity and record delegation only as provenance when needed.`
   - Vague point: `when needed` is subjective; unclear when provenance is mandatory vs optional.

3. `determine the represented harness before speaking or choosing a session protocol.`
   - Vague point: `determine` does not say what evidence is sufficient or what to do if evidence conflicts.

4. `If no role can be inferred safely, ask a short clarification question...`
   - Vague point: `safely` is undefined; unclear which failure modes require escalation vs clarification.

5. `All existing ADRs are paused except ADRs that directly govern...`
   - Vague point: `directly govern` is broad and could be interpreted inconsistently.

6. `Agents may append concerns, objections, and recommendations to relevant ADRs.`
   - Vague point: `relevant` is subjective; needs a rule for relevance.

7. `The consolidation output is a new consolidated ADR proposal.`
   - Vague point: unclear who may create it, where it lives, and what status it has on creation.

8. `At session start, agents should report not only pending work, but the highest-leverage next state to move toward.`
   - Vague point: `highest-leverage` is not measurable; likely needs a selection rule.

9. `If the tree is dirty, stabilize or explain the working tree before starting new work.`
   - Vague point: `stabilize` and `explain` are broad actions; unclear acceptable outputs.

10. `if files changed, run the smallest relevant validation you can justify`
    - Vague point: `smallest`, `relevant`, and `justify` are all subjective and invite inconsistent execution.

11. `write a process AAR... even for trivial clean sessions`
    - Vague point: `trivial` and `clean` need concrete thresholds.

12. `Use Archon workflows in the foreground by default. Use detached/background... only when explicitly needed`
    - Vague point: `explicitly needed` lacks a decision rule.

## Next step

Convert these into exact replacement candidates before editing `AGENTS.md`.
