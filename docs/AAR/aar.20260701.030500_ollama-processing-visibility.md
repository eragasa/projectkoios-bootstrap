# AAR 20260701.030500: Ollama Processing Visibility

## Scope

Improved visibility into whether the Graphify daemon is actually sending work to Ollama.

## What happened

Added explicit `[ollama]` log lines for connectivity checks, chunk selection, per-chunk processing, failures, and completion summaries. Verified the daemon now shows when it is trying to process chunks and when chunk generation fails.

## Process issues

The first inspection showed the daemon reporting `cards=0` without making it obvious whether Ollama had been invoked or whether chunk input shape was the problem.

## Proposed follow-up improvements

Consider recording Ollama model/endpoint metadata in run metadata and adding a small output sample or count of readable chunk content.

## Candidate ADR or implementation topics

Daemon run metadata enrichment for Ollama diagnostics.

## Current status

Ollama activity is now visible in daemon logs; actual chunk generation still needs a working local Ollama response path.
