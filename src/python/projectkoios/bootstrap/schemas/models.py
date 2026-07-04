from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping

from projectkoios.bootstrap.schemas.schemas import SchemaRegistry

JsonObject = dict[str, Any]
JsonMapping = Mapping[str, Any]


class ConcernLevel(StrEnum):
    """Normative concern levels supported by draft ADR content."""

    MUST = "MUST"
    MUST_NOT = "MUST NOT"
    SHOULD = "SHOULD"
    SHOULD_NOT = "SHOULD NOT"
    MAY = "MAY"


CONCERN_LEVEL_ORDER: tuple[ConcernLevel, ...] = (
    ConcernLevel.MUST,
    ConcernLevel.MUST_NOT,
    ConcernLevel.SHOULD,
    ConcernLevel.SHOULD_NOT,
    ConcernLevel.MAY,
)

DRAFT_ADR_SECTION_FIELDS: tuple[str, ...] = (
    "context",
    "decision",
    "consequences",
    "acceptance_criteria",
    "implementation_brief",
    "non_goals",
    "validation_expectations",
)

DRAFT_ADR_SECTION_HEADINGS: dict[str, str] = {
    "context": "Context",
    "decision": "Decision",
    "consequences": "Consequences",
    "acceptance_criteria": "Acceptance Criteria",
    "implementation_brief": "Implementation Brief",
    "non_goals": "Non Goals",
    "validation_expectations": "Validation Expectations",
}


def frozen_mapping(value: JsonMapping) -> JsonMapping:
    """Return an immutable shallow copy of a JSON mapping.

    Args:
        value: Mapping to freeze.

    Returns:
        Read-only mapping proxy.
    """
    return MappingProxyType(dict(value))


@dataclass(frozen=True, slots=True)
class Concern:
    """Normative concern attached to an ADR section.

    Args:
        level: Normative keyword level.
        text: Concern text without the leading keyword.
    """

    level: ConcernLevel
    text: str

    @classmethod
    def from_dict(cls, data: JsonMapping) -> Concern:
        """Build a concern from schema-shaped data.

        Args:
            data: Concern mapping.

        Returns:
            Concern instance.
        """
        return cls(level=ConcernLevel(str(data["level"])), text=str(data["text"]))

    def to_dict(self) -> dict[str, str]:
        """Serialize the concern to schema-shaped data.

        Returns:
            JSON-compatible concern mapping.
        """
        return {"level": self.level.value, "text": self.text}


@dataclass(frozen=True, slots=True)
class Section:
    """Draft ADR section content.

    Args:
        heading: Rendered section heading.
        description: Non-normative section description.
        concerns: Normative concerns in the section.
        subsections: Nested subsections, when supported by schema.
    """

    heading: str
    description: str
    concerns: tuple[Concern, ...]
    subsections: tuple[Section, ...] = ()

    @classmethod
    def from_dict(cls, data: JsonMapping) -> Section:
        """Build a section from schema-shaped data.

        Args:
            data: Section mapping.

        Returns:
            Section instance.

        Raises:
            TypeError: If list-shaped fields are not lists or tuples.
        """
        # Raw subsection payload comes from validated JSON data.
        subsections_data: object = data.get("subsections", ())
        if not isinstance(subsections_data, list | tuple):
            raise TypeError("Section subsections must be a list when present")
        # Raw concern payload comes from validated JSON data.
        concerns_data: object = data.get("concerns", ())
        if not isinstance(concerns_data, list | tuple):
            raise TypeError("Section concerns must be a list")
        return cls(
            heading=str(data["heading"]),
            description=str(data["description"]),
            concerns=tuple(Concern.from_dict(item) for item in concerns_data),
            subsections=tuple(Section.from_dict(item) for item in subsections_data),
        )

    def to_dict(self) -> JsonObject:
        """Serialize the section to schema-shaped data.

        Returns:
            JSON-compatible section mapping.
        """
        # Result starts with fields required by the section schema.
        result: JsonObject = {
            "heading": self.heading,
            "description": self.description,
            "concerns": [concern.to_dict() for concern in self.concerns],
        }
        if self.subsections:
            result["subsections"] = [section.to_dict() for section in self.subsections]
        return result


@dataclass(frozen=True, slots=True)
class RejectedMarkdown:
    """Markdown content captured because it is outside the draft ADR contract.

    Args:
        heading: Captured heading.
        reason: Deterministic rejection reason.
        body: Captured Markdown body.
    """

    heading: str
    reason: str
    body: str

    @classmethod
    def from_dict(cls, data: JsonMapping) -> RejectedMarkdown:
        """Build rejected Markdown from schema-shaped data.

        Args:
            data: Rejected Markdown mapping.

        Returns:
            Rejected Markdown instance.
        """
        return cls(heading=str(data["heading"]), reason=str(data["reason"]), body=str(data["body"]))

    def to_dict(self) -> dict[str, str]:
        """Serialize rejected Markdown to schema-shaped data.

        Returns:
            JSON-compatible rejected Markdown mapping.
        """
        return {"heading": self.heading, "reason": self.reason, "body": self.body}


