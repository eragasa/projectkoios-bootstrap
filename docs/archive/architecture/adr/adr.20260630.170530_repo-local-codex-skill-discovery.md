# ADR 20260630.170530: Repo-local Codex skill discovery

## Status

historic

## Context

Origin: archon
Created: 2026-06-30 17:05
From: Athena
To: Vulcan
Scope: projectkoios-bootstrap
Repository: /Users/eugene/repos/projectkoios-bootstrap

This specification responds to the user request for a repo-local Project Koios
Codex skill discovery layer. It is scoped only to `projectkoios-bootstrap`.
It does not define product/domain architecture for the mothership vault.

## Decision

Codex must be able to discover Project Koios operating skills directly from
the repository when a session starts in `projectkoios-bootstrap` or a child
directory. Codex discovers repo-local skills from `.agents/skills` while
walking from the current working directory up to the repository root. The
repo therefore needs a committed `.agents/skills` discovery layer that exposes
the relevant Project Koios skills from that location.

The canonical source of reusable harness skill material remains under
`agents/global/<harness>/skills/...`. The `.agents/skills` tree is the
Codex-native discovery surface, not a replacement source hierarchy. It should
materialize curated Project Koios skills by relative symlink where the source
skill already exists and by a small committed wrapper skill only where a
Codex-specific entrypoint is needed.

The discovery layer must expose one primary Project Koios skill:

- `.agents/skills/projectkoios/SKILL.md`

This skill is the Codex-facing repo entrypoint. It should explain the
Project Koios bootstrap scope, role model, routing boundary, and which
repo-local role skills to use. It must explicitly preserve the role/runtime
separation:

- Hermes is the `Hermes` meta-harness role for orchestration and operations.
- Athena is the `archon` spec/architecture role.
- Vulcan is the `opencode` implementation and validation role.
- Koios is the `goose` knowledge/provenance role.
- Codex may act as a delegated access/operator layer, but Codex does not
  become `Hermes`, `archon`, `opencode`, or `goose`.

The discovery layer should also expose related role skills when they are useful
to Codex in this repo:

- Athena/spec skills that help Codex produce or relay architecture handoffs.
- Hermes/run-control skills that help Codex inspect or manage Archon workflow
  runs when explicitly asked.
- Koios/knowledge skills that help Codex route provenance or knowledge-capture
  work to the right artifact boundary.

The existing `.agents/skills/archon` and `.agents/skills/manage-run` symlinks
already follow the intended pattern by pointing to `agents/global/archon/skills`.
Vulcan should keep that pattern, repair it if needed, and extend it with the
new Project Koios entrypoint and any selected role skill links.

Preferred materialization strategy:

1. Use relative symlinks from `.agents/skills/<skill-name>` to
   `agents/global/<harness>/skills/<skill-name>` when the skill is already
   canonical and Codex can consume it as-is.
2. Add a small wrapper skill under `.agents/skills/projectkoios/SKILL.md` if no
   canonical source currently exists for the repo-level Project Koios entrypoint.
3. Avoid duplicating long skill bodies between `.agents/skills` and
   `agents/global/...`. If a wrapper must repeat key routing facts, keep it
   concise and point to `AGENTS.md`, `docs/meta-harness.md`, and the relevant
   role skills as the authoritative sources.

## Consequences

This decision makes `.agents/skills` the Codex-native repo discovery surface
without moving canonical harness skill sources out of `agents/global/...`.
Acceptance criteria, implementation guidance, validation expectations, and
return routing are below.

## architecture-spec

Not separately stated in the original archive ADR.

## acceptance-criteria

Vulcan's implementation is complete when:

1. `.agents/skills/projectkoios/SKILL.md` exists from the repository root and
   is discoverable by Codex as a repo-local skill.

2. The `projectkoios` skill has valid skill frontmatter with a clear
   `name` and `description`, and its body states the repo scope, role model,
   routing boundaries, and non-authority of Codex as a delegated operator.

3. Existing discoverable skills under `.agents/skills` are not broken:
   `.agents/skills/archon/SKILL.md` and
   `.agents/skills/manage-run/SKILL.md` resolve successfully.

4. If additional role skills are exposed, they are exposed through
   `.agents/skills` using relative symlinks or concise wrapper skills and do
   not create duplicate, divergent canonical skill copies.

5. The implementation preserves `agents/global/<harness>/skills/...` as the
   canonical source location for reusable harness skills.

6. The implementation does not add machine-local state, secrets, session files,
   generated caches, or vault content.

7. The implementation does not alter Archon workflow definitions, Python CLI
   behavior, bootstrap install behavior, or local harness configuration unless
   Vulcan returns a deviation report explaining why the spec cannot be met
   without broadening scope.

