# Architecture conformance review 20260708.052436: Template representation round-trip first slice

## Status

conforms-to-original-brief; packaging-blocked-by-schema-backed-revision

## Provenance

- Acting-As: ATHENA
- Repository: projectkoios-bootstrap
- Workspace: workspaces/athena/
- Requested by: VULCAN via intercom after user request
- Source brief: `docs/plans/implementation-brief.20260708.041245_template-representation-roundtrip.md`
- Implementation report: `docs/implementation/template-representation-roundtrip.20260708.044531.md`
- Implementation package: `src/python/projectkoios/bootstrap/template_representation/`
- Tests: `tests/projectkoios/bootstrap/template_representation/`

## Review scope

ATHENA reviewed the implemented first-slice template representation package against the implementation brief and authority boundary. This review covers architecture/spec conformance only; VULCAN remains owner of implementation, tests, validation, implementation reports, and deviation reports.

## Inspected artifacts

- `src/python/projectkoios/bootstrap/template_representation/__init__.py`
- `src/python/projectkoios/bootstrap/template_representation/models.py`
- `src/python/projectkoios/bootstrap/template_representation/markdown.py`
- `src/python/projectkoios/bootstrap/template_representation/paths.py`
- `tests/projectkoios/bootstrap/template_representation/test__TemplateRepresentation__roundtrip.py`
- `docs/templates/ADR.proposal.template.md`
- `docs/implementation/template-representation-roundtrip.20260708.044531.md`
- `docs/AAR/aar.20260708.044531_template-representation-roundtrip.md`
- `docs/process-capture/pc.workflow.document-trace.20260708.044950Z.md`

## Validation and visual inspection rerun by ATHENA

```bash
cd /Users/eugene/repos/projectkoios-bootstrap
uv run pytest tests/projectkoios/bootstrap/template_representation -q
# 9 passed in 0.01s

uv run mypy src/python/projectkoios/bootstrap/template_representation tests/projectkoios/bootstrap/template_representation
# Success: no issues found in 5 source files

uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/template_representation tests/projectkoios/bootstrap/template_representation
# summary: 0 finding(s), 5 file(s)
```

ATHENA also visually inspected the implementation files and tests rather than relying only on the implementation report:

- `models.py`: confirmed `TemplateRecord`, `TemplateSection`, `TemplateMarker`, `TemplateNamespace`, and `NamespaceClassification` fields and serialization boundaries.
- `markdown.py`: confirmed `parse_file()` enforces the template namespace before reading, `parse()` builds the canonical record, heading ambiguity checks are explicit, deterministic marker detection is local, and `render()` preserves canonical order.
- `paths.py`: confirmed repo-relative namespace classification for `docs/templates/`, `docs/implementation/`, and `docs/plans/`.
- `test__TemplateRepresentation__roundtrip.py`: confirmed fixture construction, serialization, render parse-back, whitespace variance, typed parse failures, namespace classification, and non-template rejection tests.
- Parsed `docs/templates/ADR.proposal.template.md` and inspected the resulting record: 13 ordered sections, leading JSON preamble preserved, title `ADR: <Title>`, expected placeholder markers detected, and rendered Markdown is byte-identical to the source fixture.

ATHENA did not rerun the full VULCAN validation matrix, but the implementation report records full pytest, full mypy, full Python-policy validation, diff hygiene, and Graphify update as passing.

## Conformance findings

### 1. Package and test boundaries

Conforms.

The implementation uses the briefed package boundary:

- `src/python/projectkoios/bootstrap/template_representation/`
- `tests/projectkoios/bootstrap/template_representation/`

No new `src/python/ingestion/`, `projectkoios.ingestion`, or generic ingestion framework was introduced by this slice.

### 2. First fixture and round trip

Conforms.

The tests use the recommended first fixture `docs/templates/ADR.proposal.template.md` and prove:

- parsing the live fixture into a canonical record;
- JSON-compatible serialization/deserialization;
- deterministic Markdown rendering;
- Markdown render parse-back equivalence;
- allowed whitespace presentation variance.

This satisfies the brief's first-slice requirement to prove one template before broadening coverage.

### 3. Canonical representation behavior

Conforms.

`TemplateRecord`, `TemplateSection`, and `TemplateMarker` capture the required minimum fields: identifier, source path, title, ordered sections, section body text, deterministic markers, and representation version. The `preamble` and `lead_body` fields are justified by the live fixture's leading JSON block and title-to-first-section prose; they preserve fixture semantics without expanding into general ingestion.

### 4. Parser and renderer contract

Conforms for the first controlled slice.

The renderer preserves canonical order and emits deterministic Markdown. The parser rejects missing title, duplicate or ambiguous top-level headings, unsupported fourth-level heading depth, duplicate section headings, and non-template file parsing through `parse_file()` by default.

Nonblocking follow-up: `parse(markdown, source_path=...)` does not itself validate that `source_path` is under `docs/templates/`; `parse_file()` enforces that before reading files. This is acceptable for the current first-slice controlled tests, but if `parse()` becomes an external API, CLI surface, or validator entrypoint, VULCAN should add source-path namespace validation or document why direct string parsing is explicitly fixture/internal-only.

### 5. Namespace classification

Conforms.

`TemplateRepresentationPaths.classify()` distinguishes `docs/templates/`, `docs/implementation/`, and `docs/plans/`, and the tests cover these boundaries. The implementation does not reclassify implementation documents as templates.

### 6. Non-goals and authority boundary

Conforms.

ATHENA found no implementation evidence of:

- Graphify ingestion daemon changes;
- vault, PDF, source-crawling, or evidence ingestion;
- product-facing template architecture;
- broad all-template migration;
- ADR status or lifecycle changes;
- Athena-owned code implementation.

The implementation remains a bootstrap-local template representation slice.

## Blockers before packaging or commit

Post-review user correction: the implementation must parse down to a schema-backed record. The current implementation conforms to the original first-slice brief, but it only parses to Python dataclasses / JSON-compatible dictionaries and does not define or validate a canonical template record JSON Schema.

Packaging SHOULD pause pending `docs/plans/revision-request.20260708.070651_template-representation-schema-backed.md`, unless the user explicitly downgrades the schema-backed requirement.

## Residual risks

- The parser remains intentionally controlled-Markdown-only and should not be advertised as an arbitrary Markdown parser.
- The current marker detector is deterministic angle-bracket matching only; this matches the first slice but should be revisited before broader template coverage.
- Direct `parse(markdown, source_path=...)` namespace handling should be tightened or documented before adding public CLI/validator integration.

## Decision

ATHENA accepts the VULCAN implementation as conformant to the original source brief for the first-slice template representation round trip.

However, the user's subsequent schema-backed requirement changes the packaging gate. Recommended next state: VULCAN should implement `docs/plans/revision-request.20260708.070651_template-representation-schema-backed.md` before packaging/commit, unless the user explicitly narrows the requirement back to Python-local JSON-compatible records.
