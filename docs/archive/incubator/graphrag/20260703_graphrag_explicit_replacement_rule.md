# GraphRAG explicit replacement rule draft

## Rule

Use explicit replacement for config overlays.

## Meaning

If a preset changes a section, it must restate the full section it intends to use.
No hidden deep-merge inheritance is allowed.

## Rationale

- deterministic behavior
- reproducible experiments
- auditable configuration
- no implicit fallback values
- clearer scientific comparison across runs

## Example

### Base
```yaml
retrieval:
  strategy: 1-hop
  max_nodes: 25
```

### Overlay
```yaml
retrieval:
  strategy: 2-hop
  max_nodes: 50
```

### Result
The overlay fully replaces `retrieval`.

## Consequences

- presets are more verbose
- config readers can see the exact experimental state
- each run is self-contained and easier to compare
