```json
{
  "title": "TypeScript coding rules",
  "artifact_type": "implementation-policy",
  "status": "draft",
  "datetime": "20260711.084000Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "scope": "TypeScript implementation in projectkoios-bootstrap",
  "owner": "VULCAN",
  "review_roles": ["KOIOS", "ATHENA"],
  "controls": ["src/typescript/", "tests/typescript/"],
  "does_not_control": ["architecture decisions", "product domain policy", "non-TypeScript implementation"]
}
```

# TypeScript coding rules

## 1. Status and authority

This document is draft VULCAN implementation policy.

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL are to be interpreted as described in RFC 2119 and RFC 8174 when, and only when, they appear in all capitals.

Architecture, ADRs, implementation briefs, and explicit user/HERMES/ATHENA direction remain controlling. This policy MUST NOT be used to create product architecture authority.

## 2. Scope

This policy applies to TypeScript source and TypeScript tests under `src/typescript/` and package-local TypeScript test directories.

Existing non-conforming code is remediation work. Touching a file SHOULD move the touched surface toward this policy unless the controlling work item states otherwise.

## 3. General requirements

TypeScript implementation MUST be small, explicit, typed, and testable.

Implementation MUST follow the controlling plan, brief, ADR, or accepted work item.

Implementation MUST NOT expand architecture scope for implementation convenience.

New package surfaces MUST compile with strict TypeScript checking.

Public exports, public methods, durable data contracts, and durable constants MUST have explicit types.

New implementation MUST NOT use `any`. Untrusted input SHOULD enter as `unknown` and be narrowed before use.

Modules MUST NOT create runtime side effects at import time, except for thin executable or browser entrypoints.

## 4. DataObject and ActionObject boundary

Durable data shape MUST live in DataObjects: interfaces, structural type aliases, immutable fixture objects, or explicit schemas.

Operational behavior MUST live in ActionObjects: classes or named objects such as `Renderer`, `Resolver`, `Provider`, `Factory`, `Adapter`, `Validator`, `Application`, or `Orchestrator`.

Durable implementation behavior MUST NOT be implemented as dangling or free module-level functions.

Thin entrypoints MAY wire ActionObjects, locate a DOM mount point, invoke the application, and fail fast on missing entrypoint state.

Test files MAY use local helper functions when that improves test readability.

Repeated fixture construction SHOULD use a Factory ActionObject.

## 5. Enumerated semantic values

Durable semantic values MUST be owned by scoped TypeScript `enum` classes.

This includes status, kind, category, mode, source type, disposition, state, boundary, and similar semantic sets.

Code MUST NOT represent durable semantic values as repeated string literals, dangling module constants, unowned `as const` maps, or string-literal union types.

String-literal unions MAY be used for narrow non-semantic local helper constraints.

Runtime values crossing JSON, config, URL, CLI, storage, or provider boundaries MUST be validated before use.

## 6. Module and runtime boundaries

Contracts, fixtures, renderers, providers, resolvers, adapters, and entrypoints SHOULD be separated when present.

Browser entrypoints MUST delegate to reusable ActionObjects.

UI renderers SHOULD be deterministic over typed input state.

UI and browser code MUST NOT perform live I/O unless explicitly approved by the controlling work item.

Browser code MUST NOT read live repository filesystem state.

Browser code MUST NOT use network calls, `fetch`, `WebSocket`, live session/intercom reads, or repo-state reads unless explicitly approved.

Fixture paths MUST be treated as provenance strings, not runtime filesystem dependencies.

## 7. I/O, generated artifacts, and dependencies

Node filesystem reads and writes MUST be isolated behind adapters or scripts.

Text generation MUST use UTF-8.

Review, fixture, and test JSON artifacts MUST be deterministic when committed or compared.

Implementation MUST NOT write outside documented output surfaces.

New dependencies MUST be justified by the source artifact or by clear maintenance-risk reduction.

Dependencies SHOULD be package-local unless repo-wide tooling is explicitly approved.

`node_modules/`, `dist/`, coverage, local preview state, live snapshots, sessions, secrets, and generated runtime state MUST NOT be committed.

Package lockfiles MAY be committed for package-local reproducibility. A package-local lockfile MUST NOT be treated as repo-wide lockfile policy unless that policy is explicitly accepted.

## 8. Errors and validation

Code MUST fail explicitly for unsupported modes, invalid refs, malformed config, invalid paths, missing fixtures, and unsupported providers.

Code MUST NOT silently swallow provider, parsing, validation, rendering, or persistence failures.

Broad `try`/`catch` blocks MUST NOT convert failures into `undefined`, `false`, empty collections, or other generic success-shaped values.

Errors SHOULD identify the failing field, ref, file, provider, or path.

## 9. Testing requirements

New behavior MUST have focused tests or explicit type-level validation.

Tests MUST avoid network access, live intercom/session state, model providers, and machine-local runtime state unless explicitly isolated and approved.

Review flows SHOULD test that proposal, evidence, and content refs resolve.

Read-only slices SHOULD test absence of mutation controls.

Type checking MUST be part of validation for TypeScript changes.

Slices establishing TypeScript convention SHOULD include a scan or review note showing:

- no exported or top-level free functions where the DataObject/ActionObject boundary applies;
- no enum-like semantic string literals outside enum classes.

## 10. UI and fixture requirements

Read-only or proposal-oriented UI MUST NOT expose activate, apply, save, or mutation controls unless explicitly approved.

Fixture-backed status MUST be visibly marked fixture, static, stale-by-design, non-live, or equivalent.

UI copy SHOULD state authority boundaries for bootstrap-derived fixtures and evidence.

Fixture data MUST be deterministic and self-contained.

Fixture data MUST NOT contain secrets, credentials, private runtime transcripts, or live session state unless sanitized and explicitly approved.

Fixture evidence SHOULD include source locator, artifact type, content hash when practical, timestamp, freshness, provenance, authority boundary, transformation notes, and trust/confidence text.

## 11. Documentation and closeout

Package README files SHOULD list commands, fixture policy, authority boundaries, and extraction notes.

Implementation reports MUST list meaningful changed files, validation evidence, dependency and lockfile decisions, deviations, and residual risks.

VULCAN SHOULD self-review TypeScript changes against this policy before closeout.

KOIOS MAY review provenance quality.

ATHENA MAY review conformance to architecture and specification artifacts.

## 12. Non-goals

This policy does not define product architecture, UI/UX product policy, non-TypeScript coding rules, or feature-specific acceptance criteria.
