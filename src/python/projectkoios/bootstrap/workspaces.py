from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from projectkoios.bootstrap.models import REPO_ROOT

CANONICAL_WORKSPACES: tuple[str, ...] = ("hermes", "athena", "vulcan", "koios")


@dataclass(frozen=True, slots=True)
class WorkspaceTemplate:
    agent: str
    title: str
    role_summary: str
    instructions: tuple[str, ...]

    def render(self) -> str:
        lines = [
            f"# {self.title}",
            "",
            self.role_summary,
            "",
            "## Instructions",
        ]
        lines.extend(f"- {line}" for line in self.instructions)
        lines.extend(
            [
                "",
                "## Local workspace files",
                "- state.md",
                "- active.md",
                "- inbox/",
                "- outbox/",
                "- sessions/",
                "- handoffs/incoming/",
                "- handoffs/outgoing/",
                "- decisions/",
                "",
                "## Mail system",
                "- Read `inbox/` first for new work and replies.",
                "- Write outgoing notes to `outbox/`.",
                "- Hermes delivers mail by moving or copying items from outboxes to the next workspace inbox.",
                "- Keep mail notes short, explicit, and provenance-friendly.",
                "",
                "## Canonical references",
                "- docs/agent-charter.md",
                "- docs/workspaces.md",
                "- docs/architecture.00.md",
            ]
        )
        return "\n".join(lines).rstrip() + "\n"


TEMPLATES: dict[str, WorkspaceTemplate] = {
    "hermes": WorkspaceTemplate(
        agent="hermes",
        title="Hermes workspace",
        role_summary=(
            "Hermes is the router/operator workspace. It owns routing, repo-state\n"
            "inspection, and handoff coordination."
        ),
        instructions=(
            "At the start of every Hermes session, run `./scripts/hermes-startup new` to create the session marker, then resume from state.md, active.md, the newest timestamped sessions note, inbox, and outbox.",
            "Read inbox first; Hermes delivers mail from workspaces outboxes.",
            "Only Hermes may edit architecture notes, and only with explicit Zeus permission.",
            "Keep this workspace focused on current repo, focus, blockers, and next action.",
        ),
    ),
    "athena": WorkspaceTemplate(
        agent="athena",
        title="Athena workspace",
        role_summary=(
            "Athena is the spec workspace. It owns bounded architecture decisions,\n"
            "ADR drafts, and acceptance criteria."
        ),
        instructions=(
            "Keep scope bounded to one repo or one decision slice at a time.",
            "Read inbox first; send outgoing notes to outbox for Hermes delivery.",
            "Do not implement code from this workspace.",
            "Write architecture notes only when explicitly directed through Hermes.",
        ),
    ),
    "vulcan": WorkspaceTemplate(
        agent="vulcan",
        title="Vulcan workspace",
        role_summary=(
            "Vulcan is the implementation workspace. It owns code changes, tests,\n"
            "and validation output."
        ),
        instructions=(
            "Read the plan or ADR before making changes.",
            "Read inbox first; put implementation replies in outbox.",
            "Keep implementation and validation artifacts together.",
            "Do not edit architecture notes from this workspace.",
        ),
    ),
    "koios": WorkspaceTemplate(
        agent="koios",
        title="Koios workspace",
        role_summary=(
            "Koios is the knowledge workspace. It owns provenance, durable notes,\n"
            "and documentation capture."
        ),
        instructions=(
            "Capture validated claims only.",
            "Read inbox first; put knowledge notes or replies in outbox for Hermes delivery.",
            "Preserve provenance for notes and indexes.",
            "Do not edit architecture notes unless the request is explicitly for knowledge capture and routed by Hermes.",
        ),
    ),
}


def workspace_root(root: Path | None = None) -> Path:
    return REPO_ROOT if root is None else root


def ensure_workspace(root: Path, agent: str, *, force: bool = False) -> list[Path]:
    workspace = root / "workspaces" / agent
    workspace.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    for rel in (
        "inbox",
        "outbox",
        "sessions",
        "handoffs/incoming",
        "handoffs/outgoing",
        "decisions",
    ):
        path = workspace / rel
        path.mkdir(parents=True, exist_ok=True)
        created.append(path)

    state = workspace / "state.md"
    active = workspace / "active.md"
    agent_md = workspace / "AGENT.md"

    if force or not state.exists():
        state.write_text(
            f"# {agent.capitalize()} workspace state\n\n"
            "- Current repo:\n"
            "- Current focus:\n"
            "- Blockers:\n"
            "- Last validated decision:\n"
            "- Inbox status:\n"
            "- Outbox status:\n",
            encoding="utf-8",
        )
        created.append(state)

    if force or not active.exists():
        active.write_text(
            f"# {agent.capitalize()} active work\n\n"
            "- Top priority:\n"
            "- Waiting on:\n"
            "- Inbox items to process:\n"
            "- Outbox items to deliver:\n"
            "- Ignore for now:\n",
            encoding="utf-8",
        )
        created.append(active)

    template = TEMPLATES[agent]
    if force or not agent_md.exists():
        agent_md.write_text(template.render(), encoding="utf-8")
        created.append(agent_md)

    return created


def ensure_workspaces(
    root: Path | None = None,
    *,
    agents: Iterable[str] = (),
    force: bool = False,
) -> list[Path]:
    base = workspace_root(root)
    selected = tuple(agents) if agents else CANONICAL_WORKSPACES
    created: list[Path] = []
    for agent in selected:
        created.extend(ensure_workspace(base, agent, force=force))
    return created