@dataclass(frozen=True, slots=True)
class RecordMetadata:
    """Immutable schema-record metadata wrapper.

    Args:
        fields: Metadata fields from the base schema.
    """

    fields: JsonMapping

    @classmethod
    def from_dict(cls, data: JsonMapping) -> RecordMetadata:
        """Build metadata from schema-shaped data.

        Args:
            data: Metadata mapping.

        Returns:
            Metadata instance.
        """
        return cls(fields=frozen_mapping(data))

    def to_dict(self) -> JsonObject:
        """Serialize metadata to a mutable mapping.

        Returns:
            JSON-compatible metadata mapping.
        """
        return dict(self.fields)


@dataclass(frozen=True, slots=True)
class DraftAdrContent:
    """Content for the draft ADR schema family.

    Args:
        sections: Required draft ADR sections keyed by schema field name.
        rejected: Captured rejected Markdown entries.
    """

    sections: Mapping[str, Section]
    rejected: tuple[RejectedMarkdown, ...]

    @classmethod
    def from_dict(cls, data: JsonMapping) -> DraftAdrContent:
        """Build draft ADR content from schema-shaped data.

        Args:
            data: Draft ADR content mapping.

        Returns:
            Draft ADR content instance.

        Raises:
            TypeError: If rejected content is not list-shaped.
        """
        # Required sections are loaded in deterministic schema order.
        sections: dict[str, Section] = {}
        field: str
        for field in DRAFT_ADR_SECTION_FIELDS:
            sections[field] = Section.from_dict(data[field])
        # Raw rejected payload is validated before object conversion.
        rejected_data: object = data.get("rejected", ())
        if not isinstance(rejected_data, list | tuple):
            raise TypeError("Draft ADR rejected content must be a list")
        return cls(
            sections=frozen_mapping(sections),
            rejected=tuple(RejectedMarkdown.from_dict(item) for item in rejected_data),
        )

    def to_dict(self) -> JsonObject:
        """Serialize draft ADR content to schema-shaped data.

        Returns:
            JSON-compatible content mapping.
        """
        # Result preserves deterministic section order.
        result: JsonObject = {field: self.sections[field].to_dict() for field in DRAFT_ADR_SECTION_FIELDS}
        result["rejected"] = [item.to_dict() for item in self.rejected]
        return result


@dataclass(frozen=True, slots=True)
class SchemaRecordBase:
    """Base schema-record envelope.

    Args:
        metadata: Base record metadata.
        content: Family-owned content mapping.
    """

    metadata: RecordMetadata
    content: JsonMapping

    @classmethod
    def from_dict(cls, data: JsonMapping, registry: SchemaRegistry | None = None) -> SchemaRecordBase:
        """Build a base record after schema validation.

        Args:
            data: Base record mapping.
            registry: Optional schema registry.

        Returns:
            Base record instance.
        """
        # Active registry validates the base envelope before model construction.
        active_registry: SchemaRegistry = registry or SchemaRegistry()
        active_registry.validate("schema.record-base.json", data)
        return cls(metadata=RecordMetadata.from_dict(data["metadata"]), content=frozen_mapping(data["content"]))

    def to_dict(self) -> JsonObject:
        """Serialize the base record to schema-shaped data.

        Returns:
            JSON-compatible base record mapping.
        """
        return {"metadata": self.metadata.to_dict(), "content": dict(self.content)}


@dataclass(frozen=True, slots=True)
class DraftAdrRecord:
    """Concrete draft ADR schema record.

    Args:
        metadata: Base record metadata.
        content: Draft ADR content.
    """

    metadata: RecordMetadata
    content: DraftAdrContent

    @classmethod
    def from_dict(cls, data: JsonMapping, registry: SchemaRegistry | None = None) -> DraftAdrRecord:
        """Build a draft ADR record after schema validation.

        Args:
            data: Draft ADR record mapping.
            registry: Optional schema registry.

        Returns:
            Draft ADR record instance.
        """
        # Active registry validates base and family schema constraints.
        active_registry: SchemaRegistry = registry or SchemaRegistry()
        active_registry.validate("adr-draft.schema.json", data)
        return cls(
            metadata=RecordMetadata.from_dict(data["metadata"]),
            content=DraftAdrContent.from_dict(data["content"]),
        )

    def to_dict(self) -> JsonObject:
        """Serialize the draft ADR record to schema-shaped data.

        Returns:
            JSON-compatible draft ADR record mapping.
        """
        return {"metadata": self.metadata.to_dict(), "content": self.content.to_dict()}
