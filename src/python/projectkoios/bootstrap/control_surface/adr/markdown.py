"""Small Markdown helpers for the one-ADR storage pilot.

This module is not a general ADR Markdown importer. It reads the pilot source
ADR Markdown file, reads the generated projection's embedded JSON block, and
renders the generated projection used as pilot evidence.
"""

from __future__ import annotations

import re
from re import Pattern

from projectkoios.bootstrap.control_surface.adr.models import PilotAdrSourceConfig
from projectkoios.bootstrap.schema import SchemaRegistry
from projectkoios.bootstrap.schema.models import JsonObject


class AdrMarkdownError(ValueError):
    """Raised when ADR Markdown cannot be parsed."""


class AdrMarkdownRecordParser:
    """Parse ADR Markdown into ADR JSON records.

    This parser reads the pilot source ADR and generated projection file. It is
    intentionally narrow and does not try to import arbitrary ADR Markdown.

    Args:
        source_config: Source ADR values used by the one-ADR pilot.
        schema_registry: Loads `adr.schema.json`.
    """

    def __init__(
        self,
        source_config: PilotAdrSourceConfig | None = None,
        schema_registry: SchemaRegistry | None = None,
    ) -> None:
        """Initialize the ADR record parser.

        Args:
            source_config: Source ADR values used by the one-ADR pilot.
            schema_registry: Loads `adr.schema.json`.
        """
        # Source config keeps pilot-specific values out of parser logic.
        self.source_config: PilotAdrSourceConfig = source_config or PilotAdrSourceConfig()
        # The parser uses the schema to know which sections to require.
        self.schema_registry: SchemaRegistry = schema_registry or SchemaRegistry()

    def parse_source_record(self, markdown: str) -> tuple[JsonObject, JsonObject]:
        """Parse source Markdown into an ADR JSON record.

        Args:
            markdown: Source Markdown text.

        Returns:
            ADR record and notes about copied/changed fields.
        """
        # Split the Markdown before reading individual fields.
        sections: dict[str, str] = self.sections(markdown)
        # The title lives in the top-level `# ADR ...` heading.
        title: str = self.title(markdown)
        # Context is a small key-value section.
        context: JsonObject = self.context(sections[self.section_key_for_schema_field("context")])
        # Links is a small key-value section.
        links: JsonObject = self.links(sections[self.section_key_for_schema_field("links")])
        # The JSON record follows `docs/schemas/adr.schema.json`.
        record: JsonObject = {
            "id": self.source_config.record_id,
            "slug": self.source_config.slug,
            "title": title,
            "status": self.status(sections[self.section_key_for_schema_field("status")]),
            "context": context,
            "decision": sections[self.section_key_for_schema_field("decision")],
            "consequences": sections[self.section_key_for_schema_field("consequences")],
            "architecture_spec": sections[self.section_key_for_schema_field("architecture_spec")],
            "acceptance_criteria": self.bullets(sections[self.section_key_for_schema_field("acceptance_criteria")]),
            "implementation_brief": sections[self.section_key_for_schema_field("implementation_brief")],
            "resolved_open_questions": self.bullets(sections[self.section_key_for_schema_field("resolved_open_questions")]),
            "non_goals": self.bullets(sections[self.section_key_for_schema_field("non_goals")]),
            "validation_expectations": self.bullets(sections[self.section_key_for_schema_field("validation_expectations")]),
            "links": links,
        }
        # Notes explain values that were copied, normalized, or kept outside the record.
        source_notes: JsonObject = self.source_mapping_notes(sections, legacy_title_heading=self.legacy_title_heading(markdown))
        return record, source_notes

    def parse_projection_record(self, markdown: str) -> JsonObject:
        """Parse generated projection Markdown back to ADR JSON.

        Args:
            markdown: Generated projection Markdown.

        Returns:
            ADR record contained in the projection.
        """
        # The generated projection embeds the record in a fenced JSON block.
        start_marker: str = "```json adr-record"
        # End marker closes the embedded ADR record JSON block.
        end_marker: str = "```"
        # Find the embedded JSON record.
        start_index: int = markdown.find(start_marker)
        if start_index < 0:
            raise AdrMarkdownError("Projection missing ADR record JSON fence")
        # Skip the fence marker itself.
        json_start: int = start_index + len(start_marker)
        # Find the closing fence.
        end_index: int = markdown.find(end_marker, json_start)
        if end_index < 0:
            raise AdrMarkdownError("Projection ADR record JSON fence is unclosed")
        import json
        # Parse only the text inside the fence.
        payload: object = json.loads(markdown[json_start:end_index].strip())
        if not isinstance(payload, dict):
            raise AdrMarkdownError("Projection ADR record payload must be an object")
        return payload

    def title(self, markdown: str) -> str:
        """Return the ADR title from the top heading.

        Args:
            markdown: Source Markdown text.

        Returns:
            ADR title.
        """
        # First line must be a supported source title heading.
        first_line: str = markdown.splitlines()[0]
        # Stable headings omit lifecycle/date material from the title line.
        stable_prefix: str = "# ADR: "
        if first_line.startswith(stable_prefix):
            return first_line.removeprefix(stable_prefix).strip()
        # Legacy headings may include timestamp/status text before the title colon.
        legacy_match: re.Match[str] | None = re.match(r"^# ADR\s+[^:]+:\s*(?P<title>.+?)\s*$", first_line)
        if legacy_match is None:
            raise AdrMarkdownError("Source ADR missing title heading")
        return legacy_match.group("title")

    def sections(self, markdown: str) -> dict[str, str]:
        """Split Markdown into `##` sections.

        Args:
            markdown: Source Markdown text.

        Returns:
            Section name to section body.
        """
        # Work line-by-line so headings define section boundaries.
        lines: list[str] = markdown.splitlines()
        # Sections are collected under their normalized heading names.
        sections: dict[str, list[str]] = {}
        # Current key names the section receiving following lines.
        current_key: str | None = None
        line: str
        for line in lines[1:]:
            # A `##` line starts a new section.
            match: re.Match[str] | None = self.section_heading_pattern().match(line)
            if match is not None:
                current_key = self.section_key(match.group("heading"))
                sections[current_key] = []
                continue
            if current_key is not None:
                sections[current_key].append(line)
        # Join each section body back into text.
        normalized: dict[str, str] = {key: "\n".join(value).strip() for key, value in sections.items()}
        # Fail early if the source lacks a required section.
        missing: list[str] = [key for key in self.required_section_keys() if key not in normalized]
        if missing:
            raise AdrMarkdownError(f"Source ADR missing sections: {', '.join(missing)}")
        return normalized

    def section_heading_pattern(self) -> Pattern[str]:
        """Return the pattern for `##` headings.

        Returns:
            Compiled heading pattern.
        """
        return re.compile(r"^## (?P<heading>.+)$")

    def required_section_keys(self) -> tuple[str, ...]:
        """Return Markdown sections required for the source ADR.

        Returns:
            Required section names.
        """
        # The schema defines required ADR fields. Title comes from the H1 heading.
        required_fields: tuple[str, ...] = self.required_schema_fields()
        # The schema-required fields map to same-named Markdown sections, except
        # for a few legacy source headings handled by `section_key_for_schema_field`.
        # Links is optional in the schema but preserved because this source file has it.
        source_fields: list[str] = [field_name for field_name in required_fields if field_name != "title"]
        if "links" not in source_fields:
            source_fields.append("links")
        return tuple(self.section_key_for_schema_field(field_name) for field_name in source_fields)

    def required_schema_fields(self) -> tuple[str, ...]:
        """Return required top-level fields from `adr.schema.json`.

        Returns:
            Required schema field names.
        """
        # Load the schema instead of duplicating its required field list here.
        schema: JsonObject = self.schema_registry.load_schema("adr.schema.json")
        # Validate the raw `required` value before using it.
        required_value: object = schema.get("required", [])
        if not isinstance(required_value, list):
            raise AdrMarkdownError("ADR schema required fields must be an array")
        # Copy field names into a typed list.
        required_fields: list[str] = []
        field_name: object
        for field_name in required_value:
            if not isinstance(field_name, str):
                raise AdrMarkdownError("ADR schema required field names must be strings")
            required_fields.append(field_name)
        return tuple(required_fields)

    def section_key_for_schema_field(self, field_name: str) -> str:
        """Return the Markdown section name for a schema field.

        Args:
            field_name: Top-level schema field name.

        Returns:
            Markdown section name.
        """
        # These source headings use hyphens instead of underscores.
        legacy_hyphen_fields: set[str] = {"architecture_spec", "acceptance_criteria", "implementation_brief"}
        if field_name in legacy_hyphen_fields:
            return field_name.replace("_", "-")
        return field_name

    def section_key(self, heading: str) -> str:
        """Normalize a Markdown heading.

        Args:
            heading: Markdown heading text.

        Returns:
            Normalized section name.
        """
        return heading.strip().lower().replace(" ", "_").replace("-", "-")

    def status(self, body: str) -> str:
        """Return the value from the Status section.

        Args:
            body: Status section body.

        Returns:
            ADR status.
        """
        # First non-empty line is the status value.
        lines: list[str] = [line.strip() for line in body.splitlines() if line.strip()]
        if not lines:
            raise AdrMarkdownError("Status section is empty")
        return lines[0]

    def context(self, body: str) -> JsonObject:
        """Read the Context section.

        Args:
            body: Context section body.

        Returns:
            Context JSON object.
        """
        # The source stores context values as `Key: value` lines.
        values: dict[str, str] = self.key_values(body)
        return {
            "origin": values["Origin"],
            "from": values["From"],
            "acting_as": values["Acting-As"],
            "scope": values["Scope"],
            "repository": values["Repository"],
            "delegated_operator": values.get("Delegated-Operator", self.source_config.delegated_operator),
            "architecture_domain": values["Architecture-Domain"],
        }

    def links(self, body: str) -> JsonObject:
        """Read the Links section.

        Args:
            body: Links section body.

        Returns:
            Links JSON object.
        """
        # The source uses the string `None` for empty links.
        values: dict[str, str] = self.key_values(body)
        return {
            "back_to": values["back_to"],
            "supersedes": self.none_value(values["supersedes"]),
            "superseded_by": self.none_value(values["superseded_by"]),
        }

    def related_links(self, body: str) -> list[JsonObject]:
        """Read related links preserved outside the schema record.

        Args:
            body: Links section body.

        Returns:
            Related link evidence entries.
        """
        # `links.related` is not in the ADR schema, so preserve it as sidecar evidence.
        values: dict[str, str] = self.key_values(body)
        # Related link text is source-only evidence because schema links exclude it.
        related: str | None = values.get("related")
        if related is None:
            return []
        # The current source form is `[label](path)`.
        match: re.Match[str] | None = re.match(r"^\[(?P<label>.+)]\((?P<path>.+)\)$", related)
        if match is None:
            return [{"raw": related}]
        return [{"label": match.group("label"), "path": match.group("path")}]

    def key_values(self, body: str) -> dict[str, str]:
        """Parse `Key: value` lines.

        Args:
            body: Section body.

        Returns:
            Key-value pairs.
        """
        # Ignore prose and bullet lines that are not key-value pairs.
        values: dict[str, str] = {}
        line: str
        for line in body.splitlines():
            # Some key-value lines are written as bullets.
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
        """Return bullet text from a section.

        Args:
            body: Section body.

        Returns:
            Bullet text values.
        """
        # Bullet sections become JSON arrays.
        values: list[str] = []
        line: str
        for line in body.splitlines():
            if line.startswith("- "):
                values.append(line.removeprefix("- ").strip())
        if not values:
            raise AdrMarkdownError("Expected at least one bullet value")
        return values

    def none_value(self, value: str) -> str | None:
        """Convert textual `None` to JSON null.

        Args:
            value: Source value.

        Returns:
            Source value or None.
        """
        if value == "None":
            return None
        return value

    def legacy_title_heading(self, markdown: str) -> bool:
        """Return true when source heading uses the legacy prefixed ADR form.

        Args:
            markdown: Source Markdown text.

        Returns:
            True when a legacy prefix before the title was parsed.
        """
        # First source line determines heading compatibility mode.
        first_line: str = markdown.splitlines()[0]
        return bool(re.match(r"^# ADR\s+[^:]+:\s*.+$", first_line))

    def normalized_fields(self, *, legacy_title_heading: bool) -> JsonObject:
        """Return source-to-record normalization notes.

        Args:
            legacy_title_heading: True when legacy heading prefix was stripped.

        Returns:
            Normalization notes keyed by transformed source surface.
        """
        # Stable headings require no legacy heading stripping note.
        normalized: JsonObject = {
            "context_labels": "converted source labels to schema snake_case keys",
            "none_links": "converted textual None values to JSON null",
            "bullet_sections": "converted Markdown bullets to JSON arrays",
        }
        if legacy_title_heading:
            normalized["legacy_title_heading"] = "removed legacy ADR heading prefix before title"
        return normalized

    def source_mapping_notes(self, sections: dict[str, str], *, legacy_title_heading: bool) -> JsonObject:
        """Return notes about how the source file became JSON.

        Args:
            sections: Parsed source sections.
            legacy_title_heading: True when legacy heading prefix was stripped.

        Returns:
            Source conversion notes.
        """
        # Context values drive both schema fields and provenance notes.
        context_values: dict[str, str] = self.key_values(sections[self.section_key_for_schema_field("context")])
        # Inferred fields document parser-supplied values when source fields are absent.
        inferred_fields: JsonObject = {}
        if "Delegated-Operator" not in context_values:
            inferred_fields["context.delegated_operator"] = self.source_config.delegated_operator
        # Routing values are preserved outside the schema after routing removal.
        routing_values: dict[str, str] = self.key_values(sections.get("routing", ""))
        return {
            "status": "pilot-derived-non-authoritative",
            "source_path": self.source_config.source_path,
            "source_filename_status_suffix": self.source_config.legacy_filename_status_suffix,
            "canonical_identity_rule": "status-free id and slug; lifecycle status lives in record content",
            "canonical_id": self.source_config.record_id,
            "canonical_slug": self.source_config.slug,
            "record_status": self.status(sections[self.section_key_for_schema_field("status")]),
            "copied_fields": [
                "title",
                "status",
                "context.origin",
                "context.from",
                "context.acting_as",
                "context.scope",
                "context.repository",
                "context.delegated_operator",
                "context.architecture_domain",
                "decision",
                "consequences",
                "architecture_spec",
                "acceptance_criteria",
                "implementation_brief",
                "resolved_open_questions",
                "non_goals",
                "validation_expectations",
                "links.back_to",
                "links.supersedes",
                "links.superseded_by",
            ],
            "inferred_fields": inferred_fields,
            "normalized_fields": self.normalized_fields(legacy_title_heading=legacy_title_heading),
            "preserved_outside_schema": {
                "source_date": self.source_config.source_date,
                "routing_section": sections.get("routing", ""),
                "routing": {
                    "owner": routing_values.get("Owner"),
                    "next_phase": routing_values.get("Next phase"),
                    "notes": routing_values.get("Notes"),
                },
                "links.related": self.related_links(sections[self.section_key_for_schema_field("links")]),
            },
        }


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
        # Metadata lines make projection authority boundaries visible to reviewers.
        status_block: object = manifest.get("pilot")
        if not isinstance(status_block, dict):
            status_block = manifest.get("conformance")
        if not isinstance(status_block, dict):
            status_block = {}
        # Run status labels the projection's generating workflow.
        run_status: str = str(status_block.get("status", "generated-projection"))
        # Lines are assembled deterministically for stable projection diffs.
        lines: list[str] = [
            "<!-- GENERATED PILOT PROJECTION: non-authoritative; do not edit as ADR authority. -->",
            f"# ADR Projection: {record['title']}",
            "",
            "## Projection metadata",
            "",
            f"- Projection status: {run_status}",
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
