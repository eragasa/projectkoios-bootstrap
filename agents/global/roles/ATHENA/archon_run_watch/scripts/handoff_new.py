"""Create handoff files with correct naming and headers."""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
from datetime import datetime
from pathlib import Path
import re
import sys


def slugify(topic: str) -> str:
    """Convert *topic* to a deterministic lowercase slug."""
    lowercase_topic: str = topic.lower()
    hyphenated_topic: str = lowercase_topic.replace("_", "-")
    alphanumeric_topic: str = re.sub(r"[^a-z0-9-]", "-", hyphenated_topic)
    collapsed_topic: str = re.sub(r"-+", "-", alphanumeric_topic)
    return collapsed_topic.strip("-")


def render_fields(
    origin: str,
    from_: str,
    to: str,
    status: str = "draft",
    acting_as: str | None = None,
    scope: str | None = None,
    repository: str | None = None,
    delegated_operator: str | None = None,
) -> str:
    """Render handoff header fields in canonical order."""
    lines: list[str] = [
        f"Origin: {origin}",
        f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"From: {from_}",
        f"To: {to}",
        f"Status: {status}",
    ]
    if acting_as:
        lines.append(f"Acting-As: {acting_as}")
    if scope:
        lines.append(f"Scope: {scope}")
    if repository:
        lines.append(f"Repository: {repository}")
    if delegated_operator:
        lines.append(f"Delegated-Operator: {delegated_operator}")
    return "\n".join(lines) + "\n"


def build_parser() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(description="Create a handoff artifact file")
    parser.add_argument("--dir", required=True, type=Path, help="Target directory")
    parser.add_argument("--topic", required=True, help="Topic for filename slug")
    parser.add_argument("--origin", required=True, help="Origin header value")
    parser.add_argument("--from", dest="from_", required=True, help="From header value")
    parser.add_argument("--to", required=True, help="To header value")
    parser.add_argument("--status", default="draft", help="Status header value (default: draft)")
    parser.add_argument("--acting-as", help="Acting-As header value")
    parser.add_argument("--scope", help="Scope header value")
    parser.add_argument("--repository", help="Repository header value")
    parser.add_argument("--delegated-operator", help="Delegated-Operator header value")
    parser.add_argument("--title", help="Markdown H1 title for the handoff body")
    parser.add_argument("--body-file", type=Path, help="Read handoff body from file")
    return parser


def render_body(args: Namespace) -> list[str]:
    body: list[str] = []
    if args.title:
        body.append(f"# {args.title}")
        body.append("")
    if args.body_file:
        body.append(args.body_file.read_text(encoding="utf-8").rstrip())
        body.append("")
    return body


def main() -> None:
    args: Namespace = build_parser().parse_args()

    now: datetime = datetime.now()
    slug: str = slugify(args.topic)
    timestamp: str = now.strftime("%Y%m%d.%H%M%S")
    filename: str = f"{timestamp}_{slug}.md"
    path: Path = args.dir.resolve() / filename

    if path.exists():
        print(f"error: file already exists: {path}", file=sys.stderr)
        sys.exit(1)

    args.dir.resolve().mkdir(parents=True, exist_ok=True)

    header_block: str = render_fields(
        origin=args.origin,
        from_=args.from_,
        to=args.to,
        status=args.status,
        acting_as=args.acting_as,
        scope=args.scope,
        repository=args.repository,
        delegated_operator=args.delegated_operator,
    )

    body: list[str] = render_body(args)
    content: str = header_block + "\n" + "\n".join(body) if body else header_block

    path.write_text(content, encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
