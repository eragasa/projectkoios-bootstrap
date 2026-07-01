# Idea: JSON Database for ADR Storage

## Brainstorm

Maybe ADRs should live as JSON documents, with SQLite used to store or index them.

### Possible shapes

1. **JSON files on disk + SQLite index**
   - JSON is the source of truth
   - SQLite stores search/index metadata
   - best for git diffs and manual inspection

2. **SQLite as the database, JSON as payload**
   - each ADR is a row with JSON content
   - easy to query and filter
   - less friendly for direct editing

3. **Hybrid JSON DB**
   - JSON files stay canonical
   - SQLite mirrors the data for lookup, sorting, and joins
   - best if tooling is expected to do most writes

## Why this is interesting

- ADRs need structure
- filenames are awkward as the only lookup key
- status/title/routing are better indexed than grepped
- promotion from draft to active could become a metadata update instead of a manual rename problem

## Questions

- Should JSON files remain canonical?
- Should SQLite be cache only, or authoritative?
- Should promotion update filename, status, or both?
- Do we want full-text search over decision text?

## Lean recommendation

Use **JSON files as canonical storage** and **SQLite as an index/cache**.

That keeps:

- human-readable history
- easy git review
- stable schema evolution
- fast querying when needed

## Related ideas

- ADR title naming convention
- ADR filename naming convention
- draft vs active promotion rules
