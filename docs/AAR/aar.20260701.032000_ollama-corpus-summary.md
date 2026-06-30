# AAR 20260701.032000: Ollama Corpus Summary

## Scope

Added visible corpus coverage summary for the Graphify/Ollama daemon.

## What happened

The daemon now logs and records eligible-file, indexed-file, batch, and skipped-file counts before chunk generation, so it is easier to see whether Ollama is working on the broader Graphify corpus or falling back to a narrower input set.

## Process issues

The previous implementation made it hard to distinguish corpus-wide coverage from batch-level processing.

## Proposed follow-up improvements

If coverage still looks unexpectedly narrow, consider promoting a clearer repo-supported-file count into the run metadata or adding a dedicated coverage report file.

## Candidate ADR or implementation topics

Daemon coverage reporting and Graphify-supported-file accounting.

## Current status

The daemon now prints and persists a corpus summary during Ollama processing.
