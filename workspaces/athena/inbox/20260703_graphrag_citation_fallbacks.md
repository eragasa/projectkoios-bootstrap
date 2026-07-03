# GraphRAG citation fallbacks

## Decision
Support multiple citation formats with fallback rules.

## Citation fields
A source may provide:
- BibTeX, if bibliographic metadata exists
- page number, if the source is paginated
- section heading, if available
- file:line, as the universal fallback

## Rule
The engine must emit the strongest citation supported by the source.
It must not require unsupported citation fields.

## Fallback order
1. BibTeX + page
2. page + section
3. section + file:line
4. file:line only

## Consequences
- heterogeneous sources remain usable
- citation quality is maximized where possible
- line-only sources still participate cleanly
- the engine stays generic across document types
