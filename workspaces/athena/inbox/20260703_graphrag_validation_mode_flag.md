# GraphRAG validation mode flag

## Decision
Use **strict fail-fast** validation by default.

## Override
Make the runtime validator switchable with a flag so the behavior can be relaxed later without redesigning the pipeline.

## Suggested config shape
```yaml
validation:
  mode: strict
```

Allowed values:
- `strict` — stop on first validation failure
- `warn` — report issues but continue

## Rationale
- strict mode is safer for scientific workflows
- fail-fast prevents invalid runs from polluting results
- a flag keeps the implementation flexible
- the behavior can be flipped without changing the architecture

## Recommendation
Implement the validator as a small OOP component with a mode flag, so the policy is easy to change later.
