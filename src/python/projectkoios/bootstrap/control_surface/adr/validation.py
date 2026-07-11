from __future__ import annotations

from dataclasses import dataclass

from jsonschema.exceptions import ValidationError

from projectkoios.bootstrap.schema import SchemaRegistry
from projectkoios.bootstrap.schema.models import JsonObject


@dataclass(frozen=True, slots=True)
class AdrRecordValidator:
    """Validate ADR records against the canonical ADR schema.

    Args:
        schema_registry: Offline project schema registry.
    """

    schema_registry: SchemaRegistry = SchemaRegistry()

    def validate(self, record: JsonObject) -> None:
        """Validate one plain ADR schema record.

        Args:
            record: ADR record to validate.

        Raises:
            ValidationError: If the record fails schema validation.
        """
        self.schema_registry.validate("adr.schema.json", record)

    def schema_id(self) -> str:
        """Return the ADR schema identifier.

        Returns:
            Schema `$id` value.
        """
        # Schema document is loaded through the offline registry surface.
        schema: JsonObject = self.schema_registry.load_schema("adr.schema.json")
        # Schema identifier is copied into manifest and projection metadata.
        schema_id: object = schema.get("$id", "https://projectkoios.local/schemas/adr.schema.json")
        if not isinstance(schema_id, str):
            raise TypeError("ADR schema $id must be a string")
        return schema_id

    def invalid_record_error(self, record: JsonObject) -> str:
        """Return inspectable validation error text for an invalid record.

        Args:
            record: Invalid ADR record.

        Returns:
            Validation error text.
        """
        # Validation errors are collected without exception handler locals.
        errors: list[ValidationError] = list(self.schema_registry.validator_for("adr.schema.json").iter_errors(record))
        if errors:
            return str(errors[0].message)
        raise AssertionError("Record unexpectedly passed validation")
