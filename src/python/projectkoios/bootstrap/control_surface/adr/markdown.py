from __future__ import annotations

from dataclasses import dataclass
import re
from re import Pattern

from projectkoios.bootstrap.schema.models import JsonObject


class AdrMarkdownError(ValueError):
    """Raised when ADR Markdown cannot be mapped deterministically."""


SECTION_HEADING_PATTERN: Pattern[str] = re.compile(r"^## (?P<heading>.+)$")
REQUIRED_SECTION_KEYS: tuple[str, ...] = (
    "status",
    "context",
    "decision",
    "consequences",
    "architecture-spec",
    "acceptance-criteria",
    "implementation-brief",
    "resolved_open_questions",
    "non_goals",
    "validation_expectations",
    "routing",
    "links",
)


@dataclass(frozen=True, slots=True)
class AdrMarkdownMapper:
    """Map the one source ADR Markdown fixture into schema-shaped JSON."""

    def map_source(self, markdown: str) -> tuple[JsonObject, JsonObject]:
        """Map legacy/source Markdown to a plain ADR schema record.

        Args:
            markdown: Source Markdown text.

        Returns:
            ADR record and mapping evidence.
        """
        # Parsed sections drive the deterministic fixture mapping.
        sections: dict[str, str] = self.sections(markdown)
        # Title is extracted separately because it includes timestamp provenance.
        title: str = self.title(markdown)
        # Context key-value lines become the schema context object.
        context: JsonObject = self.context(sections["context"])
        # Routing key-value lines become schema routing values.
        routing: JsonObject = self.routing(sections["routing"])
        # Links key-value lines become optional schema links values.
        links: JsonObject = self.links(sections["links"])
        # Record is the plain schema-backed checkpoint object.
        record: JsonObject = {
            "id": "adr.json-database-for-adr-storage",
            "slug": "json-database-for-adr-storage",
            "title": title,
            "status": self.status(sections["status"]),
            "context": context,
            "decision": sections["decision"],
            "consequences": sections["consequences"],
            "architecture_spec": sections["architecture-spec"],
            "acceptance_criteria": self.bullets(sections["acceptance-criteria"]),
            "implementation_brief": sections["implementation-brief"],
            "resolved_open_questions": self.bullets(sections["resolved_open_questions"]),
            "non_goals": self.bullets(sections["non_goals"]),
            "validation_expectations": self.bullets(sections["validation_expectations"]),
            "routing": routing,
            "links": links,
        }
        # Mapping evidence carries source provenance excluded by the plain ADR schema.
        mapping: JsonObject = self.mapping_evidence(sections)
        return record, mapping

    def map_projection(self, markdown: str) -> JsonObject:
        """Map generated projection Markdown back to ADR record JSON.

        Args:
            markdown: Generated projection Markdown.

        Returns:
            ADR record contained in the projection.
        """
        # Projection embeds deterministic JSON between explicit fences.
        start_marker: str = "```json adr-record"
        # End marker closes the embedded ADR record JSON block.
        end_marker: str = "```"
        # Start index locates the generated schema-backed payload.
        start_index: int = markdown.find(start_marker)
        if start_index < 0:
            raise AdrMarkdownError("Projection missing ADR record JSON fence")
        # JSON start skips the projection fence marker.
        json_start: int = start_index + len(start_marker)
        # End index terminates the embedded JSON payload.
        end_index: int = markdown.find(end_marker, json_start)
        if end_index < 0:
            raise AdrMarkdownError("Projection ADR record JSON fence is unclosed")
        import json
        # JSON payload is parsed only after fence boundaries are known.
        payload: object = json.loads(markdown[json_start:end_index].strip())
        if not isinstance(payload, dict):
            raise AdrMarkdownError("Projection ADR record payload must be an object")
        return payload

    def title(self, markdown: str) -> str:
        """Extract the ADR title without timestamp prefix.

        Args:
            markdown: Source Markdown text.

        Returns:
            Schema title.
        """
        # First line must be the one source title heading.
        first_line: str = markdown.splitlines()[0]
        if not first_line.startswith("# ADR "):
            raise AdrMarkdownError("Source ADR missing title heading")
        return first_line.split(": ", maxsplit=1)[1].strip()

    def sections(self, markdown: str) -> dict[str, str]:
        """Split Markdown into normalized second-level sections.

        Args:
            markdown: Source Markdown text.

        Returns:
            Mapping from normalized section key to body.
        """
        # Lines preserve section boundaries for fixture parsing.
        lines: list[str] = markdown.splitlines()
        # Parsed section bodies are accumulated under normalized headings.
        sections: dict[str, list[str]] = {}
        # Current key tracks which second-level section receives following lines.
        current_key: str | None = None
        line: str
        for line in lines[1:]:
            # Match identifies the next second-level section boundary.
            match: re.Match[str] | None = SECTION_HEADING_PATTERN.match(line)
            if match is not None:
                current_key = self.section_key(match.group("heading"))
                sections[current_key] = []
                continue
            if current_key is not None:
                sections[current_key].append(line)
        # Normalized sections collapse line arrays into comparable body text.
        normalized: dict[str, str] = {key: "\n".join(value).strip() for key, value in sections.items()}
        # Missing section names produce an explicit fixture mapping failure.
        missing: list[str] = [key for key in REQUIRED_SECTION_KEYS if key not in normalized]
        if missing:
            raise AdrMarkdownError(f"Source ADR missing sections: {', '.join(missing)}")
        return normalized

    def section_key(self, heading: str) -> str:
        """Normalize a Markdown heading to a fixture section key.

        Args:
            heading: Markdown heading text.

        Returns:
            Normalized section key.
        """
        return heading.strip().lower().replace(" ", "_").replace("-", "-")

    def status(self, body: str) -> str:
        """Extract lifecycle status from the status section body.

        Args:
            body: Status section body.

        Returns:
            Schema status.
        """
        # First non-empty line is the lifecycle status value.
        lines: list[str] = [line.strip() for line in body.splitlines() if line.strip()]
        if not lines:
            raise AdrMarkdownError("Status section is empty")
        return lines[0]

    def context(self, body: str) -> JsonObject:
        """Map source context lines to schema context.

        Args:
            body: Context section body.

        Returns:
            Schema context object.
        """
        # Parsed key-value metadata precedes context prose.
        values: dict[str, str] = self.key_values(body)
        return {
            "origin": values["Origin"],
            "from": values["From"],
            "acting_as": values["Acting-As"],
            "scope": values["Scope"],
            "repository": values["Repository"],
            "delegated_operator": "HERMES",
            "architecture_domain": values["Architecture-Domain"],
        }

    def routing(self, body: str) -> JsonObject:
        """Map source routing lines to schema routing.

        Args:
            body: Routing section body.

        Returns:
            Schema routing object.
        """
        # Routing key names are title-cased in the source fixture.
        values: dict[str, str] = self.key_values(body)
        # Next phase is normalized from legacy wording into schema enum wording.
        next_phase: str = values["Next phase"].lower()
        if next_phase == "proposed":
            next_phase = "proposal"
        return {"owner": values["Owner"], "next_phase": next_phase, "notes": values["Notes"]}

    def links(self, body: str) -> JsonObject:
        """Map source links lines to schema links.

        Args:
            body: Links section body.

        Returns:
            Schema links object.
        """
        # Link values may use textual None in legacy Markdown.
        values: dict[str, str] = self.key_values(body)
        return {
            "back_to": values["back_to"],
            "supersedes": self.none_value(values["supersedes"]),
            "superseded_by": self.none_value(values["superseded_by"]),
        }

    def key_values(self, body: str) -> dict[str, str]:
        """Parse colon key-value lines from a section body.

        Args:
            body: Section body.

        Returns:
            Parsed key-value mapping.
        """
        # Parsed key-value pairs ignore prose and bullet lines.
        values: dict[str, str] = {}
        line: str
        for line in body.splitlines():
            # Bullet prefix is presentation-only for key-value sections.
            cleaned_line: str = line.removeprefix("- ")
            if ":" not in cleaned_line:
                continue
            key: str
            value: str
            key, value = cleaned_line.split(":", maxsplit=1)
            if key and value.strip():
                values[key.strip()] = value.strip()
        return values

    def bullets(self, body: str) -> list[str]:
        """Extract Markdown bullet text from a section body.

        Args:
            body: Section body.

        Returns:
            Bullet text values.
        """
        # Bullets carry list-shaped schema values.
        values: list[str] = []
        line: str
        for line in body.splitlines():
            if line.startswith("- "):
                values.append(line.removeprefix("- ").strip())
        if not values:
            raise AdrMarkdownError("Expected at least one bullet value")
        return values

    def none_value(self, value: str) -> str | None:
        """Convert legacy textual None to JSON null.

        Args:
            value: Source value.

        Returns:
            Source value or None.
        """
        if value == "None":
            return None
        return value

    def mapping_evidence(self, sections: dict[str, str]) -> JsonObject:
        """Build copied, inferred, and normalized mapping evidence.

        Args:
            sections: Parsed source sections.

        Returns:
            Mapping evidence object.
        """
        return {
            "status": "pilot-derived-non-authoritative",
            "source_path": "docs/adr/adr.json-database-for-adr-storage.draft.md",
            "source_filename_status_suffix": ".draft",
            "canonical_identity_rule": "status-free id and slug; lifecycle status lives in record content",
            "canonical_id": "adr.json-database-for-adr-storage",
            "canonical_slug": "json-database-for-adr-storage",
            "record_status": self.status(sections["status"]),
            "copied_fields": [
                "title",
                "status",
                "context.origin",
                "context.from",
                "context.acting_as",
                "context.scope",
                "context.repository",
                "context.architecture_domain",
                "decision",
                "consequences",
                "architecture_spec",
                "acceptance_criteria",
                "implementation_brief",
                "resolved_open_questions",
                "non_goals",
                "validation_expectations",
                "routing.owner",
                "routing.notes",
                "links",
            ],
            "inferred_fields": {"context.delegated_operator": "HERMES"},
            "normalized_fields": {"routing.next_phase": "proposed -> proposal"},
            "preserved_outside_schema": {"source_date": "20260702.121432Z"},
        }


