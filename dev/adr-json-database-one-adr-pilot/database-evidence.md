# ADR JSON/database pilot database evidence

Status: pilot-derived/non-authoritative evidence.

## Storage adapter policy

ADR workflow logic uses a narrow storage adapter boundary. SQLite is the selected pilot adapter implementation only.

## SQLite operational store policy

Generated database path during run: `/Users/eugene/repos/projectkoios-bootstrap/dev/adr-json-database-one-adr-pilot/generated-local/pilot.sqlite`

Mutable `.sqlite`/`.db` files are local/generated and are not committed as repository authority.

## SQLite adapter DDL

```sql
CREATE TABLE IF NOT EXISTS adr_records (
  id TEXT PRIMARY KEY,
  slug TEXT NOT NULL,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  routing_owner TEXT NOT NULL,
  routing_next_phase TEXT NOT NULL,
  schema_id TEXT NOT NULL,
  content_hash TEXT NOT NULL,
  record_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
)
```

## Adapter query evidence

`list_by_status('draft')` returned: `adr.json-database-for-adr-storage`

## JSON checkpoint hash

`9e2bd6ed13f8cfa2d9e8b63c444248f19da960e818f22eb3d8a516bcebefb55e`
