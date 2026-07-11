# ADR JSON schemas conformance database evidence

Status: active conformance record evidence.

## Storage adapter policy

ADR conformance logic uses an ADR adapter wrapper over a generic JSON document store. SQLite is the selected generated-local backend only.

## SQLite operational store policy

Generated database path during run: `/Users/eugene/repos/projectkoios-bootstrap/dev/adr-json-schemas-conformance/generated-local/conformance.sqlite`

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

## Adapter query evidence

`list_by_kind(DocumentType.ADR)` returned: `adr.json-schemas`

## JSON checkpoint hash

`e5f8c6729ee120ae4a266e6d5d575df3b9ae6f9fb86158c92a29995386a89bfb`
