from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any

from projectkoios.ingestors import Answer, AnswerFormat, App, PersistedIndexReport, ValidationReport


class Command:
    def __init__(self) -> None:
        self.app: App = App()

    def register(self, subparsers) -> None:
        parser: ArgumentParser = subparsers.add_parser(
            "koios",
            help="Koios GraphRAG command surface",
        )
        koios_subparsers: Any = parser.add_subparsers(dest="action")
        koios_subparsers.required = True

        validate_parser: ArgumentParser = koios_subparsers.add_parser("validate", help="Validate Koios GraphRAG config")
        validate_parser.add_argument("--config", type=Path, default=Path("projectkoios.ingestion.config"))
        validate_parser.add_argument("--schema", type=Path, default=None)
        validate_parser.add_argument("--preset", default=None)
        validate_parser.set_defaults(func=self.run_validate)

        index_parser: ArgumentParser = koios_subparsers.add_parser("index", help="Build or inspect Koios GraphRAG indexes")
        index_subparsers: Any = index_parser.add_subparsers(dest="index_action")
        index_subparsers.required = True
        build_parser: ArgumentParser = index_subparsers.add_parser("build", help="Build the persisted Koios GraphRAG index")
        build_parser.add_argument("--config", type=Path, default=Path("projectkoios.ingestion.config"))
        build_parser.add_argument("--schema", type=Path, default=None)
        build_parser.add_argument("--preset", default=None)
        build_parser.set_defaults(func=self.run_index_build)

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
        report: ValidationReport = self.app.validate_config(args.config, schema_path=args.schema, preset=args.preset)
        print(
            f"koios validate: schema={report.schema_valid} runtime={report.runtime_valid} sources={report.sources}"
        )
        issue: str
        for issue in report.issues:
            print(f"  issue: {issue}")
        raise SystemExit(0 if report.schema_valid and report.runtime_valid else 1)

    def run_index_build(self, args: Namespace) -> None:
        report: PersistedIndexReport = self.app.persist_index(args.config, schema_path=args.schema, preset=args.preset)
        print(
            "koios index build: "
            f"output={report.output_path} sources={report.sources} sections={report.sections}"
        )

    def run_query(self, args: Namespace) -> None:
        answer: Answer = self.app.answer(
            args.config,
            args.question,
            schema_path=args.schema,
            format=AnswerFormat(args.format),
            preset=args.preset,
        )
        print(answer.text)


def register(subparsers) -> None:
    Command().register(subparsers)
