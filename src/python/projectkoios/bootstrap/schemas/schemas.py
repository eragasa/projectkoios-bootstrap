from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
from referencing import Registry, Resource

from projectkoios.bootstrap.schemas.paths import PROJECT_SCHEMA_URI_PREFIX, SchemaPaths


@dataclass(frozen=True, slots=True)
class SchemaRegistry:
    paths: SchemaPaths = SchemaPaths()

    def load_schema(self, filename: str) -> dict[str, Any]:
        path = self.paths.canonical_schema_path(filename)
        document = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(document, dict):
            raise TypeError(f"Schema must be a JSON object: {path}")
        return document

    def validator_for(self, filename: str) -> Draft202012Validator:
        schema = self.load_schema(filename)
        registry = self.local_registry()
        Draft202012Validator.check_schema(schema)
        return Draft202012Validator(schema, registry=registry)

    def validate(self, filename: str, instance: Mapping[str, Any]) -> None:
        self.validator_for(filename).validate(instance)

    def local_registry(self) -> Registry:
        registry = Registry()
        path: Path
        for path in sorted(self.paths.schemas_dir.glob("*.json")):
            if path.name.startswith("legacy-"):
                continue
            document = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(document, dict):
                raise TypeError(f"Schema must be a JSON object: {path}")
            schema_id = document.get("$id", f"{PROJECT_SCHEMA_URI_PREFIX}{path.name}")
            if not isinstance(schema_id, str):
                raise TypeError(f"Schema $id must be a string: {path}")
            registry = registry.with_resource(schema_id, Resource.from_contents(document))
        return registry


def format_validation_error(error: ValidationError) -> str:
    path = ".".join(str(part) for part in error.absolute_path)
    if path:
        return f"{path}: {error.message}"
    return error.message
