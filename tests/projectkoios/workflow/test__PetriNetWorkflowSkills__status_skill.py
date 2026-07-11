from __future__ import annotations

import json
from pathlib import Path
from typing import cast


def test__PetriNetWorkflowSkills__manifest_lists_status_skill() -> None:
    """Validate the workflow skills manifest preserves the Slice 1 status skill."""
    # Manifest path is the slice-owned skills index under the workflow package.
    manifest_path: Path = Path("src/python/projectkoios/workflow/skills/manifest.json")
    # Manifest data is parsed so assertions inspect JSON structure, not text only.
    manifest_data: dict[str, object] = cast(dict[str, object], json.loads(manifest_path.read_text(encoding="utf-8")))

    assert manifest_data["surface"] == "projectkoios.workflow.petrinet.agent_affordances"
    assert manifest_data["parent_effort"] == "petri-net-workflow-inspectability"
    assert manifest_data["previous_slice"] == "petrinet-workflow-current-slice-status-reconciliation-slice-2"
    assert manifest_data["status"] == "candidate-slice-3"

    # Skills collection includes the original status skill plus later workflow affordances.
    skills: list[object] = cast(list[object], manifest_data["skills"])
    assert len(skills) == 2

    # Skill entry carries the inspectable command and distribution boundaries.
    skill: dict[str, object] = cast(dict[str, object], skills[0])
    assert skill["name"] == "petrinet-workflow-status"
    assert skill["path"] == "src/python/projectkoios/workflow/skills/petrinet-workflow-status/SKILL.md"
    assert skill["command"] == "uv run projectkoios workflow status"
    assert skill["runtime_mutation_allowed"] is False
    assert skill["harness_global_propagation"] == "deferred"
    assert Path(cast(str, skill["path"])).is_file()


def test__PetriNetWorkflowSkills__status_skill_contains_required_instructions() -> None:
    """Validate the status skill contains the required command, report fields, and workflow-state gate rule."""
    # Skill path is the manifest-listed status skill file.
    skill_path: Path = Path("src/python/projectkoios/workflow/skills/petrinet-workflow-status/SKILL.md")
    # Skill text is inspected for required frontmatter and operating instructions.
    skill_text: str = skill_path.read_text(encoding="utf-8")

    assert "name: petrinet-workflow-status" in skill_text
    assert "surface: projectkoios.workflow.petrinet.agent_affordances" in skill_text
    assert "parent_effort: petri-net-workflow-inspectability" in skill_text
    assert "previous_slice: live-petri-net-skeleton-slice-0" in skill_text
    assert "command: uv run projectkoios workflow status" in skill_text
    assert "runtime_mutation_allowed: false" in skill_text
    assert "harness_global_propagation: deferred" in skill_text
    assert "uv run projectkoios workflow status" in skill_text
    assert "- workflow: <workflow id>" in skill_text
    assert "- current token/place: <token> at <place>" in skill_text
    assert "- enabled transitions: <transition list>" in skill_text
    assert "- user decision required: yes/no" in skill_text
    assert "- recommendation: <one sentence>" in skill_text
    assert "treat it as a workflow-state gate only" in skill_text
    assert "Do not stop unrelated user-delegated implementation" in skill_text
    assert "continue that task after reporting the observed workflow status" in skill_text
    assert "do not fabricate workflow state" in skill_text


def test__PetriNetWorkflowSkills__status_skill_preserves_boundaries() -> None:
    """Validate the status skill preserves non-mutation and non-propagation boundaries."""
    # README path frames the directory-level placement and authority boundaries.
    readme_path: Path = Path("src/python/projectkoios/workflow/skills/README.md")
    # Skill path contains the status-skill-specific boundary list.
    skill_path: Path = Path("src/python/projectkoios/workflow/skills/petrinet-workflow-status/SKILL.md")
    # Combined text lets this test assert directory framing plus skill behavior.
    combined_text: str = readme_path.read_text(encoding="utf-8") + "\n" + skill_path.read_text(encoding="utf-8")

    assert "Petri-net workflow harness" in combined_text
    assert "not a new project identity" in combined_text
    assert "Do not fire transitions." in combined_text
    assert "Do not mutate workflow state." in combined_text
    assert "Do not treat the static bootstrap fixture as canonical workflow authority." in combined_text
    assert "Do not launch subagents merely because a transition is enabled." in combined_text
    assert "Do not expand scope beyond the user's current request." in combined_text
    assert "do not propagate themselves into `agents/global/*/skills/`" in combined_text
    assert "ask before file edits, routing, subagent launch, active/queued-state change" in combined_text
