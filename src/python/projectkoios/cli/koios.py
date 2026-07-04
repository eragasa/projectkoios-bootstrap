from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any, TypeAlias

from projectkoios.ingestors import Answer, AnswerFormat, App, PersistedIndexReport, ValidationReport


SubparserCollection: TypeAlias = Any


class Command:
    """Koios GraphRAG CLI command adapter."""

    def __init__(self) -> None:
        self.app: App = App()

    def register(self, subparsers: SubparserCollection) -> None:
        """Register Koios GraphRAG commands on a parent subparser collection.

        Args:
            subparsers: Parent argparse subparser collection receiving the command group.
        """

        # Parser owns the top-level Koios GraphRAG command group.
        parser: ArgumentParser = subparsers.add_parser(
            "koios",
            help="Koios GraphRAG command surface",
        )
        # Koios subparsers dispatch validate, index, and query actions.
        koios_subparsers: SubparserCollection = parser.add_subparsers(dest="action")
        koios_subparsers.required = True

        # Validate parser checks GraphRAG configuration without building an index.
        validate_parser: ArgumentParser = koios_subparsers.add_parser("validate", help="Validate Koios GraphRAG config")
        validate_parser.add_argument("--config", type=Path, default=Path("projectkoios.ingestion.config"))
        validate_parser.add_argument("--schema", type=Path, default=None)
        validate_parser.add_argument("--preset", default=None)
        validate_parser.set_defaults(func=self.run_validate)

        # Index parser groups persisted-index operations.
        index_parser: ArgumentParser = koios_subparsers.add_parser("index", help="Build or inspect Koios GraphRAG indexes")
        # Index subparsers dispatch concrete index actions.
        index_subparsers: SubparserCollection = index_parser.add_subparsers(dest="index_action")
        index_subparsers.required = True
        # Build parser creates the persisted Koios GraphRAG index.
        build_parser: ArgumentParser = index_subparsers.add_parser("build", help="Build the persisted Koios GraphRAG index")
        build_parser.add_argument("--config", type=Path, default=Path("projectkoios.ingestion.config"))
        build_parser.add_argument("--schema", type=Path, default=None)
        build_parser.add_argument("--preset", default=None)
        build_parser.set_defaults(func=self.run_index_build)

        # Query parser answers one GraphRAG question.
        query_parser: ArgumentParser = koios_subparsers.add_parser("query", help="Answer a query from Koios GraphRAG")
        query_parser.add_argument("--config", type=Path, default=Path("projectkoios.ingestion.config"))
        query_parser.add_argument("--schema", type=Path, default=None)
        query_parser.add_argument("--preset", default=None)
        query_parser.add_argument("--question", required=True)
        query_parser.add_argument(
            "--format",
            choices=[item.value for item in AnswerFormat],
            default=AnswerFormat.CITED_SUMMARY.value,
        )
        query_parser.set_defaults(func=self.run_query)

    def run_validate(self, args: Namespace) -> None:
        """Run Koios GraphRAG config validation and exit with validation status.

        Args:
            args: Parsed CLI namespace containing config, schema, and preset options.
        """

        # Report contains schema and runtime validation results from the application layer.
        report: ValidationReport = self.app.validate_config(args.config, schema_path=args.schema, preset=args.preset)
        print(
            f"koios validate: schema={report.schema_valid} runtime={report.runtime_valid} sources={report.sources}"
        )
        issue: str
        for issue in report.issues:
            print(f"  issue: {issue}")
        raise SystemExit(0 if report.schema_valid and report.runtime_valid else 1)

    def run_index_build(self, args: Namespace) -> None:
        """Build the persisted Koios GraphRAG index.

        Args:
            args: Parsed CLI namespace containing config, schema, and preset options.
        """

        # Report summarizes persisted index output and indexed source counts.
        report: PersistedIndexReport = self.app.persist_index(args.config, schema_path=args.schema, preset=args.preset)
        print(
            "koios index build: "
            f"output={report.output_path} sources={report.sources} sections={report.sections}"
        )

    def run_query(self, args: Namespace) -> None:
        """Answer a Koios GraphRAG question.

        Args:
            args: Parsed CLI namespace containing config, question, schema, format, and preset options.
        """

        # Answer contains the formatted response text returned by the application layer.
        answer: Answer = self.app.answer(
            args.config,
            args.question,
            schema_path=args.schema,
            format=AnswerFormat(args.format),
            preset=args.preset,
        )
        print(answer.text)


def register(subparsers: SubparserCollection) -> None:
    """Register Koios GraphRAG commands on a parent subparser collection.

    Args:
        subparsers: Parent argparse subparser collection receiving the command group.
    """

    Command().register(subparsers)
