from __future__ import annotations

import copy

import pytest
from jsonschema.exceptions import ValidationError

from projectkoios.bootstrap.schemas import SchemaPaths, SchemaRegistry


def valid_draft_adr_record() -> dict:
    section_names = {
        "context": "Context",
        "decision": "Decision",
        "consequences": "Consequences",
        "acceptance_criteria": "Acceptance Criteria",
        "implementation_brief": "Implementation Brief",
        "non_goals": "Non Goals",
        "validation_expectations": "Validation Expectations",
    }
    return {
        "metadata": {
            "record_id": "adr.test-schema-record",
            "schema_id": "https://projectkoios.local/schemas/adr-draft.schema.json",
            "schema_version": "0.1.0-draft",
            "record_version": "0.1.0-draft",
            "title": "Test Schema Record",
            "status": "draft",
            "created_on": "20260704.172632",
            "updated_on": None,
            "origin": {"type": "role_output", "method": "manual", "actor": "ATHENA", "authority": "role"},
            "scope": "projectkoios-bootstrap",
            "repository": "projectkoios-bootstrap",
            "domain": {"domain_type": "architecture", "domain_subtype": "software", "domain_scope": "schema"},
            "source_artifacts": [{"path": "docs/adr/adr.schema-base.md", "relationship": "controls", "role": "ATHENA"}],
            "derived_from": [],
            "evidence": [{"kind": "artifact", "ref": "docs/schemas/adr-draft.schema.json", "claim": "Draft schema exists"}],
            "projections": [{
                "path": "docs/adr/adr.test-schema-record.md",
                "projection_type": "editable_markdown",
                "source_record_id": "adr.test-schema-record",
                "source_schema_id": "https://projectkoios.local/schemas/adr-draft.schema.json",
                "source_schema_version": "0.1.0-draft",
                "projection_method": "manual",
                "generated_by": "ATHENA",
                "editable": True,
                "source_of_truth": "schema_record",
            }],
        },
        "content": {
            field: {
                "heading": heading,
                "description": f"{heading} description.",
                "concerns": [{"level": "MUST", "text": f"Preserve {field}."}],
            }
            for field, heading in section_names.items()
        } | {"rejected": []},
    }


def test__SchemaRegistry__validate__accepts_draft_adr_record():
    SchemaRegistry().validate("adr-draft.schema.json", valid_draft_adr_record())


def test__SchemaRegistry__validate__rejects_extra_top_level_field():
    record = valid_draft_adr_record()
    record["extra"] = "not allowed"
    with pytest.raises(ValidationError):
        SchemaRegistry().validate("adr-draft.schema.json", record)


def test__SchemaRegistry__validate__requires_base_metadata_fields_after_allof_narrowing():
    record = valid_draft_adr_record()
    del record["metadata"]["origin"]
    with pytest.raises(ValidationError):
        SchemaRegistry().validate("adr-draft.schema.json", record)


def test__SchemaRegistry__validate__narrows_schema_id_and_status():
    record = valid_draft_adr_record()
    record["metadata"] = copy.deepcopy(record["metadata"])
    record["metadata"]["schema_id"] = "https://projectkoios.local/schemas/schema.record-base.json"
    with pytest.raises(ValidationError):
        SchemaRegistry().validate("adr-draft.schema.json", record)

    record = valid_draft_adr_record()
    record["metadata"]["status"] = "accepted"
    with pytest.raises(ValidationError):
        SchemaRegistry().validate("adr-draft.schema.json", record)


def test__SchemaRegistry__local_registry__resolves_project_schema_id_offline():
    registry = SchemaRegistry().local_registry()
    resolved = registry.get("https://projectkoios.local/schemas/schema.record-base.json")
    assert resolved.contents["title"] == "SchemaRecordBase"


def test__SchemaPaths__canonical_schema_path__rejects_legacy_schema_files():
    with pytest.raises(ValueError):
        SchemaPaths().canonical_schema_path("legacy-architecture.adr.schema-adr.json")
