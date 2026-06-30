# AAR 20260701.031500: Ollama Manifest-Wide Batching

## Scope

Expanded daemon chunk-card generation from the small Graphify chunk list to manifest-wide batching.

## What happened

The daemon was only processing the `.graphify_chunks.json` bucket output, which represented a narrower slice than the repository corpus Graphify had indexed. I changed the Ollama input path to prefer Graphify's `manifest.json` and batch the indexed files across the corpus, with the old chunk list kept as fallback.

## Process issues

The earlier implementation made the daemon look like it was covering the whole repository when it was really only covering the chunk bucket structure.

## Proposed follow-up improvements

Record batch source and indexed-file counts in run metadata so coverage is visible without reading logs.

## Candidate ADR or implementation topics

Daemon coverage diagnostics and manifest/provenance reporting.

## Current status

The daemon now batches across the Graphify manifest, which is a much broader representation of the repository corpus.
