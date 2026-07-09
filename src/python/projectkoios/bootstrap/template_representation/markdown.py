from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from re import Pattern

from projectkoios.bootstrap.schema import SchemaRegistry
from projectkoios.bootstrap.template_representation.models import JsonObject, TemplateMarker, TemplateRecord, TemplateSection
from projectkoios.bootstrap.template_representation.paths import TemplateRepresentationPaths


class TemplateMarkdownError(ValueError):
    """Raised when controlled template Markdown cannot be represented losslessly."""


MARKER_PATTERN: Pattern[str] = re.compile(r"<[^>\n]+>")
"""Deterministic first-slice placeholder marker pattern."""


@dataclass(frozen=True, slots=True)
class TemplateMarkdownParser:
    """Parse controlled bootstrap template Markdown into canonical representation.

    Args:
        paths: Template representation path helper.
    """

    paths: TemplateRepresentationPaths = TemplateRepresentationPaths()
    schema_registry: SchemaRegistry = SchemaRegistry()

    def parse_file(self, path: Path, *, allow_test_fixture: bool = False) -> TemplateRecord:
        """Parse a template Markdown file into canonical representation.

        Args:
            path: Markdown template path.
            allow_test_fixture: Whether non-template paths are allowed for tests.

        Returns:
            Canonical template record.
        """

        # Source path is validated before reading so namespace errors are explicit.
        source_path: str = self.paths.ensure_template_path(path, allow_test_fixture=allow_test_fixture)
        # Markdown text is read from the controlled fixture file.
        markdown: str = path.read_text(encoding="utf-8")
        return self.parse(markdown, source_path=source_path)

    def parse_file_schema_record(
        self,
        path: Path,
        *,
        created_on: str,
        allow_test_fixture: bool = False,
    ) -> JsonObject:
        """Parse a template Markdown file into a validated schema-backed record.

        Args:
            path: Markdown template path.
            created_on: Deterministic schema record creation timestamp.
            allow_test_fixture: Whether non-template paths are allowed for tests.

        Returns:
            Validated schema-backed template record instance.
        """

        # Parsed template record is the source for the schema-backed envelope.
        record: TemplateRecord = self.parse_file(path, allow_test_fixture=allow_test_fixture)
        # Schema-backed record is the authoritative parsed output for this slice.
        schema_record: JsonObject = record.to_schema_record(created_on=created_on)
        self.schema_registry.validate("template-record.schema.json", schema_record)
        return schema_record

    def parse_schema_record(self, markdown: str, *, source_path: str, created_on: str) -> JsonObject:
        """Parse controlled Markdown into a validated schema-backed record.

        Args:
            markdown: Markdown template text.
            source_path: Repository-relative source path.
            created_on: Deterministic schema record creation timestamp.

        Returns:
            Validated schema-backed template record instance.
        """

        # Parsed template record is converted into the schema-backed envelope.
        record: TemplateRecord = self.parse(markdown, source_path=source_path)
        # Schema validation distinguishes schema failures from Markdown parse failures.
        schema_record: JsonObject = record.to_schema_record(created_on=created_on)
        self.schema_registry.validate("template-record.schema.json", schema_record)
        return schema_record

    def parse(self, markdown: str, *, source_path: str) -> TemplateRecord:
        """Parse controlled Markdown into canonical representation.

        Args:
            markdown: Markdown template text.
            source_path: Repository-relative source path.

        Returns:
            Canonical template record.

        Raises:
            TemplateMarkdownError: If Markdown cannot be represented deterministically.
        """

        # Markdown lines preserve heading and body structure for parsing.
        lines: list[str] = markdown.splitlines()
        # Title line index identifies the single supported top-level heading.
        title_index: int = self.find_title_index(lines)
        # Preamble preserves controlled text before the top-level heading.
        preamble: str = self.normalize_body("\n".join(lines[:title_index]))
        # Title text is the top-level heading without the Markdown marker.
        title: str = lines[title_index].removeprefix("# ").strip()
        if not title:
            raise TemplateMarkdownError("Template title must not be empty")
        # Section start lines identify ordered second-level sections.
        section_starts: list[int] = self.find_section_starts(lines, start=title_index + 1)
        if not section_starts:
            raise TemplateMarkdownError("Template must contain at least one second-level section")
        # Lead body preserves controlled prose between title and first section.
        lead_body: str = self.normalize_body("\n".join(lines[title_index + 1:section_starts[0]]))
        # Parsed sections preserve source order.
        sections: list[TemplateSection] = []
        section_number: int
        section_start: int
        for section_number, section_start in enumerate(section_starts):
            # Section end is either next section start or end of document.
            section_end: int = section_starts[section_number + 1] if section_number + 1 < len(section_starts) else len(lines)
            sections.append(self.parse_section(lines, section_start, section_end))
        # Document markers include preamble, title, and lead body markers.
        document_text: str = "\n".join([preamble, title, lead_body])
        # Template identifier comes from the source filename.
        template_id: str = self.paths.template_id(source_path)
        return TemplateRecord(
            template_id=template_id,
            source_path=source_path,
            title=title,
            sections=tuple(sections),
            markers=self.detect_markers(document_text, "document"),
            preamble=preamble,
            lead_body=lead_body,
        )

    def find_title_index(self, lines: list[str]) -> int:
        """Return the single top-level heading index.

        Args:
            lines: Markdown lines.

        Returns:
            Index of the supported title heading.

        Raises:
            TemplateMarkdownError: If title heading is missing or ambiguous.
        """

        # Top-level heading indexes are collected to reject ambiguous titles.
        title_indexes: list[int] = [index for index, line in enumerate(lines) if line.startswith("# ")]
        if not title_indexes:
            raise TemplateMarkdownError("Missing required top-level template heading")
        if len(title_indexes) > 1:
            raise TemplateMarkdownError("Ambiguous multiple top-level template headings")
        return title_indexes[0]

    def find_section_starts(self, lines: list[str], *, start: int) -> list[int]:
        """Return second-level section start indexes.

        Args:
            lines: Markdown lines.
            start: First line to inspect.

        Returns:
            Ordered second-level section indexes.

        Raises:
            TemplateMarkdownError: If a heading level would change section identity.
        """

        # Section starts are second-level headings after the title.
        starts: list[int] = []
        # Seen headings prevent duplicate section identity in the first slice.
        seen_headings: set[str] = set()
        index: int
        for index in range(start, len(lines)):
            # Current line may be a heading or body content.
            line: str = lines[index]
            if line.startswith("# "):
                raise TemplateMarkdownError("Top-level heading is only allowed once")
            if line.startswith("## ") and not line.startswith("### "):
                # Heading text identifies the template section.
                heading: str = line.removeprefix("## ").strip()
                if not heading:
                    raise TemplateMarkdownError("Section heading must not be empty")
                if heading in seen_headings:
                    raise TemplateMarkdownError(f"Duplicate section heading: {heading}")
                seen_headings.add(heading)
                starts.append(index)
                continue
            if line.startswith("####"):
                raise TemplateMarkdownError("Ambiguous heading depth below supported subsection level")
        return starts

    def parse_section(self, lines: list[str], start: int, end: int) -> TemplateSection:
        """Parse one second-level template section.

        Args:
            lines: Markdown lines.
            start: Section heading index.
            end: Exclusive section end index.

        Returns:
            Template section representation.
        """

        # Section heading has already been validated by section discovery.
        heading: str = lines[start].removeprefix("## ").strip()
        # Section body preserves supported nested headings and prose.
        body: str = self.normalize_body("\n".join(lines[start + 1:end]))
        return TemplateSection(heading=heading, body=body, markers=self.detect_markers(body, f"section:{heading}"))

    def detect_markers(self, text: str, location: str) -> tuple[TemplateMarker, ...]:
        """Detect deterministic first-slice template markers in text.

        Args:
            text: Text to inspect.
            location: Marker source location.

        Returns:
            Ordered unique marker tuple.
        """

        # Marker strings preserve first-seen order while deduplicating repeats.
        markers: list[TemplateMarker] = []
        # Seen marker strings prevent duplicate marker records in one location.
        seen: set[str] = set()
        match: re.Match[str]
        for match in MARKER_PATTERN.finditer(text):
            # Matched marker is a deterministic angle-bracket placeholder.
            marker: str = match.group(0)
            if marker not in seen:
                seen.add(marker)
                markers.append(TemplateMarker(marker=marker, location=location))
        return tuple(markers)

    def normalize_body(self, body: str) -> str:
        """Normalize presentation-only whitespace in Markdown body text.

        Args:
            body: Raw Markdown body text.

        Returns:
            Body with trailing spaces removed and surrounding blank lines trimmed.
        """

        # Lines are stripped only on the right to preserve meaningful indentation.
        lines: list[str] = [line.rstrip() for line in body.splitlines()]
        while lines and not lines[0].strip():
            del lines[0]
        while lines and not lines[-1].strip():
            lines.pop()
        return "\n".join(lines)


