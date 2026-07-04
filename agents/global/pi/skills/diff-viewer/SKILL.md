---
name: diff-viewer
adr_binding:
  - docs/adr/adr.unified-diff-review-surface.draft.md
  - docs/adr/adr.adversarial-two-plane-gate.draft.md
description: |
  Show literal unified diffs for file review before commit or approval.
  Bound to ADRs: adr.unified-diff-review-surface.draft.md, adr.adversarial-two-plane-gate.draft.md.
metadata:
  agent: pi
  harness_role: arbiter
  consumes:
    - file-change
    - git-diff
  produces:
    - review-view
    - review-decision
---
## When to use this skill

When a user needs to inspect the exact file-level change before approving a draft, status change, or commit.

## Agent responsibility

Hermes owns review gating. This skill must show the literal diff, not a paraphrase, and must preserve file path and line context.

## Inputs

- `file-change` — the proposed edit or changed file path
- `git-diff` — the literal diff output for the current working tree or a selected file

## Procedure

1. Render the literal unified diff for the selected file(s).
2. Keep file names, hunk headers, and surrounding context visible.
3. If the diff is too large, split it into reviewable chunks without summarizing away the actual diff text.
4. Surface the diff alongside the current review question or approval gate.
5. If the user requests a change, refresh the diff and repeat.

## Output artifacts

- `review-view` — literal diff view for the selected file(s)
- `review-decision` — approve, reject, or revise the proposed change

## Failure modes

- Diff is summarized instead of shown literally — fail and re-render
- File path or hunk context is missing — fail and re-render
- Change is too large to inspect at once — chunk without collapsing the actual diff text
