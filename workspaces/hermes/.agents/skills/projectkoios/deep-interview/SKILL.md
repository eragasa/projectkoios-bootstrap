---
name: deep-interview
description: |
  Use when: you need a deep, recursive interview to define a problem, compare competing interests, and refine the task over multiple turns.
  Triggers: "interview me", "ask me questions", "define the problem", "assessment framework", "competing interests", "question stack", "recursive interview".
  Capability: Maintains an interview note in the Hermes workspace, proposes 3-5 assessment axes, asks one question at a time with four courses of action and recommendation, and updates the question stack as new information changes the problem.
  NOT for: Archon DAG workflows, automatic architecture decisions, implementation, or one-shot questionnaires.
  Bound to ADRs: adr.skill-register-and-adr-binding-policy.draft.md, adr.canonical-workspace-state-next-action-protocol.draft.md, adr.comment-scope-and-control-boundary-review-rule.draft.md.
---
# Deep interview

## Purpose

Use this skill to turn an underspecified problem into a stable, testable decision
package through a recursive interview loop.

The skill is designed for repeated use. It should:
1. define the problem first
2. propose objective variables second
3. choose a mechanism for selecting/scoring those variables third
4. collect and reorder questions as understanding changes
5. preserve a durable interview file in the Hermes workspace
6. keep the current problem statement visible and revisable

## Operating model

This is not a DAG workflow. Recursion is modeled as an iterative stack:
1. capture the problem statement in plain language
2. if the problem is abstract, define scenario cards before taxonomy
3. propose objective variables for the chosen scenario(s)
4. ask the user to choose the scoring/selection mechanism
5. create a numbered question stack
6. ask the top question
7. revise the problem statement when the answer changes the framing
8. prepend new questions when needed
9. repeat until the stack is empty or the user says stop

## Workspace artifact

Create or update one interview file in the Hermes workspace:

- `workspaces/hermes/interviews/interview.<timestamp>_<slug>.md`

The file should contain at least this numbered flow:
1. problem context
2. objective variables
3. choosing mechanism
4. question stack
5. current top question
6. answered questions
7. revised understanding
8. open questions
9. next action

## Assessment framework

After the problem context is defined, propose 3-5 objective variables, not binary
trade-off pairs.

Each axis should be a single measurable dimension that can be placed on a Pareto
surface, and each axis must say whether it is being minimized or maximized.
Examples:
- YAGNI / unnecessary scope (minimize)
- separation of concerns (maximize)
- Petri-net workflow compatibility (maximize)
- automation potential (maximize)
- cost observability (maximize)

The user may also split axes into primary and deprioritized tiers when the
problem has a clear core and secondary concerns.
- revision cost / churn (minimize)
- reuse / generalization value (maximize)

For each axis, ask the user to keep, drop, or merge it.
Then propose a 0-10 rubric with the objective direction stated explicitly.
After that, propose a choosing mechanism such as:
1. scalar score
2. score plus notes
3. score range
4. ranked comparison

Do not hide the actual objective inside a trade-off label. The axis must be the
thing being optimized or minimized.

## Question design

If the problem is not tied to a specific concrete case, start with scenario
cards. Each scenario card should describe a real-seeming case the control surface
must handle. Do not ask abstract taxonomy questions before the scenario is
anchored.

When multiple questions target the same domain, combine them into one scenario or
one question unless separating them materially changes the answer.

Every question must include four courses of action.
For each course of action, provide:
- a short label
- an analysis of the option
- key trade-offs or risks
- when it is the right choice

Then:
- recommend one course of action
- explain why it is the best default
- record the user's decision if they override it
- write the selected mechanism into the interview file before continuing

## Recursive update rule

Whenever the answer changes the problem framing:
- update the top-level problem statement in the interview file
- adjust the assessment axes if necessary
- prepend any new questions to the top of the question stack
- merge questions that belong to the same domain before adding new ones
- prioritize questions by domain and leverage
- keep older questions and answers as provenance
- do not silently discard prior context

## Interview loop format

For each turn, answer with:
1. current understanding
2. the concrete scenario, if one is active
3. the problem statement, if it changed
4. the objective variable(s), if they changed
5. the question
6. four courses of action with analysis
7. recommendation
8. what answer will change next

If the current top question is answered, replace it with the next question.
If the answer reveals a missing prerequisite, add that prerequisite to the top of
stack before continuing.

## Boundaries

- Do not use Archon for the recursion loop; Archon DAGs are the wrong shape.
- Do not turn the interview into implementation work.
- Do not write a final decision before the assessment framework is agreed.
- Do not lose provenance when the understanding changes.
- Do not collapse multiple unresolved questions into one vague prompt.

## Deliverable shape

The skill should end with a clean decision summary:
- final problem statement
- agreed assessment axes
- 0-10 rubric per axis
- ordered question log
- remaining unknowns
- recommended next action
- if relevant, a control-surface matrix that maps surfaces to review modes
- a prioritized question queue that merges same-domain questions before recursion expands
- a debt triage rule for combine/split/promote
- a human override rule for prioritization and promotion
- a weighted rubric for leverage, effort, and structural importance
- a routing rule for high-cost/high-payoff items into long-term control-surface change or ADR promotion
- a promotion rule from control-surface change to ADR candidate
- a policy rule that lets policy-surface changes update long-term goals and priorities