8. The implementation includes enough inline skill routing guidance that a
   future Codex session started inside this repo can find the Project Koios
   entrypoint without relying on copied user-level skills.

## implementation-brief

Implement only the repo-local Codex discovery layer and the minimal skill text
needed for it.

Recommended file targets:

- `.agents/skills/projectkoios/SKILL.md`
- `.agents/skills/archon` if the existing symlink needs repair
- `.agents/skills/manage-run` if the existing symlink needs repair
- optionally `.agents/skills/<role-skill>` symlinks for selected existing
  Athena, Hermes, or Koios skills

Recommended source references:

- `AGENTS.md`
- `docs/meta-harness.md`
- `agents/global/archon/skills/spec-agent-scope-review/SKILL.md`
- `agents/global/archon/skills/spec-agent-acceptance-criteria/SKILL.md`
- `agents/global/archon/skills/manage-run/SKILL.md`
- `agents/global/pi/skills/meta-harness-task-routing/SKILL.md`
- `agents/global/goose/skills/knowledge-agent-provenance-note/SKILL.md`

The `projectkoios` skill should be a small operational entrypoint, not a full
copy of `AGENTS.md`. It should tell Codex when to:

- use Athena-style spec handoffs for architecture and planning;
- use Vulcan handoffs for implementation and validation;
- use Hermes routing/run-control when asked to inspect, approve, reject,
  resume, or cancel Archon runs;
- route durable knowledge/provenance work to Koios/goose boundaries;
- keep local secrets and machine-specific runtime state out of git.

If Vulcan chooses symlinks, use repository-relative symlinks that remain valid
from the repository root. If symlinks are unsuitable on the target platform,
use concise wrapper skills in `.agents/skills` and document that choice in the
implementation report.

Do not modify bootstrap install commands in this slice. The immediate goal is
Codex repo-local discovery from `.agents/skills`, not installation into user,
admin, or system skill locations.

## resolved-open-questions

1. The correct Codex discovery location for this repo is `.agents/skills` at
   the repository root, because Codex walks from the current directory up to
   the repo root looking for repo-local skills.

2. The primary required new skill is `projectkoios`, exposed at
   `.agents/skills/projectkoios/SKILL.md`.

3. Existing harness skill source remains under `agents/global/...`; the
   `.agents/skills` tree is the Codex discovery layer.

4. Relative symlinks are preferred for existing canonical skills because they
   avoid divergent copies. Wrapper skills are acceptable only for the new
   Project Koios Codex entrypoint or for platform constraints.

5. Related role skills are appropriate only when they help Codex route work
   according to the meta-harness boundary. This does not require exposing every
   harness skill.

6. This change does not make Codex a new Project Koios harness role. It gives
   Codex local discovery of instructions for acting as a delegated operator.

## non-goals

- Do not redesign the meta-harness role model.
- Do not move canonical harness skills out of `agents/global/...`.
- Do not package or publish Project Koios skills to user, admin, or system
  skill locations.
- Do not change Archon workflow YAML, opencode configuration, Goose runtime
  state, or Python bootstrap behavior.
- Do not create product/domain architecture in this repo.
- Do not add machine-local secrets, auth files, sessions, generated caches, or
  vault state.
- Do not commit, push, or open a PR as part of this task.

## validation-expectations

Vulcan should run the smallest structural validation that proves discovery is
wired correctly:

```bash
test -f .agents/skills/projectkoios/SKILL.md
test -f .agents/skills/archon/SKILL.md
test -f .agents/skills/manage-run/SKILL.md
find -L .agents/skills -maxdepth 2 -name SKILL.md -print
find .agents/skills -xtype l -print
git status --short
```

Expected results:

- `projectkoios`, `archon`, and `manage-run` each resolve to a `SKILL.md`.
- `find -L` lists the discoverable skill files.
- `find .agents/skills -xtype l -print` prints nothing, meaning no broken
  symlinks exist.
- `git status --short` shows only intentional repo-local discovery/skill
  changes and no local secrets or runtime state.

If Vulcan adds or edits markdown skill files, it should also visually inspect
the frontmatter and confirm each skill has a concise trigger-oriented
description.

## routing

After implementation, Vulcan must return to Hermes with:

- an `implementation-report` listing changed files and the chosen
  materialization strategy;
- `test-results` containing the validation commands and outputs;
- a `deviation-report` if it had to broaden scope beyond `.agents/skills` or
  minimal skill text;
- any recommendation for Athena only if the implementation reveals a durable
  architecture question not resolved here.

Hermes should then decide whether the implementation is complete, whether a
knowledge-capture pass should be routed to Koios, and whether any follow-up ADR
or bootstrap installer change is needed.

