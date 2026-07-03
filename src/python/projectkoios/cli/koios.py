from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path
import sys

from projectkoios.ingestors import AnswerFormat, App


class Command:
    def __init__(self) -> None:
        self._app = App()

    def register(self, subparsers) -> None:
        parser: ArgumentParser = subparsers.add_parser(
            "koios",
            help="Koios GraphRAG command surface",
        )
        koios_sub = parser.add_subparsers(dest="action")
        koios_sub.required = True

        validate_parser = koios_sub.add_parser("validate", help="Validate Koios GraphRAG config")
        validate_parser.add_argument("--config", type=Path, default=Path("projectkoios.ingestion.config"))
        validate_parser.add_argument("--schema", type=Path, default=None)
        validate_parser.add_argument("--preset", default=None)
        validate_parser.set_defaults(func=self.run_validate)

        query_parser = koios_sub.add_parser("query", help="Answer a query from Koios GraphRAG")
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
        report = self._app.validate_config(args.config, schema_path=args.schema, preset=args.preset)
        print(
            f"koios validate: schema={report.schema_valid} runtime={report.runtime_valid} sources={report.sources}"
        )
        for issue in report.issues:
            print(f"  issue: {issue}")
        raise SystemExit(0 if report.schema_valid and report.runtime_valid else 1)

    def run_query(self, args: Namespace) -> None:
        answer = self._app.answer(
            args.config,
            args.question,
            schema_path=args.schema,
            format=AnswerFormat(args.format),
            preset=args.preset,
        )
        print(answer.text)


def register(subparsers) -> None:
    Command().register(subparsers)
