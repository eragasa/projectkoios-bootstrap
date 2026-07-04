from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Mapping


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
        resolved: Path = path.resolve()
        document: Any = json.loads(resolved.read_text(encoding="utf-8"))
        if not isinstance(document, dict):
            raise TypeError(f"JSON Schema must be an object: {resolved}")
        return JsonSchema(path=resolved, document=document)


class JsonSchemaValidator:
    def __init__(self, schema: JsonSchema) -> None:
        self.schema: JsonSchema = schema

    def validate(self, instance: Mapping[str, Any]) -> None:
        self.validate_node(self.schema.as_dict(), instance, path=self.schema.title)

    def validate_node(self, schema: Mapping[str, Any], value: Any, *, path: str) -> None:
        expected_type: Any = schema.get("type")
        if expected_type is not None:
            self.check_type(expected_type, value, path)

        enum_values: Any = schema.get("enum")
        if enum_values is not None and value not in enum_values:
            raise ValueError(f"{path}: expected one of {enum_values!r}, got {value!r}")

        if isinstance(value, Mapping):
            required: tuple[Any, ...] = tuple(schema.get("required", ()))
            key: Any
            for key in required:
                if key not in value:
                    raise ValueError(f"{path}: missing required key '{key}'")
            properties: Any = schema.get("properties", {})
            if not isinstance(properties, Mapping):
                raise TypeError(f"{path}: 'properties' must be a mapping")
            child_key: Any
            child_schema: Any
            for child_key, child_schema in properties.items():
                if child_key in value and isinstance(child_schema, Mapping):
                    self.validate_node(child_schema, value[child_key], path=f"{path}.{child_key}")
            additional: Any = schema.get("additionalProperties", True)
            if additional is False:
                allowed: set[Any] = set(properties.keys())
                extra: list[Any] = [value_key for value_key in value.keys() if value_key not in allowed]
                if extra:
                    raise ValueError(f"{path}: unexpected keys {extra!r}")

        if isinstance(value, list):
            item_schema: Any = schema.get("items")
            if isinstance(item_schema, Mapping):
                index: int
                item: Any
                for index, item in enumerate(value):
                    self.validate_node(item_schema, item, path=f"{path}[{index}]")

    def check_type(self, expected_type: Any, value: Any, path: str) -> None:
        if isinstance(expected_type, list):
            if any(self.matches_type(kind, value) for kind in expected_type):
                return
            raise TypeError(f"{path}: expected one of {expected_type!r}, got {type(value).__name__}")
        if not self.matches_type(expected_type, value):
            raise TypeError(f"{path}: expected {expected_type!r}, got {type(value).__name__}")

    def matches_type(self, expected_type: Any, value: Any) -> bool:
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
