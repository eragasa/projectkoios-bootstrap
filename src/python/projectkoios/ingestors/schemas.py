from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping
import json


@dataclass(frozen=True, slots=True)
class JsonSchema:
    path: Path
    document: Mapping[str, Any]

    @property
    def title(self) -> str:
        return str(self.document.get("title", self.path.stem))

    @property
    def version(self) -> str:
        return str(self.document.get("$id", self.path.name))

    def as_dict(self) -> dict[str, Any]:
        return dict(self.document)


class JsonSchemaLoader:
    def load(self, path: Path) -> JsonSchema:
        resolved = path.resolve()
        document = json.loads(resolved.read_text(encoding="utf-8"))
        if not isinstance(document, dict):
            raise TypeError(f"JSON Schema must be an object: {resolved}")
        return JsonSchema(path=resolved, document=document)


class JsonSchemaValidator:
    def __init__(self, schema: JsonSchema) -> None:
        self._schema = schema

    @property
    def schema(self) -> JsonSchema:
        return self._schema

    def validate(self, instance: Mapping[str, Any]) -> None:
        self._validate_node(self._schema.as_dict(), instance, path=self._schema.title)

    def _validate_node(self, schema: Mapping[str, Any], value: Any, *, path: str) -> None:
        expected_type = schema.get("type")
        if expected_type is not None:
            self._check_type(expected_type, value, path)

        enum_values = schema.get("enum")
        if enum_values is not None and value not in enum_values:
            raise ValueError(f"{path}: expected one of {enum_values!r}, got {value!r}")

        if isinstance(value, Mapping):
            required = tuple(schema.get("required", ()))
            for key in required:
                if key not in value:
                    raise ValueError(f"{path}: missing required key '{key}'")
            properties = schema.get("properties", {})
            if not isinstance(properties, Mapping):
                raise TypeError(f"{path}: 'properties' must be a mapping")
            for key, child_schema in properties.items():
                if key in value and isinstance(child_schema, Mapping):
                    self._validate_node(child_schema, value[key], path=f"{path}.{key}")
            additional = schema.get("additionalProperties", True)
            if additional is False:
                allowed = set(properties.keys())
                extra = [key for key in value.keys() if key not in allowed]
                if extra:
                    raise ValueError(f"{path}: unexpected keys {extra!r}")

        if isinstance(value, list):
            item_schema = schema.get("items")
            if isinstance(item_schema, Mapping):
                for index, item in enumerate(value):
                    self._validate_node(item_schema, item, path=f"{path}[{index}]")

    def _check_type(self, expected_type: Any, value: Any, path: str) -> None:
        if isinstance(expected_type, list):
            if any(self._matches_type(kind, value) for kind in expected_type):
                return
            raise TypeError(f"{path}: expected one of {expected_type!r}, got {type(value).__name__}")
        if not self._matches_type(expected_type, value):
            raise TypeError(f"{path}: expected {expected_type!r}, got {type(value).__name__}")

    def _matches_type(self, expected_type: Any, value: Any) -> bool:
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
