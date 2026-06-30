"""Hermes-owned Graphify ingestion daemon for projectkoios-bootstrap.

Implements the first slice of ADR adr.20260701.004713: a local background
service that performs an initial full Graphify build, watches the repository
filesystem for eligible changes, debounces and coalesces events, and publishes
updated local Graphify snapshots, universal chunk cards, run metadata,
freshness markers, and degraded-state reports to Hermes-local runtime state.

The daemon's internal state is modeled as Colored Petri net DataObjects and
ActivityObjects, consistent with adr.20260630.042202_colored-petri-net-meta-harness.
"""
