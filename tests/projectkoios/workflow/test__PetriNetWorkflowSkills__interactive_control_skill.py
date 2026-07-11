from __future__ import annotations

import json
from pathlib import Path
from typing import cast


def test__PetriNetWorkflowSkills__manifest_lists_interactive_control_skill() -> None:
    """Validate the manifest lists the workflow-local interactive-control skill."""
    # Manifest path is the workflow-local skill index, not a global skill registry.
    manifest_path: Path = Path("src/python/projectkoios/workflow/skills/manifest.json")
    # Manifest JSON is parsed to validate the inspectable index shape.
    manifest_data: dict[str, object] = cast(dict[str, object], json.loads(manifest_path.read_text(encoding="utf-8")))

    assert manifest_data["surface"] == "projectkoios.workflow.petrinet.agent_affordances"
    assert manifest_data["parent_effort"] == "petri-net-workflow-inspectability"
    assert manifest_data["previous_slice"] == "petrinet-workflow-current-slice-status-reconciliation-slice-2"
    assert manifest_data["status"] == "candidate-slice-3"

    # Skills collection contains each workflow-local affordance entry.
    skills: list[object] = cast(list[object], manifest_data["skills"])
    # Skill lookup verifies both entries without relying only on order.
    skill_by_name: dict[str, dict[str, object]] = {
        cast(str, cast(dict[str, object], skill)["name"]): cast(dict[str, object], skill) for skill in skills
    }

    assert set(skill_by_name) == {"petrinet-workflow-status", "petrinet-workflow-interactive-control"}
    assert skill_by_name["petrinet-workflow-status"]["path"] == "src/python/projectkoios/workflow/skills/petrinet-workflow-status/SKILL.md"

    # Interactive control skill remains read-only and workflow-local.
    interactive_skill: dict[str, object] = skill_by_name["petrinet-workflow-interactive-control"]
    assert interactive_skill["path"] == "src/python/projectkoios/workflow/skills/petrinet-workflow-interactive-control/SKILL.md"
    assert interactive_skill["command"] == "uv run projectkoios workflow status"
    assert interactive_skill["runtime_mutation_allowed"] is False
    assert interactive_skill["harness_global_propagation"] == "deferred"
    assert Path(cast(str, interactive_skill["path"])).is_file()


def test__PetriNetWorkflowSkills__interactive_control_skill_contains_required_behavior() -> None:
    """Validate the interactive-control skill defines inspect, summarize, recommend, and ask behavior."""
    # Skill path is the new Slice 3 interactive-control affordance.
    skill_path: Path = Path("src/python/projectkoios/workflow/skills/petrinet-workflow-interactive-control/SKILL.md")
    # Skill text is checked for required frontmatter and operator behavior.
    skill_text: str = skill_path.read_text(encoding="utf-8")

    assert "name: petrinet-workflow-interactive-control" in skill_text
    assert "surface: projectkoios.workflow.petrinet.agent_affordances" in skill_text
    assert "parent_effort: petri-net-workflow-inspectability" in skill_text
    assert "previous_slice: petrinet-workflow-current-slice-status-reconciliation-slice-2" in skill_text
    assert "command: uv run projectkoios workflow status" in skill_text
    assert "runtime_mutation_allowed: false" in skill_text
    assert "harness_global_propagation: deferred" in skill_text
    assert "inspect → summarize → recommend → ask/act" in skill_text
    assert "uv run projectkoios workflow status" in skill_text
    assert "workflow id" in skill_text
    assert "current token/place" in skill_text
    assert "active slice if visible" in skill_text
    assert "enabled transitions" in skill_text
    assert "whether user decision is required" in skill_text
    assert "active vs queued vs superseded/deferred distinction" in skill_text
    assert "Recommend exactly one primary next action" in skill_text
    assert "Ask before acting" in skill_text
    assert "edit files, route work to another agent, launch subagents, change active/queued state" in skill_text
    assert "Act only after approval" in skill_text
    assert "do not invent workflow id" in skill_text


def test__PetriNetWorkflowSkills__interactive_control_skill_preserves_boundaries() -> None:
    """Validate the interactive-control skill preserves slice boundaries."""
    # README gives directory-level authority framing.
    readme_path: Path = Path("src/python/projectkoios/workflow/skills/README.md")
    # Skill path gives interactive-control-specific boundaries.
    skill_path: Path = Path("src/python/projectkoios/workflow/skills/petrinet-workflow-interactive-control/SKILL.md")
    # Combined text checks that both directory and skill boundaries are present.
    combined_text: str = readme_path.read_text(encoding="utf-8") + "\n" + skill_path.read_text(encoding="utf-8")

    assert "petrinet-workflow-status" in combined_text
    assert "petrinet-workflow-interactive-control" in combined_text
    assert "not a new project identity" in combined_text
    assert "Do not fire transitions." in combined_text
    assert "Do not mutate workflow state." in combined_text
    assert "Do not edit files unless the user explicitly approves" in combined_text
    assert "Do not launch subagents or route work merely because a transition is enabled." in combined_text
    assert "Do not activate queued work without explicit USER/HERMES direction." in combined_text
    assert "Do not treat the static bootstrap workflow-net fixture as canonical workflow authority." in combined_text
    assert "Do not treat tests as the main explanation of progress." in combined_text
    assert "Do not introduce persistence, schema authority, live adapter/session reads" in combined_text
    assert "Operator Console integration, workflow-object runtime coupling" in combined_text
    assert "product/mothership authority" in combined_text
    assert "Do not propagate this skill into global skill directories." in combined_text
    assert "Do not replace or supersede `pi-skill-determinism-slice-0`" in combined_text
