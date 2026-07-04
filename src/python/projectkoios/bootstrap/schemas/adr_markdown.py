from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Mapping

from projectkoios.bootstrap.schemas.models import (
    CONCERN_LEVEL_ORDER,
    DRAFT_ADR_SECTION_FIELDS,
    DRAFT_ADR_SECTION_HEADINGS,
    Concern,
    ConcernLevel,
    DraftAdrRecord,
    RejectedMarkdown,
    Section,
)


class MarkdownIngestError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class DraftAdrMarkdownRenderer:
    def render(self, record: DraftAdrRecord) -> str:
        metadata = record.metadata.to_dict()
        lines: list[str] = [f"# ADR: {metadata['title']}", "", "```json"]
        lines.extend(json.dumps(metadata, indent=2, sort_keys=True).splitlines())
        lines.extend(["```", ""])
        for field in DRAFT_ADR_SECTION_FIELDS:
            section = record.content.sections[field]
            lines.extend(self.render_section(section, level=2))
        if record.content.rejected:
            lines.extend(["## Rejected", ""])
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
        heading_prefix = "#" * level
        lines = [f"{heading_prefix} {section.heading}", "", section.description, "", "### Concern"]
        sorted_concerns = sorted(section.concerns, key=lambda concern: CONCERN_LEVEL_ORDER.index(concern.level))
        for concern in sorted_concerns:
            lines.append(f"- {concern.level.value} {concern.text}")
        lines.append("")
        for subsection in section.subsections:
            lines.extend(self.render_section(subsection, level=level + 1))
        return lines


@dataclass(frozen=True, slots=True)
class DraftAdrMarkdownIngester:
    def ingest(self, markdown: str) -> dict[str, Any]:
        lines = markdown.splitlines()
        metadata, body_start = self.parse_metadata(lines)
        content = self.parse_content(lines[body_start:])
        return {"metadata": metadata, "content": content}

    def parse_metadata(self, lines: list[str]) -> tuple[dict[str, Any], int]:
        if not lines or not lines[0].startswith("# ADR: "):
            raise MarkdownIngestError("Missing ADR title heading")
        fence_start = self.find_line(lines, "```json", start=1)
        if fence_start is None:
            raise MarkdownIngestError("Missing metadata JSON block")
        fence_end = self.find_line(lines, "```", start=fence_start + 1)
        if fence_end is None:
            raise MarkdownIngestError("Unclosed metadata JSON block")
        try:
            metadata = json.loads("\n".join(lines[fence_start + 1:fence_end]))
        except json.JSONDecodeError as error:
            raise MarkdownIngestError(f"Invalid metadata JSON: {error}") from error
        if not isinstance(metadata, dict):
            raise MarkdownIngestError("Metadata JSON must be an object")
        title = lines[0].removeprefix("# ADR: ")
        if metadata.get("title") != title:
            raise MarkdownIngestError("Title heading must match metadata.title")
        return metadata, fence_end + 1

    def parse_content(self, lines: list[str]) -> dict[str, Any]:
        sections: dict[str, Any] = {}
        index = self.skip_blank(lines, 0)
        for field in DRAFT_ADR_SECTION_FIELDS:
            expected_heading = DRAFT_ADR_SECTION_HEADINGS[field]
            section, index = self.parse_required_section(lines, index, expected_heading)
            sections[field] = section
            index = self.skip_blank(lines, index)
        rejected: list[dict[str, str]] = []
        while index < len(lines):
            if lines[index].startswith("####"):
                raise MarkdownIngestError("Ambiguous heading depth")
            if lines[index] == "## Rejected":
                captured, index = self.parse_rendered_rejected(lines, index + 1)
                rejected.extend(captured)
                index = self.skip_blank(lines, index)
                continue
            if lines[index].startswith("## "):
                heading = lines[index].removeprefix("## ")
                body_start = index + 1
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

    def parse_required_section(self, lines: list[str], index: int, expected_heading: str) -> tuple[dict[str, Any], int]:
        if index >= len(lines) or lines[index] != f"## {expected_heading}":
            raise MarkdownIngestError(f"Missing or out-of-order section: {expected_heading}")
        index += 1
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
        description = "\n".join(description_lines).strip()
        if len(description) > 600:
            raise MarkdownIngestError(f"Section description exceeds 600 characters: {expected_heading}")
        index += 1
        concerns: list[dict[str, str]] = []
        while index < len(lines) and not lines[index].startswith("## "):
            line = lines[index]
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
        if not line.startswith("- "):
            raise MarkdownIngestError(f"Malformed concern line: {line}")
        text = line.removeprefix("- ")
        for level in (ConcernLevel.MUST_NOT, ConcernLevel.SHOULD_NOT, ConcernLevel.MUST, ConcernLevel.SHOULD, ConcernLevel.MAY):
            prefix = f"{level.value} "
            if text.startswith(prefix):
                concern_text = text.removeprefix(prefix)
                if not concern_text:
                    raise MarkdownIngestError(f"Empty concern text: {line}")
                return {"level": level.value, "text": concern_text}
        raise MarkdownIngestError(f"Malformed concern keyword: {line}")

    def parse_rendered_rejected(self, lines: list[str], index: int) -> tuple[list[dict[str, str]], int]:
        rejected: list[dict[str, str]] = []
        index = self.skip_blank(lines, index)
        while index < len(lines) and not lines[index].startswith("## "):
            if not lines[index].startswith("### "):
                raise MarkdownIngestError("Rendered rejected content must use ### headings")
            heading = lines[index].removeprefix("### ")
            index = self.skip_blank(lines, index + 1)
            if index >= len(lines) or not lines[index].startswith("Reason: "):
                raise MarkdownIngestError("Rendered rejected content missing reason")
            reason = lines[index].removeprefix("Reason: ")
            index = self.skip_blank(lines, index + 1)
            if index >= len(lines) or lines[index] != "```text":
                raise MarkdownIngestError("Rendered rejected content missing text fence")
            fence_end = self.find_line(lines, "```", start=index + 1)
            if fence_end is None:
                raise MarkdownIngestError("Unclosed rejected text fence")
            body = "\n".join(lines[index + 1:fence_end])
            rejected.append({"heading": heading, "reason": reason, "body": body})
            index = self.skip_blank(lines, fence_end + 1)
        return rejected, index

    def find_line(self, lines: list[str], target: str, *, start: int) -> int | None:
        for index in range(start, len(lines)):
            if lines[index] == target:
                return index
        return None

    def skip_blank(self, lines: list[str], index: int) -> int:
        while index < len(lines) and not lines[index].strip():
            index += 1
        return index

    def next_top_heading(self, lines: list[str], index: int) -> int:
        while index < len(lines) and not lines[index].startswith("## "):
            if lines[index].startswith("####"):
                raise MarkdownIngestError("Ambiguous heading depth")
            index += 1
        return index
