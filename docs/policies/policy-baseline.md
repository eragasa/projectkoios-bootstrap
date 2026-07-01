# Policy Baseline

## Purpose

This document is the policy surface baseline for Project Koios bootstrap.

Policy surfaces are vision surfaces: they define values, priorities, and target
assumptions that guide how agents and processes evolve over time.

This is not an implementation plan.

## Policy Principles

### PP-001: Policy Changes Long-Term Direction

Policy changes may update long-term goals by changing agent motivations,
personality defaults, and priority ordering.

### PP-002: Policy Is a Vision Surface

Policy should stay broad enough to steer evolution, but concrete enough to
shape downstream behavior.

### PP-003: Target Assumptions

Policy should record the assumptions the system should evolve toward.

### PP-004: Human Override

Humans may override policy-derived priorities when necessary.

## Relationship To Other Surfaces

- ADRs capture explicit architecture decisions.
- Review mechanics evaluate coherence and improvement.
- Code implements behavior within the current policy direction.
- Markdown may serve as a hybrid control/render surface.
