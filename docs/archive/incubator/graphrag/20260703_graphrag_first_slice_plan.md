# GraphRAG first slice plan

## Slice goal
Prove the smallest useful academic GraphRAG loop on ADRs only.

## Slice boundary
- source corpus: ADRs only
- retrieval: 1-hop default
- graph: derived index only
- config: `projectkoios.ingestion.config`
- output: cited answer
- validation: schema + runtime checks
- model backend: one implemented adapter only

## Build steps
1. define the config schema
2. implement config loading and preset resolution
3. validate config shape with JSON Schema
4. validate source paths/globs at runtime
5. ingest ADR files with deterministic structure extraction
6. build a small derived graph index
7. retrieve 1-hop evidence
8. emit cited summary output
9. support structured JSON output from prompt
10. keep backend selection pluggable behind an interface

## Slice constraints
- no AARs yet
- no workflow logs yet
- no deep merge overlays
- no hidden defaults from config inheritance
- no second backend implementation required yet
- no source authority mutation

## Success criteria
- a run can be configured without code edits
- ADR sources are discovered and indexed
- relevant sections are surfaced reliably
- answers include the strongest supported citation available
- the system remains easy to extend without redesign
