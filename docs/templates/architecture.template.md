# Architecture note template

Controlled by: [adr.templates](../adr/adr.templates.md).
Template index: [templates.00](templates.00.md).

Architecture notes represent the best-effort documentation of the current state
of the system. They are navigation, synthesis, and decomposition surfaces. They
should link to controlling authority and evidence, but they do not create new
architecture authority unless promoted through the appropriate ADR/spec process.

This is the current architecture note template. Existing architecture notes that
use the older YAML-frontmatter format remain valid until explicitly migrated.

## Note format

````md
# Architecture: <Title>

```json
{
  "title": "<Title>",
  "artifact_type": "architecture-note",
  "status": "working-draft",
  "datetime": "YYYYMMDD.HHMMSSZ",
  "repository": "projectkoios-bootstrap",
  "scope": "<bounded scope>",
  "canonical_location": "docs/architecture/architecture.<topic>.md"
}
```

## Purpose

<Purpose of the document. State what system surface this note describes and what
kind of current-state synthesis it provides.>

## Index

### Architecture Decomposition

| # | Surface | Role / Scope |
|---|---|---|
| 1 | `<architecture surface>` | `<what it decomposes or indexes>` |

### Controlling ADR

Only include ADRs that are appropriate at this architecture-note level.

| # | ADR | Applicability |
|---|---|---|
| 1 | `<ADR path>` | `<what it controls for this surface>` |

### Specifications

| # | Specification | Status / Applicability |
|---|---|---|
| 1 | `<spec path>` | `<status or scope>` |

### Specific Tests

Specific tests are an evidence index only. Test authority remains in actual test
files, test results, implementation reports, and review artifacts.

#### Unit Tests

| # | Test | Coverage |
|---|---|---|
| 1 | `<test path>` | `<behavior covered>` |

#### Integration Tests

| # | Test | Coverage |
|---|---|---|
| 1 | `<test path>` | `<integration boundary covered>` |

### Use Cases

Use cases describe tests or examples that cross classes, modules, packages, or
roles and show the architecture operating as a system. They are evidence and
scenario indexes, not independent architecture authority.

| # | Use case | Coverage |
|---|---|---|
| 1 | `<use-case path>` | `<system behavior covered>` |

## Workplan

The workplan records past, current, and future slices for this architecture
surface. It should link to implementation reports, conformance reviews, briefs,
and future candidate slices without embedding full implementation detail.
Workplan entries are planning and evidence pointers only. Implementation
authority remains in accepted ADRs/specs/briefs and validation authority remains
in test output, implementation reports, and conformance reviews.

### Past Slices

| # | Slice | Evidence |
|---|---|---|
| 1 | `<slice name>` | `<implementation report / review path>` |

### Current Slice

| # | Slice | Exit Criteria |
|---|---|---|
| 1 | `<slice name>` | `<criteria>` |

### Future Slices

| # | Slice | Trigger |
|---|---|---|
| 1 | `<slice name>` | `<when to decompose>` |
````

## Compatibility notes

This format uses a JSON metadata block after the title instead of YAML
frontmatter before the title. Normalize architecture notes incrementally rather
than rewriting all existing notes at once.

Existing architecture notes that use YAML frontmatter remain valid until they are
explicitly migrated. The active template does not invalidate existing notes
solely because they use the older frontmatter style.
