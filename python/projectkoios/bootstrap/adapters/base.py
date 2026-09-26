"""Nominal base classes for maintained bootstrap boundary adapters.

The taxonomy is adapted from Project Koios Frankenstein commit
``88ee17332a5fdf0fddceedf8e08cbd55968cf8d7``:
https://github.com/eragasa/projectkoios-frankenstein/blob/88ee17332a5fdf0fddceedf8e08cbd55968cf8d7/docs/architecture/adapters/index.md

An adapter is a nominal role rather than a claim that every boundary shares an
``adapt`` or ``execute`` operation. Bindings adapt imported or deliberately
vendored code. Integrations adapt external applications or services. An
integration may contain a binding, but the roles stay separate.
"""

from __future__ import annotations


class Adapter:
    """Common nominal base for maintained bootstrap boundary adapters."""

    __slots__ = ()


class Binding(Adapter):
    """Adapter to imported or deliberately vendored code."""

    __slots__ = ()


class Integration(Adapter):
    """Adapter to an external application or service."""

    __slots__ = ()


__all__ = ["Adapter", "Binding", "Integration"]
