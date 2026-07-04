from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping

from projectkoios.bootstrap.schemas.schemas import SchemaRegistry


class ConcernLevel(StrEnum):
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


def frozen_mapping(value: Mapping[str, Any]) -> Mapping[str, Any]:
    return MappingProxyType(dict(value))


@dataclass(frozen=True, slots=True)
class Concern:
    level: ConcernLevel
    text: str

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Concern:
        return cls(level=ConcernLevel(str(data["level"])), text=str(data["text"]))

    def to_dict(self) -> dict[str, str]:
        return {"level": self.level.value, "text": self.text}


@dataclass(frozen=True, slots=True)
class Section:
    heading: str
    description: str
    concerns: tuple[Concern, ...]
    subsections: tuple[Section, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Section:
        subsections_data = data.get("subsections", ())
        if not isinstance(subsections_data, list | tuple):
            raise TypeError("Section subsections must be a list when present")
        concerns_data = data.get("concerns", ())
        if not isinstance(concerns_data, list | tuple):
            raise TypeError("Section concerns must be a list")
        return cls(
            heading=str(data["heading"]),
            description=str(data["description"]),
            concerns=tuple(Concern.from_dict(item) for item in concerns_data),
            subsections=tuple(Section.from_dict(item) for item in subsections_data),
        )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "heading": self.heading,
            "description": self.description,
            "concerns": [concern.to_dict() for concern in self.concerns],
        }
        if self.subsections:
            result["subsections"] = [section.to_dict() for section in self.subsections]
        return result


@dataclass(frozen=True, slots=True)
class RejectedMarkdown:
    heading: str
    reason: str
    body: str

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> RejectedMarkdown:
        return cls(heading=str(data["heading"]), reason=str(data["reason"]), body=str(data["body"]))

    def to_dict(self) -> dict[str, str]:
        return {"heading": self.heading, "reason": self.reason, "body": self.body}


@dataclass(frozen=True, slots=True)
class RecordMetadata:
    fields: Mapping[str, Any]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> RecordMetadata:
        return cls(fields=frozen_mapping(data))

    def to_dict(self) -> dict[str, Any]:
        return dict(self.fields)


@dataclass(frozen=True, slots=True)
class DraftAdrContent:
    sections: Mapping[str, Section]
    rejected: tuple[RejectedMarkdown, ...]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> DraftAdrContent:
        sections: dict[str, Section] = {}
        for field in DRAFT_ADR_SECTION_FIELDS:
            sections[field] = Section.from_dict(data[field])
        rejected_data = data.get("rejected", ())
        if not isinstance(rejected_data, list | tuple):
            raise TypeError("Draft ADR rejected content must be a list")
        return cls(
            sections=frozen_mapping(sections),
            rejected=tuple(RejectedMarkdown.from_dict(item) for item in rejected_data),
        )

    def to_dict(self) -> dict[str, Any]:
        result = {field: self.sections[field].to_dict() for field in DRAFT_ADR_SECTION_FIELDS}
        result["rejected"] = [item.to_dict() for item in self.rejected]
        return result


@dataclass(frozen=True, slots=True)
class SchemaRecordBase:
    metadata: RecordMetadata
    content: Mapping[str, Any]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any], registry: SchemaRegistry | None = None) -> SchemaRecordBase:
        active_registry = registry or SchemaRegistry()
        active_registry.validate("schema.record-base.json", data)
        return cls(metadata=RecordMetadata.from_dict(data["metadata"]), content=frozen_mapping(data["content"]))

    def to_dict(self) -> dict[str, Any]:
        return {"metadata": self.metadata.to_dict(), "content": dict(self.content)}


@dataclass(frozen=True, slots=True)
class DraftAdrRecord:
    metadata: RecordMetadata
    content: DraftAdrContent

    @classmethod
    def from_dict(cls, data: Mapping[str, Any], registry: SchemaRegistry | None = None) -> DraftAdrRecord:
        active_registry = registry or SchemaRegistry()
        active_registry.validate("adr-draft.schema.json", data)
        return cls(
            metadata=RecordMetadata.from_dict(data["metadata"]),
            content=DraftAdrContent.from_dict(data["content"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {"metadata": self.metadata.to_dict(), "content": self.content.to_dict()}
