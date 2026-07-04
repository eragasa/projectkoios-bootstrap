from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[5]
SCHEMAS_DIR = REPO_ROOT / "docs" / "schemas"
PROJECT_SCHEMA_URI_PREFIX = "https://projectkoios.local/schemas/"


@dataclass(frozen=True, slots=True)
class SchemaPaths:
    """Canonical filesystem paths for Project Koios schemas.

    Args:
        repo_root: Repository root path.
        schemas_dir: Canonical schema directory.
    """

    repo_root: Path = REPO_ROOT
    schemas_dir: Path = SCHEMAS_DIR

    def canonical_schema_path(self, filename: str) -> Path:
        """Return the canonical path for a schema filename.

        Args:
            filename: Schema filename without directory components.

        Returns:
            Canonical schema file path.

        Raises:
            ValueError: If filename is path-like or legacy-only.
            FileNotFoundError: If the canonical schema file does not exist.
        """
        if Path(filename).name != filename:
            raise ValueError(f"Schema filename must not include path segments: {filename}")
        if filename.startswith("legacy-"):
            raise ValueError(f"Legacy schema is not canonical: {filename}")
        # Canonical path lives under docs/schemas.
        path: Path = self.schemas_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Schema file not found: {path}")
        return path

    def schema_uri(self, filename: str) -> str:
        """Return the project-local schema URI for a canonical schema.

        Args:
            filename: Schema filename without directory components.

        Returns:
            Project-local schema URI.
        """
        self.canonical_schema_path(filename)
        return f"{PROJECT_SCHEMA_URI_PREFIX}{filename}"
