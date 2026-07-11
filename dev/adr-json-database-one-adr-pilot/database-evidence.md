# ADR JSON/document-store pilot database evidence

Status: pilot-derived/non-authoritative evidence.

## Storage adapter policy

ADR workflow logic uses an ADR adapter wrapper over a generic JSON document store. SQLite is the selected pilot document-store backend only.

## SQLite operational store policy

Generated database path during run: `/Users/eugene/repos/projectkoios-bootstrap/dev/adr-json-database-one-adr-pilot/generated-local/pilot.sqlite`

Mutable `.sqlite`/`.db` files are local/generated and are not committed as repository authority.

## SQLite document-store DDL

```sql
CREATE TABLE IF NOT EXISTS json_documents (
  document_id TEXT PRIMARY KEY NOT NULL,
  document_kind TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  content_hash TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
)
```

## SQLite document-store index

```sql
CREATE INDEX IF NOT EXISTS idx_json_documents_kind
ON json_documents (document_kind, document_id)
```

## Replaced ADR-specific table

The previous `adr_records` table and ADR-specific query columns are retained only as historical migration evidence.

## Adapter query evidence

`list_by_kind(DocumentType.ADR)` returned: `adr.json-database-for-adr-storage`

## JSON checkpoint hash

`0bb030d8f33bd1081f5415871431e10aeb943d23d00dd346dc91b645ede45d04`
