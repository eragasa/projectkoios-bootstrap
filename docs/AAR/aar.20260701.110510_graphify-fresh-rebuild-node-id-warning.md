# AAR 20260701.110510: Fresh graphify rebuild and pre-#1504 node-ID warning

## Scope

projectkoios-bootstrap repo, master branch, clean tree.
Single-task session: rebuild the graphify graph to retire the pre-#1504
node-ID scheme warning flagged at session start.

## What happened

- Session-start state check: clean tree, no draft ADRs, no active Archon runs.
- The only outstanding flag was graphify's note that the graph used the
  pre-#1504 node-ID scheme and recommended `graphify extract --force`.
- Ran `graphify update --force .` first; it reported "no topology changes"
  and left outputs untouched, so the warning was not cleared.
- Backed up `graphify-out/`, deleted it, and ran `graphify update .` for a
  fresh AST-only rebuild: 3887 nodes, 4272 edges, 409 communities.
- The pre-#1504 warning **still** appears after a clean rebuild.
- Investigated: installed graphify is 0.9.2. The `extract` subcommand is a
  full semantic (LLM) extraction, not an AST-only node-ID migration. The
  warning's hint ("rebuild with `graphify extract --force`") cannot be
  satisfied by this graphify version for an AST-only fix.

## Process issues

1. **Misleading warning hint.** The graphify warning recommends
   `graphify extract --force` to fix the node-ID scheme, but in 0.9.2
   `extract` is a full LLM semantic run, not a node-ID migration. An
   operator following the hint literally would either (a) trigger an
   unintended LLM pass or (b) assume the graph is unfixable. The hint
   should either be gated on a graphify version that supports
   path-qualified IDs, or the warning should distinguish "stale graph"
   from "graphify version too old".
2. **`update --force` does not rewrite node IDs.** Even with a deleted
   `graphify-out/`, the freshly built graph still carries the pre-#1504
   scheme. The node-ID scheme is a property of the graphify build, not
   the graph file, so no AST-only rebuild can retire it on 0.9.2.
3. **AGENTS.md wording vs reality.** AGENTS.md directs harnesses to run
   `graphify update .` at session end "so the next session starts from
   current indexed state". That is correct and useful, but it does not
   address the node-ID scheme warning, which is often the most visible
   graphify flag at session start. The two should not be conflated.

## Proposed follow-up improvements

- Track upstream graphify for a release that emits path-qualified
  node IDs (#1504) and upgrade when available; only then will the
  warning clear via a normal `update`.
- Consider downgrading the pre-#1504 warning to a "discovery only"
  note in AGENTS.md guidance so harnesses do not treat it as a blocker
  or spend a session trying to "fix" a graphify-version limitation.
- Optionally add a one-line `graphify --version` check to the
  session-start protocol so the node-ID warning is immediately
  attributed to the installed version rather than the graph state.

## Candidate ADR or implementation topics

- ADR: "Treat graphify node-ID scheme warnings as graphify-version
  signals, not graph-staleness signals." (Small, but would prevent
  repeated investigative sessions like this one.)

## Current status

- Working tree: clean (graphify-out is gitignored; no tracked changes).
- Graph: freshly rebuilt, 3887 nodes / 4272 edges / 409 communities,
  AST-only, current with source.
- Pre-#1504 warning: still present; attributable to graphify 0.9.2,
  not to a stale graph. Treat graph as discovery only per AGENTS.md.
- No commits made; no code changes outside graphify-out.
