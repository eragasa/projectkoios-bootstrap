"""Create handoff files with correct naming and headers."""

from __future__ import annotations

from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
import re
import sys


def slugify(topic: str) -> str:
    """Convert *topic* to a deterministic lowercase slug.

    - Lowercase
    - Spaces and underscores to hyphens
    - Strip non-alphanumeric except hyphens
    - Collapse consecutive hyphens
    - Strip leading/trailing hyphens
    """
    s = topic.lower()
    s = s.replace("_", "-")
    s = re.sub(r"[^a-z0-9-]", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


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
    p = ArgumentParser(description="Create a handoff artifact file")
    p.add_argument("--dir", required=True, type=Path, help="Target directory")
    p.add_argument("--topic", required=True, help="Topic for filename slug")
    p.add_argument("--origin", required=True, help="Origin header value")
    p.add_argument("--from", dest="from_", required=True, help="From header value")
    p.add_argument("--to", required=True, help="To header value")
    p.add_argument("--status", default="draft", help="Status header value (default: draft)")
    p.add_argument("--acting-as", help="Acting-As header value")
    p.add_argument("--scope", help="Scope header value")
    p.add_argument("--repository", help="Repository header value")
    p.add_argument("--delegated-operator", help="Delegated-Operator header value")
    p.add_argument("--title", help="Markdown H1 title for the handoff body")
    p.add_argument("--body-file", type=Path, help="Read handoff body from file")
    return p


def main() -> None:
    args = build_parser().parse_args()

    now = datetime.now()
    slug = slugify(args.topic)
    timestamp = now.strftime("%Y%m%d.%H%M%S")
    filename = f"{timestamp}_{slug}.md"
    path = args.dir.resolve() / filename

    if path.exists():
        print(f"error: file already exists: {path}", file=sys.stderr)
        sys.exit(1)

    args.dir.resolve().mkdir(parents=True, exist_ok=True)

    header_block = render_fields(
        origin=args.origin,
        from_=args.from_,
        to=args.to,
        status=args.status,
        acting_as=args.acting_as,
        scope=args.scope,
        repository=args.repository,
        delegated_operator=args.delegated_operator,
    )

    body: list[str] = []
    if args.title:
        body.append(f"# {args.title}")
        body.append("")
    if args.body_file:
        body.append(args.body_file.read_text(encoding="utf-8").rstrip())
        body.append("")

    content = header_block + "\n" + "\n".join(body) if body else header_block

    path.write_text(content, encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
