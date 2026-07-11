from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]
RECORD_PATH = REPO_ROOT / "dev" / "workflow-objects" / "operator-console-bootstrap-bundle.workflow-object.json"
PACKAGE_JSON_LOCATOR = "src/typescript/projectkoios/ui/operator-console/package.json"
REQUIRED_NON_AUTHORITY_MARKERS = {
    "projection-index-only",
    "not-source-authority",
    "not-completion-authority",
    "not-petri-net-runtime",
    "not-storage-authority",
    "not-schema-authority",
    "static-record",
    "bootstrap-incubation",
    "fixture-only",
    "non-live",
    "stale-by-design",
    "not-product-authority",
}


class WorkflowObjectStaticRecordValidator:
    """Test-only ActionObject for validating the Slice 0 static record DataObject."""

    def loadRecord(self) -> dict[str, Any]:
        """Load the candidate WorkflowObjectRecord DataObject from JSON."""

        return json.loads(RECORD_PATH.read_text())

    def hashFile(self, locator: str) -> str:
        """Return the SHA-256 content ref for a referenced file artifact."""

        return hashlib.sha256((REPO_ROOT / locator).read_bytes()).hexdigest()


def test__operator_console_workflow_object__candidate_zero_shape_is_minimal() -> None:
    """Validate candidate-0 stays bounded to the ATHENA-approved skeleton shape."""
    validator = WorkflowObjectStaticRecordValidator()
    record = validator.loadRecord()

    assert record["record_type"] == "workflow_object"
    assert record["record_shape_version"] == "candidate-0"
    assert record["shape_authority"] == "candidate-only-not-schema-authority"
    assert record["record_id"] == "workflow-object.operator-console-bootstrap-bundle.20260711"
    assert set(record["non_authority_markers"]).issuperset(REQUIRED_NON_AUTHORITY_MARKERS)
    assert record["authority_boundary"]["mode"] == "projection-index-only"
    assert record["authority_boundary"]["source_authorities_preserved"] is True

    assert isinstance(record["work_item"], dict)
    assert len(record["artifact_records"]) == 9
    assert len(record["gate_evaluations"]) == 3
    assert len(record["validation_evidence"]) == 1
    assert len(record["preview_evidence"]) == 1


def test__operator_console_workflow_object__artifact_refs_exist_and_have_hashes() -> None:
    """Validate ArtifactRecord DataObjects point to existing files with current content refs."""
    validator = WorkflowObjectStaticRecordValidator()
    record = validator.loadRecord()

    for artifact in record["artifact_records"]:
        locator = artifact["locator"]
        content_ref = artifact["content_ref"]

        assert (REPO_ROOT / locator).is_file(), locator
        assert content_ref["ref_type"] == "sha256"
        assert content_ref["availability"] == "present"
        assert content_ref["value"] == validator.hashFile(locator)


def test__operator_console_workflow_object__only_required_package_source_ref_is_indexed() -> None:
    """Validate broad package/source indexing remains deferred in Slice 0."""
    record = WorkflowObjectStaticRecordValidator().loadRecord()
    source_like_artifacts = [
        artifact
        for artifact in record["artifact_records"]
        if artifact["artifact_type"] in {"package-manifest", "source-directory", "source-file", "fixture", "lockfile"}
    ]

    assert [artifact["locator"] for artifact in source_like_artifacts] == [PACKAGE_JSON_LOCATOR]
    assert any(item["extension_id"] == "extension:full-artifact-index" for item in record["deferred_extensions"])


def test__operator_console_workflow_object__workflow_places_are_not_artifacts() -> None:
    """Validate WorkflowPlaceRecord DataObjects do not use document paths or ArtifactRecord ids."""
    record = WorkflowObjectStaticRecordValidator().loadRecord()
    artifact_ids = {artifact["artifact_id"] for artifact in record["artifact_records"]}
    artifact_locators = {artifact["locator"] for artifact in record["artifact_records"]}

    for place in record["workflow_places"]:
        place_id = place["place_id"]
        assert place["not_a_document"] is True
        assert place_id not in artifact_ids
        assert place_id not in artifact_locators
        assert not place_id.startswith("docs/")
        assert not place_id.startswith("src/")


def test__operator_console_workflow_object__gate_evaluations_do_not_create_completion_authority() -> None:
    """Validate GateEvaluationRecord DataObjects remain evidence-only."""
    record = WorkflowObjectStaticRecordValidator().loadRecord()

    for evaluation in record["gate_evaluations"]:
        assert evaluation["observed_result"] == "passed"
        assert evaluation["completion_authority_created"] is False
        assert evaluation["evidence_refs"]

    preview = record["preview_evidence"][0]
    assert preview["authority_boundary"] == "preview-evidence-only-not-product-activation"
