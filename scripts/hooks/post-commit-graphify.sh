#!/usr/bin/env bash
# Post-commit hook: rebuild graphify graph (AST-only, no LLM) when committed
# files match docs/** or src/**. Exits fast otherwise to avoid taxing every
# commit. Skips silently if graphify is unavailable or no graphify-out exists.
set -eu

# Only run if a graphify graph already exists in this repo.
if [ ! -d "graphify-out" ]; then
  exit 0
fi

# Check if any committed file matches docs/** or src/**
changed=$(git diff --cached --name-only --diff-filter=ACMR HEAD~1 HEAD 2>/dev/null | grep -E '^(docs/|src/)' || true)
if [ -z "$changed" ]; then
  exit 0
fi

# Find graphify binary
if ! command -v graphify >/dev/null 2>&1; then
  exit 0
fi

# Run AST-only update in background to avoid blocking the commit; output to log.
nohup graphify update . > /tmp/graphify-post-commit.log 2>&1 &