- Notes: Historic archived ADR normalized to the template; original text preserved below.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None

---

## original

# ADR 20260630.170530: Repo-local Codex skill discovery

## Status

historic

## Context

Origin: archon
Created: 2026-06-30 17:05
From: Athena
To: Vulcan
Scope: projectkoios-bootstrap
Repository: /Users/eugene/repos/projectkoios-bootstrap

This specification responds to the user request for a repo-local Project Koios
Codex skill discovery layer. It is scoped only to `projectkoios-bootstrap`.
It does not define product/domain architecture for the mothership vault.

## Decision

Codex must be able to discover Project Koios operating skills directly from
the repository when a session starts in `projectkoios-bootstrap` or a child
directory. Codex discovers repo-local skills from `.agents/skills` while
walking from the current working directory up to the repository root. The
repo therefore needs a committed `.agents/skills` discovery layer that exposes
the relevant Project Koios skills from that location.

The canonical source of reusable harness skill material remains under
`agents/global/<harness>/skills/...`. The `.agents/skills` tree is the
Codex-native discovery surface, not a replacement source hierarchy. It should
materialize curated Project Koios skills by relative symlink where the source
skill already exists and by a small committed wrapper skill only where a
Codex-specific entrypoint is needed.

The discovery layer must expose one primary Project Koios skill:

- `.agents/skills/projectkoios/SKILL.md`

This skill is the Codex-facing repo entrypoint. It should explain the
Project Koios bootstrap scope, role model, routing boundary, and which
repo-local role skills to use. It must explicitly preserve the role/runtime
separation:

- Hermes is the `Hermes` meta-harness role for orchestration and operations.
- Athena is the `archon` spec/architecture role.
- Vulcan is the `opencode` implementation and validation role.
- Koios is the `goose` knowledge/provenance role.
- Codex may act as a delegated access/operator layer, but Codex does not
  become `Hermes`, `archon`, `opencode`, or `goose`.

The discovery layer should also expose related role skills when they are useful
to Codex in this repo:

- Athena/spec skills that help Codex produce or relay architecture handoffs.
- Hermes/run-control skills that help Codex inspect or manage Archon workflow
  runs when explicitly asked.
- Koios/knowledge skills that help Codex route provenance or knowledge-capture
  work to the right artifact boundary.

The existing `.agents/skills/archon` and `.agents/skills/manage-run` symlinks
already follow the intended pattern by pointing to `agents/global/archon/skills`.
Vulcan should keep that pattern, repair it if needed, and extend it with the
new Project Koios entrypoint and any selected role skill links.

Preferred materialization strategy:

1. Use relative symlinks from `.agents/skills/<skill-name>` to
   `agents/global/<harness>/skills/<skill-name>` when the skill is already
   canonical and Codex can consume it as-is.
2. Add a small wrapper skill under `.agents/skills/projectkoios/SKILL.md` if no
   canonical source currently exists for the repo-level Project Koios entrypoint.
3. Avoid duplicating long skill bodies between `.agents/skills` and
   `agents/global/...`. If a wrapper must repeat key routing facts, keep it
   concise and point to `AGENTS.md`, `docs/meta-harness.md`, and the relevant
   role skills as the authoritative sources.

## Consequences

This decision makes `.agents/skills` the Codex-native repo discovery surface
without moving canonical harness skill sources out of `agents/global/...`.
Acceptance criteria, implementation guidance, validation expectations, and
return routing are below.

## Acceptance-Criteria

Vulcan's implementation is complete when:

1. `.agents/skills/projectkoios/SKILL.md` exists from the repository root and
   is discoverable by Codex as a repo-local skill.

2. The `projectkoios` skill has valid skill frontmatter with a clear
   `name` and `description`, and its body states the repo scope, role model,
   routing boundaries, and non-authority of Codex as a delegated operator.

3. Existing discoverable skills under `.agents/skills` are not broken:
   `.agents/skills/archon/SKILL.md` and
   `.agents/skills/manage-run/SKILL.md` resolve successfully.

4. If additional role skills are exposed, they are exposed through
   `.agents/skills` using relative symlinks or concise wrapper skills and do
   not create duplicate, divergent canonical skill copies.

5. The implementation preserves `agents/global/<harness>/skills/...` as the
   canonical source location for reusable harness skills.

6. The implementation does not add machine-local state, secrets, session files,
   generated caches, or vault content.

7. The implementation does not alter Archon workflow definitions, Python CLI
   behavior, bootstrap install behavior, or local harness configuration unless
   Vulcan returns a deviation report explaining why the spec cannot be met
   without broadening scope.