@dataclass(frozen=True, slots=True)
class AdrProjectionRenderer:
    """Render deterministic non-authoritative Markdown projections."""

    def render(self, record: JsonObject, manifest: JsonObject, record_json: str) -> str:
        """Render a generated pilot projection.

        Args:
            record: ADR record to project.
            manifest: Pilot manifest/config.
            record_json: Deterministic ADR record JSON.

        Returns:
            Generated Markdown projection.
        """
        # Metadata lines make pilot authority boundaries visible to reviewers.
        lines: list[str] = [
            "<!-- GENERATED PILOT PROJECTION: non-authoritative; do not edit as ADR authority. -->",
            f"# ADR Projection: {record['title']}",
            "",
            "## Projection metadata",
            "",
            f"- Pilot status: {manifest['pilot']['status']}",
            f"- Source record ID: {record['id']}",
            f"- Canonical slug: {record['slug']}",
            f"- Record status: {record['status']}",
            f"- Legacy/source path: {manifest['source_adr']['path']}",
            f"- Schema ID: {manifest['schema']['id']}",
            f"- Generation method: {manifest['generation']['method']}",
            f"- Source-of-truth mode: {manifest['authority_mode']}",
            f"- Source hash: {manifest['source_adr']['content_hash']}",
            f"- JSON checkpoint hash: {manifest['json_checkpoint']['content_hash']}",
            f"- Conflict rule: {manifest['conflict_rule']}",
            "",
            "```json adr-record",
            record_json.rstrip(),
            "```",
            "",
        ]
        lines.extend(self.render_sections(record))
        return "\n".join(lines).rstrip() + "\n"

    def render_sections(self, record: JsonObject) -> list[str]:
        """Render human-readable ADR sections from a record.

        Args:
            record: ADR record.

        Returns:
            Markdown lines.
        """
        # Section lines preserve required ADR review headings.
        lines: list[str] = []
        lines.extend(["## Status", "", str(record["status"]), ""])
        lines.extend(["## Context", "", str(record["context"]), ""])
        lines.extend(["## Decision", "", str(record["decision"]), ""])
        lines.extend(["## Consequences", "", str(record["consequences"]), ""])
        lines.extend(["## architecture-spec", "", str(record["architecture_spec"]), ""])
        lines.extend(self.render_list("acceptance-criteria", record["acceptance_criteria"]))
        lines.extend(["## implementation-brief", "", str(record["implementation_brief"]), ""])
        lines.extend(self.render_list("resolved_open_questions", record["resolved_open_questions"]))
        lines.extend(self.render_list("non_goals", record["non_goals"]))
        lines.extend(self.render_list("validation_expectations", record["validation_expectations"]))
        lines.extend(["## routing", "", str(record["routing"]), ""])
        lines.extend(["## links", "", str(record["links"]), ""])
        return lines

    def render_list(self, heading: str, value: object) -> list[str]:
        """Render a JSON array section as Markdown bullets.

        Args:
            heading: Section heading.
            value: JSON array value.

        Returns:
            Markdown lines.
        """
        if not isinstance(value, list):
            raise AdrMarkdownError(f"Expected list for section: {heading}")
        # Bullet lines preserve array order.
        lines: list[str] = [f"## {heading}", ""]
        item: object
        for item in value:
            lines.append(f"- {item}")
        lines.append("")
        return lines