@dataclass(frozen=True, slots=True)
class TemplateMarkdownRenderer:
    """Render canonical template records as deterministic Markdown."""

    def render_schema_record(self, schema_record: JsonObject) -> str:
        """Render a schema-backed template record into deterministic Markdown.

        Args:
            schema_record: Schema-backed template record instance.

        Returns:
            Deterministic Markdown text.
        """

        # TemplateRecord provides the canonical renderable content model.
        record: TemplateRecord = TemplateRecord.from_schema_record(schema_record)
        return self.render(record)

    def render(self, record: TemplateRecord) -> str:
        """Render a template record into deterministic Markdown.

        Args:
            record: Canonical template record.

        Returns:
            Deterministic Markdown text.
        """

        # Output lines are accumulated in canonical document order.
        lines: list[str] = []
        if record.preamble.strip():
            lines.extend(record.preamble.strip().splitlines())
            lines.append("")
        lines.append(f"# {record.title}")
        if record.lead_body.strip():
            lines.extend(["", *record.lead_body.strip().splitlines()])
        section: TemplateSection
        for section in record.sections:
            lines.extend(["", f"## {section.heading}"])
            if section.body.strip():
                lines.extend(["", *section.body.strip().splitlines()])
        return "\n".join(lines).rstrip() + "\n"
