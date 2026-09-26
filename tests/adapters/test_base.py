from __future__ import annotations

from dataclasses import FrozenInstanceError, dataclass

import pytest
from projectkoios.bootstrap.adapters.base import Adapter, Binding, Integration


@dataclass(frozen=True, slots=True)
class _DependencyBinding(Binding):
    dependency_name: str


@dataclass(frozen=True, slots=True)
class _ServiceIntegration(Integration):
    service_name: str
    binding: _DependencyBinding


def test_adapter_is_nominal_without_inventing_a_generic_operation() -> None:
    assert issubclass(Binding, Adapter)
    assert issubclass(Integration, Adapter)
    assert not hasattr(Adapter, "adapt")
    assert not hasattr(Adapter, "execute")


def test_binding_is_a_distinct_immutable_adapter_role() -> None:
    binding = _DependencyBinding(dependency_name="example-dependency")

    assert isinstance(binding, Adapter)
    assert isinstance(binding, Binding)
    assert not isinstance(binding, Integration)
    with pytest.raises(FrozenInstanceError):
        binding.dependency_name = "changed"  # type: ignore[misc]


def test_integration_contains_a_binding_through_composition() -> None:
    binding = _DependencyBinding(dependency_name="example-client")
    integration = _ServiceIntegration(
        service_name="example-service",
        binding=binding,
    )

    assert isinstance(integration, Adapter)
    assert isinstance(integration, Integration)
    assert not isinstance(integration, Binding)
    assert integration.binding is binding
    assert not issubclass(Integration, Binding)
