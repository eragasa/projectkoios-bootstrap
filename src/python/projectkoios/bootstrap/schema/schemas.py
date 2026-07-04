from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
from referencing import Registry, Resource

from projectkoios.bootstrap.schema.paths import PROJECT_SCHEMA_URI_PREFIX, SchemaPaths

JsonObject = dict[str, Any]


@dataclass(frozen=True, slots=True)
class SchemaRegistry:
    """Load and validate canonical Project Koios schemas.

    Args:
        paths: Schema path resolver.
    """

    paths: SchemaPaths = SchemaPaths()

    def load_schema(self, filename: str) -> JsonObject:
        """Load one canonical JSON Schema document.

        Args:
            filename: Canonical schema filename.

        Returns:
            JSON Schema document.

        Raises:
            TypeError: If the schema file does not contain a JSON object.
        """
        # Schema path is resolved through canonical namespace rules.
        path: Path = self.paths.canonical_schema_path(filename)
        # Raw JSON document is decoded before object-shape validation.
        document: object = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(document, dict):
            raise TypeError(f"Schema must be a JSON object: {path}")
        return document

    def validator_for(self, filename: str) -> Draft202012Validator:
        """Build a draft 2020-12 validator for one schema.

        Args:
            filename: Canonical schema filename.

        Returns:
            JSON Schema validator using the local registry.
        """
        # Schema document controls the validator root.
        schema: JsonObject = self.load_schema(filename)
        # Local registry resolves project-local schema URIs offline.
        registry: Registry = self.local_registry()
        Draft202012Validator.check_schema(schema)
        return Draft202012Validator(schema, registry=registry)

    def validate(self, filename: str, instance: Mapping[str, Any]) -> None:
        """Validate an instance against a canonical schema.

        Args:
            filename: Canonical schema filename.
            instance: JSON-like instance mapping.

        Raises:
            jsonschema.exceptions.ValidationError: If validation fails.
        """
        self.validator_for(filename).validate(instance)

    def local_registry(self) -> Registry:
        """Build an offline registry for canonical project-local schemas.

        Returns:
            Registry keyed by schema `$id` values.

        Raises:
            TypeError: If a schema file has an invalid shape or `$id`.
        """
        # Registry starts empty and is extended with canonical schema resources.
        registry: Registry = Registry()
        path: Path
        for path in sorted(self.paths.schemas_dir.glob("*.json")):
            if path.name.startswith("legacy-"):
                continue
            # Schema resource document must be object-shaped.
            document: object = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(document, dict):
                raise TypeError(f"Schema must be a JSON object: {path}")
            # Schema identifier defaults to the project-local URI convention.
            schema_id: object = document.get("$id", f"{PROJECT_SCHEMA_URI_PREFIX}{path.name}")
            if not isinstance(schema_id, str):
                raise TypeError(f"Schema $id must be a string: {path}")
            registry = registry.with_resource(schema_id, Resource.from_contents(document))
        return registry


def format_validation_error(error: ValidationError) -> str:
    """Format a JSON Schema validation error for humans.

    Args:
        error: JSON Schema validation error.

    Returns:
        Concise path-prefixed error text.
    """
    # Error path identifies the failing instance location.
    path: str = ".".join(str(part) for part in error.absolute_path)
    if path:
        return f"{path}: {error.message}"
    return error.message
