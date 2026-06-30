from __future__ import annotations

from pathlib import Path
import re

from projectkoios.bootstrap.harness.data.artifact import HandoffArtifact


HEADER_FIELD_PATTERN = re.compile(r"^([A-Za-z][A-Za-z0-9_-]+):\s*(.*)$")
"""Matches ``Key: value`` lines in handoff file headers."""


class HandoffParser:
    """Tokenizer that converts handoff files into ``HandoffArtifact`` tokens.

    Each ``*.md`` file in a handoff directory is parsed:
    1. Header fields are extracted from the top of the file
       (``_extract_frontmatter``).
    2. An artifact kind is inferred from the title and header combination
       (``_infer_kind``).
    3. A frozen ``HandoffArtifact`` is returned.

    Files without recognised headers return ``None`` (skipped).
    The parser is stateless — it can be reused safely.
    """

    def parse_file(self, path: Path) -> HandoffArtifact | None:
        """Parse a single handoff file, or return ``None`` if it has no headers."""
        if not path.exists():
            return None
        text = path.read_text(encoding="utf-8")
        return self._parse_text(path, text)

    def parse_directory(self, directory: Path) -> list[HandoffArtifact]:
        """Parse every ``*.md`` file in *directory*, sorted by path."""
        result: list[HandoffArtifact] = []
        if not directory.exists():
            return result
        for path in sorted(directory.iterdir()):
            if path.is_file() and path.suffix == ".md":
                token = self.parse_file(path)
                if token is not None:
                    result.append(token)
        return result

    def _parse_text(self, path: Path, text: str) -> HandoffArtifact | None:
        """Internal: build an artifact from header fields and title."""
        frontmatter = self._extract_frontmatter(text)
        if not frontmatter:
            return None

        return HandoffArtifact(
            path=path,
            kind=self._infer_kind(frontmatter, text),
            origin=frontmatter.get("Origin", ""),
            sender=frontmatter.get("From", ""),
            recipient=frontmatter.get("To", ""),
            acting_as=frontmatter.get("Acting-As"),
            delegated_operator=frontmatter.get("Delegated-Operator"),
            provenance=[
                v for k, v in frontmatter.items()
                if k.lower() in ("origin", "from", "scope", "repository")
            ],
        )

    def _extract_frontmatter(self, text: str) -> dict[str, str]:
        """Extract header field key-value pairs from the top of *text*.

        Scanning stops at the first non-header line (blank line or prose).
        Duplicate keys overwrite — the last occurrence wins.
        """
        fields: dict[str, str] = {}
        for line in text.splitlines():
            m = HEADER_FIELD_PATTERN.match(line)
            if m:
                fields[m.group(1)] = m.group(2).strip()
            elif fields:
                break
        return fields

    def _infer_kind(self, frontmatter: dict[str, str], text: str) -> str:
        """Classify the artifact by its H1 title, then fall back to sender/recipient.

        Title checks use substring matching on lowercase text, ordered from
        most to least specific to minimise false positives. The final fallback
        returns ``"user-request"``.
        """
        title_lower = ""
        for line in text.splitlines():
            if line.startswith("# "):
                title_lower = line.lower()
                break

        from_hdr = frontmatter.get("From", "").lower()
        to_hdr = frontmatter.get("To", "").lower()

        if "architecture" in title_lower or "spec" in title_lower:
            return "architecture-spec"
        if "acceptance" in title_lower or "acceptance-criteria" in title_lower:
            return "acceptance-criteria"
        if "implementation brief" in title_lower or "implementation-brief" in title_lower:
            return "implementation-brief"
        if "implementation plan" in title_lower or "implementation-plan" in title_lower:
            return "implementation-plan"
        if "implementation report" in title_lower or "implementation-report" in title_lower:
            return "implementation-report"
        if "patch" in title_lower:
            return "patch"
        if "test results" in title_lower or "test-results" in title_lower:
            return "test-results"
        if "routing" in title_lower:
            return "routing-decision"
        if "blockage" in title_lower or "blocked" in title_lower:
            return "blockage-report"
        if "revision" in title_lower:
            return "revision-request"
        if "completion" in title_lower:
            return "completion-decision"
        if "deviation" in title_lower:
            return "deviation-report"
        if "knowledge" in title_lower:
            return "knowledge-note"
        if "provenance" in title_lower:
            return "provenance-index"
        if from_hdr in ("vulcan", "opencode") and to_hdr in ("athena", "archon", "pi", "hermes"):
            return "implementation-report"
        if from_hdr in ("athena", "archon") and to_hdr in ("vulcan", "opencode"):
            return "implementation-brief"

        return "user-request"