8. The implementation includes enough inline skill routing guidance that a
   future Codex session started inside this repo can find the Project Koios
   entrypoint without relying on copied user-level skills.

## Implementation-Brief

Implement only the repo-local Codex discovery layer and the minimal skill text
needed for it.

Recommended file targets:

- `.agents/skills/projectkoios/SKILL.md`
- `.agents/skills/archon` if the existing symlink needs repair
- `.agents/skills/manage-run` if the existing symlink needs repair
- optionally `.agents/skills/<role-skill>` symlinks for selected existing
  Athena, Hermes, or Koios skills

Recommended source references:

- `AGENTS.md`
- `docs/meta-harness.md`
- `agents/global/archon/skills/spec-agent-scope-review/SKILL.md`
- `agents/global/archon/skills/spec-agent-acceptance-criteria/SKILL.md`
- `agents/global/archon/skills/manage-run/SKILL.md`
- `agents/global/pi/skills/meta-harness-task-routing/SKILL.md`
- `agents/global/goose/skills/knowledge-agent-provenance-note/SKILL.md`

The `projectkoios` skill should be a small operational entrypoint, not a full
copy of `AGENTS.md`. It should tell Codex when to:

- use Athena-style spec handoffs for architecture and planning;
- use Vulcan handoffs for implementation and validation;
- use Hermes routing/run-control when asked to inspect, approve, reject,
  resume, or cancel Archon runs;
- route durable knowledge/provenance work to Koios/goose boundaries;
- keep local secrets and machine-specific runtime state out of git.

If Vulcan chooses symlinks, use repository-relative symlinks that remain valid
from the repository root. If symlinks are unsuitable on the target platform,
use concise wrapper skills in `.agents/skills` and document that choice in the
implementation report.

Do not modify bootstrap install commands in this slice. The immediate goal is
Codex repo-local discovery from `.agents/skills`, not installation into user,
admin, or system skill locations.

## Resolved Open Questions

1. The correct Codex discovery location for this repo is `.agents/skills` at
   the repository root, because Codex walks from the current directory up to
   the repo root looking for repo-local skills.

2. The primary required new skill is `projectkoios`, exposed at
   `.agents/skills/projectkoios/SKILL.md`.

3. Existing harness skill source remains under `agents/global/...`; the
   `.agents/skills` tree is the Codex discovery layer.

4. Relative symlinks are preferred for existing canonical skills because they
   avoid divergent copies. Wrapper skills are acceptable only for the new
   Project Koios Codex entrypoint or for platform constraints.

5. Related role skills are appropriate only when they help Codex route work
   according to the meta-harness boundary. This does not require exposing every
   harness skill.

6. This change does not make Codex a new Project Koios harness role. It gives
   Codex local discovery of instructions for acting as a delegated operator.

## Non-Goals

- Do not redesign the meta-harness role model.
- Do not move canonical harness skills out of `agents/global/...`.
- Do not package or publish Project Koios skills to user, admin, or system
  skill locations.
- Do not change Archon workflow YAML, opencode configuration, Goose runtime
  state, or Python bootstrap behavior.
- Do not create product/domain architecture in this repo.
- Do not add machine-local secrets, auth files, sessions, generated caches, or
  vault state.
- Do not commit, push, or open a PR as part of this task.

## Validation Expectations

Vulcan should run the smallest structural validation that proves discovery is
wired correctly:

```bash
test -f .agents/skills/projectkoios/SKILL.md
test -f .agents/skills/archon/SKILL.md
test -f .agents/skills/manage-run/SKILL.md
find -L .agents/skills -maxdepth 2 -name SKILL.md -print
find .agents/skills -xtype l -print
git status --short
```

Expected results:

- `projectkoios`, `archon`, and `manage-run` each resolve to a `SKILL.md`.
- `find -L` lists the discoverable skill files.
- `find .agents/skills -xtype l -print` prints nothing, meaning no broken
  symlinks exist.
- `git status --short` shows only intentional repo-local discovery/skill
  changes and no local secrets or runtime state.

If Vulcan adds or edits markdown skill files, it should also visually inspect
the frontmatter and confirm each skill has a concise trigger-oriented
description.

## Handoff Routing

After implementation, Vulcan must return to Hermes with:

- an `implementation-report` listing changed files and the chosen
  materialization strategy;
- `test-results` containing the validation commands and outputs;
- a `deviation-report` if it had to broaden scope beyond `.agents/skills` or
  minimal skill text;
- any recommendation for Athena only if the implementation reveals a durable
  architecture question not resolved here.

Hermes should then decide whether the implementation is complete, whether a
knowledge-capture pass should be routed to Koios, and whether any follow-up ADR
or bootstrap installer change is needed.
