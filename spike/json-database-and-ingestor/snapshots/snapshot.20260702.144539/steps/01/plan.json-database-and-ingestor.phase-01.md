# Phase P1 — Document model + DocumentType enum

**Files:**
- `src/python/projectkoios/bootstrap/storage/__init__.py` — package init, re-exports
- `src/python/projectkoios/bootstrap/storage/document.py` — Document dataclass, DocumentType enum

**What:**
- Define `DocumentType(Enum)` with `ADR`, `AAR`, `GENERIC`
- Define `Document` frozen dataclass: `id`, `doc_type`, `status`, `title`, `created_at`, `updated_at`, `body` (dict), `metadata` (dict)
- Define `DocumentStatus(Enum)` with `draft`, `active`, `archived`, `superseded`
- Validation: required fields, type constraints on status transitions

**Verification:** unit test creates Document instances, validates field constraints, tests enum membership.
