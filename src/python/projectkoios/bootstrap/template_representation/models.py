from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Any

JsonObject = dict[str, Any]

TEMPLATE_REPRESENTATION_VERSION = "0.1.0"
TEMPLATE_RECORD_SCHEMA_ID = "https://projectkoios.local/schemas/template-record.schema.json"
TEMPLATE_RECORD_SCHEMA_VERSION = "0.1.0-draft"
TEMPLATE_RECORD_VERSION = "0.1.0-draft"


class TemplateNamespace(StrEnum):
    """Supported bootstrap document namespaces for template representation."""

    TEMPLATE = "template"
    IMPLEMENTATION = "implementation"
    PLAN = "plan"
    OTHER = "other"


@dataclass(frozen=True, slots=True)
class TemplateMarker:
    """Deterministically detected template placeholder or instruction marker.

    Args:
        marker: Marker text as it appears in controlled Markdown.
        location: Template location where the marker was found.
    """

    marker: str
    location: str

    @classmethod
    def from_dict(cls, data: JsonObject) -> TemplateMarker:
        """Build a template marker from serialized data.

        Args:
            data: Serialized marker data.

        Returns:
            Template marker instance.
        """

        return cls(marker=str(data["marker"]), location=str(data["location"]))

    def to_dict(self) -> dict[str, str]:
        """Serialize the marker to JSON-compatible data.

        Returns:
            Serialized marker mapping.
        """

        return {"marker": self.marker, "location": self.location}


@dataclass(frozen=True, slots=True)
class TemplateSection:
    """Ordered Markdown section in a bootstrap template representation.

    Args:
        heading: Section heading text without Markdown heading marker.
        body: Section body text normalized for deterministic rendering.
        markers: Deterministically detected placeholders or instruction markers.
    """

    heading: str
    body: str
    markers: tuple[TemplateMarker, ...] = ()

    @classmethod
    def from_dict(cls, data: JsonObject) -> TemplateSection:
        """Build a template section from serialized data.

        Args:
            data: Serialized section data.

        Returns:
            Template section instance.
        """

        # Marker data is read from controlled serialized representation.
        marker_data: object = data.get("markers", ())
        if not isinstance(marker_data, list | tuple):
            raise TypeError("section markers must be a list")
        return cls(
            heading=str(data["heading"]),
            body=str(data["body"]),
            markers=tuple(TemplateMarker.from_dict(item) for item in marker_data),
        )

    def to_dict(self) -> JsonObject:
        """Serialize the section to JSON-compatible data.

        Returns:
            Serialized section mapping.
        """

        return {
            "heading": self.heading,
            "body": self.body,
            "markers": [marker.to_dict() for marker in self.markers],
        }


