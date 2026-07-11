from __future__ import annotations

from dataclasses import dataclass

from projectkoios.bootstrap.schema.models import JsonObject


class AdrSemanticEqualityError(AssertionError):
    """Raised when ADR records differ under pilot semantic equality."""


@dataclass(frozen=True, slots=True)
class AdrSemanticComparer:
    """Compare ADR records under the pilot semantic equality policy."""

    def assert_equal(self, expected: JsonObject, actual: JsonObject) -> None:
        """Assert that two ADR records are semantically equal.

        Args:
            expected: Expected schema-backed ADR record.
            actual: Actual schema-backed ADR record.

        Raises:
            AdrSemanticEqualityError: If records differ.
        """
        if expected != actual:
            raise AdrSemanticEqualityError("ADR records differ under semantic equality policy")

    def equal(self, expected: JsonObject, actual: JsonObject) -> bool:
        """Return whether two ADR records are semantically equal.

        Args:
            expected: Expected schema-backed ADR record.
            actual: Actual schema-backed ADR record.

        Returns:
            Whether the records are equal.
        """
        return expected == actual
