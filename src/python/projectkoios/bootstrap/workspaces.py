from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Iterable

from projectkoios.bootstrap.models import REPO_ROOT

CANONICAL_WORKSPACES: tuple[str, ...] = ("hermes", "athena", "vulcan", "koios")


@dataclass(frozen=True, slots=True)
class WorkspaceTemplate:
    """Seed content for one role workspace instruction file.

    Args:
        agent: Workspace agent key.
        title: Human-readable workspace title.
        role_summary: Short role boundary summary.
        instructions: Bullet instructions rendered into the workspace file.
    """

    agent: str
    title: str
    role_summary: str
    instructions: tuple[str, ...]

    def render(self) -> str:
        """Render this template as Markdown text."""
        # Lines accumulates the deterministic Markdown template body.
        lines: list[str] = [
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
                "- sessions/",
                "- working/",
                "- scratch/",
                "- decisions/",
                "",
                "## Document-state coordination",
                "- Treat repository documents and statuses as durable workflow state.",
                "- Use working folders only for current or transitional workspace material.",
                "- Hermes owns cross-domain consistency decisions; directory placement is not authority.",
                "- Prefer updating the owned repository document when the next state is clear.",
                "",
                "## Canonical references",
                "- docs/agents/agent-charter.md",
                "- docs/policies/workspace-layout.md",
                "- docs/architecture/architecture.00.md",
            ]
        )
        return "\n".join(lines).rstrip() + "\n"


TEMPLATES: dict[str, WorkspaceTemplate] = {
    "hermes": WorkspaceTemplate(
        agent="hermes",
        title="Hermes workspace",
        role_summary=(
            "Hermes is the orchestration workspace. It owns repo-state inspection,\n"
            "document-domain consistency, and cross-domain conflict resolution."
        ),
        instructions=(
            "Use this workspace for state reconciliation and repo-state summaries.",
            "Read state, active work, and relevant repository documents before reconciling domains.",
            "Only Hermes may edit architecture notes, and only with explicit Zeus permission.",
            "Keep this workspace focused on current repo, focus, blockers, and next coherent state.",
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
            "Update Athena-owned document state when architecture/specification authority is missing.",
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
            "Update Vulcan-owned implementation and validation state with evidence.",
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
            "Update Koios-owned knowledge and provenance state with cited sources.",
            "Preserve provenance for notes and indexes.",
            "Do not edit architecture notes unless the request is explicitly for knowledge capture and authorized by Hermes.",
        ),
    ),
}


def workspace_root(root: Path | None = None) -> Path:
    """Return the repository root used for workspace materialization."""
    return REPO_ROOT if root is None else root


def role_name(agent: str) -> str:
    """Return the durable display name for a workspace role.

    Args:
        agent: Workspace agent key.

    Returns:
        Uppercase role identity label.
    """
    return agent.upper()


def workspace_document_domain(agent: str) -> str:
    """Return the default document domain summary for a workspace role.

    Args:
        agent: Workspace agent key.

    Returns:
        Human-readable document-domain summary.
    """
    # Domains summarize the owned document surface for generated state files.
    domains: dict[str, str] = {
        "hermes": "orchestration, repo-state reconciliation, cross-domain consistency",
        "athena": "architecture, ADRs, specs, acceptance criteria, implementation briefs",
        "vulcan": "implementation, tests, validation, implementation reports, deviation reports",
        "koios": "knowledge capture, provenance, durable notes, evidence-backed synthesis",
    }
    return domains[agent]


def metadata_block(*, agent: str, title: str, artifact_type: str, status: str, next_owner: str) -> str:
    """Render stable top JSON metadata for workspace control files.

    Args:
        agent: Workspace agent key.
        title: Metadata title.
        artifact_type: Metadata artifact type.
        status: Initial control-surface status.
        next_owner: Initial next-owner value.

    Returns:
        Markdown fenced JSON metadata block.
    """
    # Metadata fields follow the accepted workspace-state ADR minimum set.
    metadata: dict[str, object] = {
        "title": title,
        "artifact_type": artifact_type,
        "status": status,
        "datetime": "seed",
        "acting_as": role_name(agent),
        "repository": "projectkoios-bootstrap",
        "workspace": f"workspaces/{agent}/",
        "document_domain": workspace_document_domain(agent),
        "control_files": ["state.md", "active.md"],
        "next_owner": next_owner,
        "blockers": [],
    }
    return "```json\n" + json.dumps(metadata, indent=2) + "\n```\n\n"


