from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Mapping, TypeAlias, cast


JsonScalar: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
JsonObject: TypeAlias = dict[str, JsonValue]


@dataclass(frozen=True, slots=True)
class JsonSchema:
    """Loaded JSON Schema document.

    Args:
        path: Resolved schema path.
        document: Parsed schema document object.
    """

    path: Path
    document: Mapping[str, JsonValue]

    @property
    def title(self) -> str:
        """Return the schema title or file stem fallback."""
        return str(self.document.get("title", self.path.stem))

    @property
    def version(self) -> str:
        """Return the schema identifier or filename fallback."""
        return str(self.document.get("$id", self.path.name))

    def as_dict(self) -> JsonObject:
        """Return a mutable dictionary copy of the schema document."""
        return dict(self.document)


class JsonSchemaLoader:
    """Load JSON Schema documents from disk."""

    def load(self, path: Path) -> JsonSchema:
        """Load and parse a JSON Schema file.

        Args:
            path: Schema file path.

        Returns:
            Loaded JSON Schema object.
        """

        # Resolved path is used in diagnostics and returned schema metadata.
        resolved: Path = path.resolve()
        # Document is the parsed JSON value from the schema file.
        document: JsonValue = cast(JsonValue, json.loads(resolved.read_text(encoding="utf-8")))
        if not isinstance(document, dict):
            raise TypeError(f"JSON Schema must be an object: {resolved}")
        return JsonSchema(path=resolved, document=document)


class JsonSchemaValidator:
    """Small JSON Schema validator for repository-local config schemas."""

    def __init__(self, schema: JsonSchema) -> None:
        self.schema: JsonSchema = schema

    def validate(self, instance: Mapping[str, JsonValue]) -> None:
        """Validate one instance against the loaded schema."""
        self.validate_node(self.schema.as_dict(), cast(JsonValue, dict(instance)), path=self.schema.title)

    def validate_node(self, schema: Mapping[str, JsonValue], value: JsonValue, *, path: str) -> None:
        """Validate one node of a JSON-compatible value against a schema node."""
        # Expected type is the optional JSON Schema type declaration.
        expected_type: JsonValue = schema.get("type")
        if expected_type is not None:
            self.check_type(expected_type, value, path)

        # Enum values are allowed literal values for this node.
        enum_values: JsonValue = schema.get("enum")
        if isinstance(enum_values, list) and value not in enum_values:
            raise ValueError(f"{path}: expected one of {enum_values!r}, got {value!r}")

        if isinstance(value, Mapping):
            # Required contains object keys that must be present.
            required_value: JsonValue = schema.get("required", [])
            # Required contains only list entries from the schema document.
            required: tuple[JsonValue, ...] = tuple(required_value) if isinstance(required_value, list) else ()
            key: JsonValue
            for key in required:
                if key not in value:
                    raise ValueError(f"{path}: missing required key '{key}'")
            # Properties maps object keys to child schemas.
            properties_value: JsonValue = schema.get("properties", {})
            if not isinstance(properties_value, Mapping):
                raise TypeError(f"{path}: 'properties' must be a mapping")
            # Properties is the object mapping used for child validation.
            properties: Mapping[str, JsonValue] = cast(Mapping[str, JsonValue], properties_value)
            child_key: str
            child_schema: JsonValue
            for child_key, child_schema in properties.items():
                if child_key in value and isinstance(child_schema, Mapping):
                    self.validate_node(child_schema, value[child_key], path=f"{path}.{child_key}")
            # Additional controls whether undeclared object keys are allowed.
            additional: JsonValue = schema.get("additionalProperties", True)
            if additional is False:
                # Allowed contains declared property names.
                allowed: set[str] = set(properties.keys())
                # Extra contains instance keys not declared in properties.
                extra: list[str] = [value_key for value_key in value.keys() if str(value_key) not in allowed]
                if extra:
                    raise ValueError(f"{path}: unexpected keys {extra!r}")

        if isinstance(value, list):
            # Item schema validates each array element when object-shaped.
            item_schema: JsonValue = schema.get("items")
            if isinstance(item_schema, Mapping):
                index: int
                item: JsonValue
                for index, item in enumerate(value):
                    self.validate_node(item_schema, item, path=f"{path}[{index}]")

    def check_type(self, expected_type: JsonValue, value: JsonValue, path: str) -> None:
        """Validate a value against a JSON Schema type declaration."""
        if isinstance(expected_type, list):
            if any(self.matches_type(kind, value) for kind in expected_type):
                return
            raise TypeError(f"{path}: expected one of {expected_type!r}, got {type(value).__name__}")
        if not self.matches_type(expected_type, value):
            raise TypeError(f"{path}: expected {expected_type!r}, got {type(value).__name__}")

    def matches_type(self, expected_type: JsonValue, value: JsonValue) -> bool:
        """Return whether a JSON value matches one schema type name."""
        match expected_type:
            case "object":
                return isinstance(value, Mapping)
            case "array":
                return isinstance(value, list)
            case "string":
                return isinstance(value, str)
            case "integer":
                return isinstance(value, int) and not isinstance(value, bool)
            case "number":
                return isinstance(value, (int, float)) and not isinstance(value, bool)
            case "boolean":
                return isinstance(value, bool)
            case "null":
                return value is None
            case _:
                return True
