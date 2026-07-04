from __future__ import annotations

from pathlib import Path
import json
import textwrap

from projectkoios.ingestors.schemas import JsonObject


def write_schema(root: Path) -> Path:
    """Write a minimal ingestion configuration schema fixture."""
    # Schema mirrors the ingestion config shape used by package tests.
    schema: JsonObject = {
        "title": "projectkoios.ingestion.config",
        "type": "object",
        "required": ["version", "project", "pipeline", "validation", "source", "ontology", "extraction", "retrieval", "evaluation", "presets"],
        "properties": {
            "version": {"type": "integer"},
            "project": {"type": "string"},
            "pipeline": {
                "type": "object",
                "required": ["mode", "answer_format", "retrieval_depth", "index_path"],
                "properties": {
                    "mode": {"type": "string", "enum": ["derived-index"]},
                    "answer_format": {"type": "string", "enum": ["cited_summary", "structured_json"]},
                    "retrieval_depth": {"type": "integer"},
                    "index_path": {"type": "string"},
                },
                "additionalProperties": False,
            },
            "validation": {"type": "object", "required": ["mode"], "properties": {"mode": {"type": "string", "enum": ["strict", "relaxed"]}}, "additionalProperties": False},
            "source": {"type": "object", "required": ["include", "exclude"], "properties": {"include": {"type": "array", "items": {"type": "string"}}, "exclude": {"type": "array", "items": {"type": "string"}}}, "additionalProperties": False},
            "ontology": {"type": "object"},
            "extraction": {
                "type": "object",
                "required": ["backend"],
                "properties": {"backend": {"type": "object", "required": ["name", "model", "timeout_seconds", "on_failure"], "properties": {"name": {"type": "string", "enum": ["ollama"]}, "endpoint": {"type": "string"}, "model": {"type": "string"}, "timeout_seconds": {"type": "integer"}, "on_failure": {"type": "string", "enum": ["error", "fallback"]}}, "additionalProperties": False}},
                "additionalProperties": False,
            },
            "retrieval": {"type": "object", "required": ["max_nodes"], "properties": {"max_nodes": {"type": "integer"}}, "additionalProperties": False},
            "evaluation": {"type": "object"},
            "presets": {"type": "object"},
        },
        "additionalProperties": False,
    }
    # Schema path is returned to callers for config loader construction.
    schema_path: Path = root / "projectkoios.ingestion.schema.json"
    schema_path.write_text(json.dumps(schema, indent=2), encoding="utf-8")
    return schema_path


def write_config(root: Path) -> Path:
    """Write a minimal ingestion configuration and ADR source fixture."""
    # ADR directory contains the source file matched by the config include glob.
    adr: Path = root / "docs" / "adr"
    adr.mkdir(parents=True, exist_ok=True)
    (adr / "adr.example.md").write_text(
        "# ADR Example\n\n## Status\n\ndraft\n\n## Context\n\nExample context.\n",
        encoding="utf-8",
    )
    # Config text exercises the complete ingestion pipeline with local fixture paths.
    config: str = textwrap.dedent(
        """
        version: 1
        project: projectkoios
        pipeline:
          mode: derived-index
          answer_format: cited_summary
          retrieval_depth: 1
          index_path: graph/index.json
        validation:
          mode: strict
        source:
          include:
            - docs/adr/**/*.md
          exclude: []
        ontology: {}
        extraction:
          backend:
            name: ollama
            endpoint: http://localhost:11434
            model: llama3.2
            timeout_seconds: 60
            on_failure: error
        retrieval:
          max_nodes: 1
        evaluation: {}
        presets:
          adr:
            source:
              include:
                - docs/adr/**/*.md
              exclude: []
        """
    ).strip()
    # Config path is returned to callers as the application input.
    config_path: Path = root / "projectkoios.ingestion.config"
    config_path.write_text(config, encoding="utf-8")
    return config_path
