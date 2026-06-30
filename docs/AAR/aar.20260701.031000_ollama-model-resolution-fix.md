# AAR 20260701.031000: Ollama Model Resolution Fix

## Scope

Fixed the daemon's Ollama model selection so local runs use an installed model instead of failing every chunk.

## What happened

The daemon was logging repeated Ollama chunk failures even though Ollama was reachable. Inspection showed the configured default model name did not match the local registry, so the daemon now resolves a usable model from `/api/tags` before generating cards.

## Process issues

The failure mode was initially ambiguous because the daemon only logged generic chunk failures. We had to probe Ollama directly to identify the model mismatch.

## Proposed follow-up improvements

Record the resolved Ollama model in run metadata and surface request errors more explicitly when generation still fails.

## Candidate ADR or implementation topics

Daemon diagnostics and Ollama metadata reporting.

## Current status

The daemon now resolves `llama3.2:1b` locally and successfully generates chunk cards.
