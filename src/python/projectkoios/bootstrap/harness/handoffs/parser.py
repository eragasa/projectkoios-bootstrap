from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.artifact import HandoffArtifact
from projectkoios.bootstrap.harness.headers import extract_handoff_headers


class HandoffParser:
    """Tokenizer that converts handoff files into ``HandoffArtifact`` tokens."""

    def parse_file(self, path: Path) -> HandoffArtifact | None:
        """Parse a single handoff file, or return ``None`` if it has no headers."""
        if not path.exists():
            return None
        text: str = path.read_text(encoding="utf-8")
        return self.parse_text(path, text)

    def parse_directory(self, directory: Path) -> list[HandoffArtifact]:
        """Parse every ``*.md`` file in *directory*, sorted by path."""
        result: list[HandoffArtifact] = []
        if not directory.exists():
            return result
        path: Path
        for path in sorted(directory.iterdir()):
            if path.is_file() and path.suffix == ".md":
                token: HandoffArtifact | None = self.parse_file(path)
                if token is not None:
                    result.append(token)
        return result

    def parse_text(self, path: Path, text: str) -> HandoffArtifact | None:
        """Build an artifact from header fields and title."""
        frontmatter: dict[str, str] = self.extract_frontmatter(text)
        if not frontmatter:
            return None

        return HandoffArtifact(
            path=path,
            kind=self.infer_kind(frontmatter, text),
            origin=frontmatter.get("Origin", ""),
            sender=frontmatter.get("From", ""),
            recipient=frontmatter.get("To", ""),
            acting_as=frontmatter.get("Acting-As"),
            delegated_operator=frontmatter.get("Delegated-Operator"),
            provenance=[
                value for key, value in frontmatter.items()
                if key.lower() in ("origin", "from", "scope", "repository")
            ],
        )

    def extract_frontmatter(self, text: str) -> dict[str, str]:
        return extract_handoff_headers(text)

    def infer_kind(self, frontmatter: dict[str, str], text: str) -> str:
        """Classify the artifact by its H1 title, then fall back to sender/recipient."""
        title_lower: str = next((line.lower() for line in text.splitlines() if line.startswith("# ")), "")

        from_hdr: str = frontmatter.get("From", "").lower()
        to_hdr: str = frontmatter.get("To", "").lower()

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
