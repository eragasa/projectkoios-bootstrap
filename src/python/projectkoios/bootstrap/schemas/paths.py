from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[5]
SCHEMAS_DIR = REPO_ROOT / "docs" / "schemas"
PROJECT_SCHEMA_URI_PREFIX = "https://projectkoios.local/schemas/"


@dataclass(frozen=True, slots=True)
class SchemaPaths:
    repo_root: Path = REPO_ROOT
    schemas_dir: Path = SCHEMAS_DIR

    def canonical_schema_path(self, filename: str) -> Path:
        if Path(filename).name != filename:
            raise ValueError(f"Schema filename must not include path segments: {filename}")
        if filename.startswith("legacy-"):
            raise ValueError(f"Legacy schema is not canonical: {filename}")
        path = self.schemas_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Schema file not found: {path}")
        return path

    def schema_uri(self, filename: str) -> str:
        self.canonical_schema_path(filename)
        return f"{PROJECT_SCHEMA_URI_PREFIX}{filename}"