def render_state(agent: str) -> str:
    """Render initial workspace state.md content.

    Args:
        agent: Workspace agent key.

    Returns:
        Markdown workspace state seed content.
    """
    # Title is reused by metadata and the human-readable heading.
    title: str = f"{agent.capitalize()} workspace state"
    # Lines provide the minimum human-readable sections required by the ADR.
    lines: list[str] = [
        metadata_block(agent=agent, title=title, artifact_type="workspace-state", status="seed", next_owner=role_name(agent)),
        f"# {title}",
        "",
        "## Current focus",
        "- Current repo: projectkoios-bootstrap",
        "- Current focus: initialize workspace control surface",
        f"- Document domain: {workspace_document_domain(agent)}",
        "",
        "## Blockers",
        "- None recorded in seed state.",
        "",
        "## Validated state",
        "- Workspace control files have been materialized by the bootstrap initializer.",
        "",
        "## Handoff status",
        "- No active handoff recorded in seed state.",
        "",
        "## Open questions",
        "- None recorded in seed state.",
        "",
        "## Next transition",
        f"- Next owner: {role_name(agent)}",
        "- Next action: replace seed state with current role-owned workspace state when work begins.",
        "",
    ]
    return "\n".join(lines)


def render_active(agent: str) -> str:
    """Render initial workspace active.md content.

    Args:
        agent: Workspace agent key.

    Returns:
        Markdown active-work seed content.
    """
    # Title is reused by metadata and the human-readable heading.
    title: str = f"{agent.capitalize()} active work"
    # Lines provide the minimum next-action sections required by the ADR.
    lines: list[str] = [
        metadata_block(agent=agent, title=title, artifact_type="workspace-active-priorities", status="seed", next_owner=role_name(agent)),
        f"# {title}",
        "",
        "## Current priority stack",
        "1. Replace seed active-work content with the current role-owned priority stack when work begins.",
        "",
        "## Waiting on",
        "- Nothing recorded in seed active work.",
        "",
        "## Working material",
        "- No active working material is recorded in seed active work.",
        "- Files under `working/` are active only when named here.",
        "",
        "## Ignore for now",
        "- Nothing recorded in seed active work.",
        "",
        "## Exit criteria",
        "- Seed state has been replaced with current workspace priorities when active work begins.",
        "",
        "## Next expected artifact",
        "- Updated `state.md` and `active.md` for the current role-owned task.",
        "",
    ]
    return "\n".join(lines)


def ensure_workspace(root: Path, agent: str, *, force: bool = False) -> list[Path]:
    """Ensure one workspace directory and seed files exist.

    Args:
        root: Repository root containing the workspaces directory.
        agent: Workspace agent key to materialize.
        force: Overwrite seed files when true.

    Returns:
        Paths created or overwritten during materialization.
    """

    # Workspace is the role-specific directory under the repository workspace root.
    workspace: Path = root / "workspaces" / agent
    workspace.mkdir(parents=True, exist_ok=True)
    # Created records all directories and files materialized by this call.
    created: list[Path] = []

    # Workspace dirs are the canonical local subdirectories for each role workspace.
    workspace_dirs: tuple[str, ...] = (
        "sessions",
        "working",
        "scratch",
        "decisions",
    )
    rel: str
    for rel in workspace_dirs:
        # Path is the concrete workspace subdirectory being ensured.
        path: Path = workspace / rel
        path.mkdir(parents=True, exist_ok=True)
        created.append(path)

    # State is the durable workspace resume snapshot file.
    state: Path = workspace / "state.md"
    # Active is the current priority and work queue file.
    active: Path = workspace / "active.md"
    # Agent file contains local role instructions for the workspace.
    agent_md: Path = workspace / "AGENTS.md"

    if force or not state.exists():
        state.write_text(render_state(agent), encoding="utf-8")
        created.append(state)

    if force or not active.exists():
        active.write_text(render_active(agent), encoding="utf-8")
        created.append(active)

    # Template provides the role-specific local instruction content.
    template: WorkspaceTemplate = TEMPLATES[agent]
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
    """Ensure canonical workspaces or a selected subset exist.

    Args:
        root: Repository root containing the workspaces directory.
        agents: Optional subset of workspace agent keys.
        force: Overwrite seed files when true.

    Returns:
        Paths created or overwritten across all selected workspaces.
    """

    # Base is the repository root used for materialization.
    base: Path = workspace_root(root)
    # Selected is either the requested agent subset or every canonical workspace.
    selected: tuple[str, ...] = tuple(agents) if agents else CANONICAL_WORKSPACES
    # Created accumulates materialized paths across selected workspaces.
    created: list[Path] = []
    agent: str
    for agent in selected:
        created.extend(ensure_workspace(base, agent, force=force))
    return created
