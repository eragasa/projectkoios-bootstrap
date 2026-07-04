from __future__ import annotations

from dataclasses import dataclass
import json

from projectkoios.bootstrap.schemas.models import (
    CONCERN_LEVEL_ORDER,
    DRAFT_ADR_SECTION_FIELDS,
    DRAFT_ADR_SECTION_HEADINGS,
    Concern,
    ConcernLevel,
    DraftAdrRecord,
    JsonObject,
    RejectedMarkdown,
    Section,
)


class MarkdownIngestError(ValueError):
    """Raised when controlled draft ADR Markdown cannot be ingested."""


@dataclass(frozen=True, slots=True)
class DraftAdrMarkdownRenderer:
    """Render draft ADR records into controlled Markdown projections."""

    def render(self, record: DraftAdrRecord) -> str:
        """Render a draft ADR record as deterministic Markdown.

        Args:
            record: Draft ADR record to render.

        Returns:
            Controlled Markdown projection text.
        """
        # Metadata block is projected without changing schema-owned fields.
        metadata: JsonObject = record.metadata.to_dict()
        # Output lines are accumulated in deterministic render order.
        lines: list[str] = [f"# ADR: {metadata['title']}", "", "```json"]
        lines.extend(json.dumps(metadata, indent=2, sort_keys=True).splitlines())
        lines.extend(["```", ""])
        field: str
        for field in DRAFT_ADR_SECTION_FIELDS:
            # Section content is rendered in schema-defined order.
            section: Section = record.content.sections[field]
            lines.extend(self.render_section(section, level=2))
        if record.content.rejected:
            lines.extend(["## Rejected", ""])
            rejected: RejectedMarkdown
            for rejected in record.content.rejected:
                lines.extend([
                    f"### {rejected.heading}",
                    "",
                    f"Reason: {rejected.reason}",
                    "",
                    "```text",
                    rejected.body,
                    "```",
                    "",
                ])
        return "\n".join(lines).rstrip() + "\n"

    def render_section(self, section: Section, *, level: int) -> list[str]:
        """Render one draft ADR section.

        Args:
            section: Section to render.
            level: Markdown heading depth.

        Returns:
            Markdown lines for the section.
        """
        # Heading prefix controls Markdown section depth.
        heading_prefix: str = "#" * level
        # Section lines start with heading, description, and concern marker.
        lines: list[str] = [f"{heading_prefix} {section.heading}", "", section.description, "", "### Concern"]
        # Concerns are sorted into normative keyword order.
        sorted_concerns: list[Concern] = sorted(section.concerns, key=lambda concern: CONCERN_LEVEL_ORDER.index(concern.level))
        concern: Concern
        for concern in sorted_concerns:
            lines.append(f"- {concern.level.value} {concern.text}")
        lines.append("")
        subsection: Section
        for subsection in section.subsections:
            lines.extend(self.render_section(subsection, level=level + 1))
        return lines