@dataclass(frozen=True, slots=True)
class TemplateRecord:
    """Canonical bootstrap template representation.

    Args:
        template_id: Stable template identifier.
        source_path: Repository-relative source path.
        title: Top-level Markdown heading.
        sections: Ordered Markdown sections.
        markers: Document-level detected placeholders or instruction markers.
        representation_version: Representation contract version.
        preamble: Controlled Markdown before the top-level heading.
        lead_body: Controlled Markdown between top-level heading and first section.
    """

    template_id: str
    source_path: str
    title: str
    sections: tuple[TemplateSection, ...]
    markers: tuple[TemplateMarker, ...] = ()
    representation_version: str = TEMPLATE_REPRESENTATION_VERSION
    preamble: str = ""
    lead_body: str = ""

    @classmethod
    def from_dict(cls, data: JsonObject) -> TemplateRecord:
        """Build a template record from serialized data.

        Args:
            data: Serialized template record data.

        Returns:
            Template record instance.
        """

        # Section data is read from controlled serialized representation.
        section_data: object = data.get("sections", ())
        if not isinstance(section_data, list | tuple):
            raise TypeError("template sections must be a list")
        # Marker data is read from controlled serialized representation.
        marker_data: object = data.get("markers", ())
        if not isinstance(marker_data, list | tuple):
            raise TypeError("template markers must be a list")
        return cls(
            template_id=str(data["template_id"]),
            source_path=str(data["source_path"]),
            title=str(data["title"]),
            sections=tuple(TemplateSection.from_dict(item) for item in section_data),
            markers=tuple(TemplateMarker.from_dict(item) for item in marker_data),
            representation_version=str(data["representation_version"]),
            preamble=str(data.get("preamble", "")),
            lead_body=str(data.get("lead_body", "")),
        )

    def to_dict(self) -> JsonObject:
        """Serialize the template record to JSON-compatible data.

        Returns:
            Serialized template record mapping.
        """

        return {
            "template_id": self.template_id,
            "source_path": self.source_path,
            "title": self.title,
            "sections": [section.to_dict() for section in self.sections],
            "markers": [marker.to_dict() for marker in self.markers],
            "representation_version": self.representation_version,
            "preamble": self.preamble,
            "lead_body": self.lead_body,
        }

    @classmethod
    def from_schema_record(cls, data: JsonObject) -> TemplateRecord:
        """Build a template record from a schema-backed record instance.

        Args:
            data: Schema-backed template record instance.

        Returns:
            Template record instance built from schema content.
        """

        return cls.from_dict(self_content(data))

    def to_schema_record(self, *, created_on: str, updated_on: str | None = None) -> JsonObject:
        """Serialize the template record into the schema-backed record envelope.

        Args:
            created_on: Deterministic record creation timestamp.
            updated_on: Optional record update timestamp.

        Returns:
            Schema-backed template record instance.
        """

        return {
            "metadata": {
                "record_id": f"template.{self.template_id}",
                "schema_id": TEMPLATE_RECORD_SCHEMA_ID,
                "schema_version": TEMPLATE_RECORD_SCHEMA_VERSION,
                "record_version": TEMPLATE_RECORD_VERSION,
                "title": self.title,
                "status": "draft",
                "created_on": created_on,
                "updated_on": updated_on,
                "origin": {"type": "derived", "method": "ingester", "actor": "VULCAN", "authority": "role"},
                "scope": "projectkoios-bootstrap bootstrap template representation",
                "repository": "projectkoios-bootstrap",
                "domain": {
                    "domain_type": "schema",
                    "domain_subtype": "template-representation",
                    "domain_scope": "bootstrap-template",
                },
                "source_artifacts": [{"path": self.source_path, "relationship": "derived_from", "role": "template"}],
                "derived_from": [],
                "evidence": [{"kind": "file", "ref": self.source_path, "claim": "Template Markdown parsed into schema-backed record"}],
                "projections": [{
                    "path": self.source_path,
                    "projection_type": "editable_markdown",
                    "source_record_id": f"template.{self.template_id}",
                    "source_schema_id": TEMPLATE_RECORD_SCHEMA_ID,
                    "source_schema_version": TEMPLATE_RECORD_SCHEMA_VERSION,
                    "projection_method": "ingester",
                    "generated_by": "VULCAN",
                    "editable": True,
                    "source_of_truth": "projection",
                }],
            },
            "content": self.to_dict(),
        }

    def semantic_dict(self) -> JsonObject:
        """Return semantic equality data for round-trip comparison.

        Returns:
            Serialized record data excluding presentation-only preamble whitespace.
        """

        # Semantic data starts from full serialization and normalizes preamble whitespace.
        data: JsonObject = self.to_dict()
        data["preamble"] = self.preamble.strip()
        return data


def self_content(data: JsonObject) -> JsonObject:
    """Return content object from a schema-backed record.

    Args:
        data: Schema-backed record data.

    Returns:
        Template record content object.

    Raises:
        TypeError: If content is not object-shaped.
    """

    # Content holds the family-specific template representation fields.
    content: object = data["content"]
    if not isinstance(content, dict):
        raise TypeError("template schema record content must be an object")
    return content


@dataclass(frozen=True, slots=True)
class NamespaceClassification:
    """Classification for a repository document path.

    Args:
        namespace: Bootstrap document namespace classification.
        path: Repository-relative path.
    """

    namespace: TemplateNamespace
    path: str

    def to_dict(self) -> MappingProxyType[str, str]:
        """Serialize namespace classification as an immutable mapping.

        Returns:
            Serialized immutable classification mapping.
        """

        return MappingProxyType({"namespace": self.namespace.value, "path": self.path})