@dataclass(frozen=True, slots=True)
class DraftAdrMarkdownIngester:
    """Ingest controlled draft ADR Markdown into schema-shaped data."""

    def ingest(self, markdown: str) -> JsonObject:
        """Ingest controlled draft ADR Markdown.

        Args:
            markdown: Markdown projection text.

        Returns:
            Schema-shaped draft ADR record data.

        Raises:
            MarkdownIngestError: If Markdown cannot be mapped deterministically.
        """
        # Input lines preserve Markdown structure for deterministic parsing.
        lines: list[str] = markdown.splitlines()
        metadata: JsonObject
        body_start: int
        metadata, body_start = self.parse_metadata(lines)
        # Parsed content is constrained by the draft ADR schema surface.
        content: JsonObject = self.parse_content(lines[body_start:])
        return {"metadata": metadata, "content": content}

    def parse_metadata(self, lines: list[str]) -> tuple[JsonObject, int]:
        """Parse the title and metadata JSON block.

        Args:
            lines: Markdown lines.

        Returns:
            Metadata mapping and body start index.

        Raises:
            MarkdownIngestError: If metadata is missing or invalid.
        """
        if not lines or not lines[0].startswith("# ADR: "):
            raise MarkdownIngestError("Missing ADR title heading")
        # Opening JSON fence begins the metadata block.
        fence_start: int | None = self.find_line(lines, "```json", start=1)
        if fence_start is None:
            raise MarkdownIngestError("Missing metadata JSON block")
        # Closing fence ends the metadata block.
        fence_end: int | None = self.find_line(lines, "```", start=fence_start + 1)
        if fence_end is None:
            raise MarkdownIngestError("Unclosed metadata JSON block")
        error: json.JSONDecodeError
        try:
            # Metadata payload is parsed as JSON before schema validation.
            metadata: object = json.loads("\n".join(lines[fence_start + 1:fence_end]))
        except json.JSONDecodeError as error:
            raise MarkdownIngestError(f"Invalid metadata JSON: {error}") from error
        if not isinstance(metadata, dict):
            raise MarkdownIngestError("Metadata JSON must be an object")
        # Heading title must match schema-owned metadata title.
        title: str = lines[0].removeprefix("# ADR: ")
        if metadata.get("title") != title:
            raise MarkdownIngestError("Title heading must match metadata.title")
        return metadata, fence_end + 1

    def parse_content(self, lines: list[str]) -> JsonObject:
        """Parse controlled draft ADR content sections.

        Args:
            lines: Markdown body lines after the metadata block.

        Returns:
            Draft ADR content mapping.

        Raises:
            MarkdownIngestError: If required content cannot be mapped.
        """
        # Parsed sections are keyed by draft ADR schema field name.
        sections: JsonObject = {}
        # Current parser index advances through required sections.
        index: int = self.skip_blank(lines, 0)
        field: str
        for field in DRAFT_ADR_SECTION_FIELDS:
            # Expected heading comes from the schema field order.
            expected_heading: str = DRAFT_ADR_SECTION_HEADINGS[field]
            section: JsonObject
            section, index = self.parse_required_section(lines, index, expected_heading)
            sections[field] = section
            index = self.skip_blank(lines, index)
        # Rejected entries capture deterministic extra content.
        rejected: list[dict[str, str]] = []
        while index < len(lines):
            if lines[index].startswith("####"):
                raise MarkdownIngestError("Ambiguous heading depth")
            if lines[index] == "## Rejected":
                captured: list[dict[str, str]]
                captured, index = self.parse_rendered_rejected(lines, index + 1)
                rejected.extend(captured)
                index = self.skip_blank(lines, index)
                continue
            if lines[index].startswith("## "):
                # Extra section heading is captured under rejected content.
                heading: str = lines[index].removeprefix("## ")
                # Body begins after the rejected heading.
                body_start: int = index + 1
                index = self.next_top_heading(lines, body_start)
                rejected.append({
                    "heading": heading,
                    "reason": "extra_section",
                    "body": "\n".join(lines[body_start:index]).strip(),
                })
                index = self.skip_blank(lines, index)
                continue
            if lines[index].strip():
                raise MarkdownIngestError(f"Unexpected content outside a section: {lines[index]}")
            index += 1
        sections["rejected"] = rejected
        return sections

    def parse_required_section(self, lines: list[str], index: int, expected_heading: str) -> tuple[JsonObject, int]:
        """Parse one required draft ADR section.

        Args:
            lines: Markdown lines.
            index: Current parser index.
            expected_heading: Required section heading.

        Returns:
            Parsed section mapping and next parser index.

        Raises:
            MarkdownIngestError: If the section is missing or malformed.
        """
        if index >= len(lines) or lines[index] != f"## {expected_heading}":
            raise MarkdownIngestError(f"Missing or out-of-order section: {expected_heading}")
        index += 1
        # Description lines precede the section concern block.
        description_lines: list[str] = []
        while index < len(lines) and lines[index] != "### Concern":
            if lines[index].startswith("####"):
                raise MarkdownIngestError("Ambiguous heading depth")
            if lines[index].startswith("## "):
                raise MarkdownIngestError(f"Missing Concern block for section: {expected_heading}")
            description_lines.append(lines[index])
            index += 1
        if index >= len(lines):
            raise MarkdownIngestError(f"Missing Concern block for section: {expected_heading}")
        # Description is normalized by trimming surrounding blank lines.
        description: str = "\n".join(description_lines).strip()
        if len(description) > 600:
            raise MarkdownIngestError(f"Section description exceeds 600 characters: {expected_heading}")
        index += 1
        # Parsed concerns preserve section-local concern order.
        concerns: list[dict[str, str]] = []
        while index < len(lines) and not lines[index].startswith("## "):
            # Current line may be a concern or blank separator.
            line: str = lines[index]
            if line.startswith("####"):
                raise MarkdownIngestError("Ambiguous heading depth")
            if line.startswith("### "):
                raise MarkdownIngestError(f"Unsupported subsection in first slice: {line}")
            if line.strip():
                concerns.append(self.parse_concern(line))
            index += 1
        return {
            "heading": expected_heading,
            "description": description,
            "concerns": concerns,
        }, index

    def parse_concern(self, line: str) -> dict[str, str]:
        """Parse one normative concern line.

        Args:
            line: Markdown concern line.

        Returns:
            Schema-shaped concern mapping.

        Raises:
            MarkdownIngestError: If the concern syntax is malformed.
        """
        if not line.startswith("- "):
            raise MarkdownIngestError(f"Malformed concern line: {line}")
        # Concern text without the Markdown bullet marker.
        text: str = line.removeprefix("- ")
        level: ConcernLevel
        for level in (ConcernLevel.MUST_NOT, ConcernLevel.SHOULD_NOT, ConcernLevel.MUST, ConcernLevel.SHOULD, ConcernLevel.MAY):
            # Prefix includes trailing whitespace after the normative keyword.
            prefix: str = f"{level.value} "
            if text.startswith(prefix):
                # Concern text excludes the normative keyword prefix.
                concern_text: str = text.removeprefix(prefix)
                if not concern_text:
                    raise MarkdownIngestError(f"Empty concern text: {line}")
                return {"level": level.value, "text": concern_text}
        raise MarkdownIngestError(f"Malformed concern keyword: {line}")

    def parse_rendered_rejected(self, lines: list[str], index: int) -> tuple[list[dict[str, str]], int]:
        """Parse a rendered rejected-content block.

        Args:
            lines: Markdown lines.
            index: Current parser index after `## Rejected`.

        Returns:
            Rejected entries and next parser index.

        Raises:
            MarkdownIngestError: If rejected content syntax is malformed.
        """
        # Rejected entries mirror renderer output.
        rejected: list[dict[str, str]] = []
        index = self.skip_blank(lines, index)
        while index < len(lines) and not lines[index].startswith("## "):
            if not lines[index].startswith("### "):
                raise MarkdownIngestError("Rendered rejected content must use ### headings")
            # Rejected heading is the original out-of-contract heading.
            heading: str = lines[index].removeprefix("### ")
            index = self.skip_blank(lines, index + 1)
            if index >= len(lines) or not lines[index].startswith("Reason: "):
                raise MarkdownIngestError("Rendered rejected content missing reason")
            # Rejection reason is emitted by renderer or ingester.
            reason: str = lines[index].removeprefix("Reason: ")
            index = self.skip_blank(lines, index + 1)
            if index >= len(lines) or lines[index] != "```text":
                raise MarkdownIngestError("Rendered rejected content missing text fence")
            # Closing fence marks the end of rejected body text.
            fence_end: int | None = self.find_line(lines, "```", start=index + 1)
            if fence_end is None:
                raise MarkdownIngestError("Unclosed rejected text fence")
            # Body preserves rejected content inside the text fence.
            body: str = "\n".join(lines[index + 1:fence_end])
            rejected.append({"heading": heading, "reason": reason, "body": body})
            index = self.skip_blank(lines, fence_end + 1)
        return rejected, index

    def find_line(self, lines: list[str], target: str, *, start: int) -> int | None:
        """Find a line exactly matching a target string.

        Args:
            lines: Lines to scan.
            target: Exact target line.
            start: Starting index.

        Returns:
            Matching index, or None when absent.
        """
        index: int
        for index in range(start, len(lines)):
            if lines[index] == target:
                return index
        return None

    def skip_blank(self, lines: list[str], index: int) -> int:
        """Skip blank Markdown lines.

        Args:
            lines: Lines to scan.
            index: Starting index.

        Returns:
            First non-blank index or end index.
        """
        while index < len(lines) and not lines[index].strip():
            index += 1
        return index

    def next_top_heading(self, lines: list[str], index: int) -> int:
        """Find the next top-level section heading for parser recovery.

        Args:
            lines: Lines to scan.
            index: Starting index.

        Returns:
            Index of next `##` heading or end index.

        Raises:
            MarkdownIngestError: If ambiguous heading depth appears.
        """
        while index < len(lines) and not lines[index].startswith("## "):
            if lines[index].startswith("####"):
                raise MarkdownIngestError("Ambiguous heading depth")
            index += 1
        return index
