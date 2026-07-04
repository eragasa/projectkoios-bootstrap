from __future__ import annotations

import re


HEADER_FIELD_PATTERN = re.compile(r"^([A-Za-z][A-Za-z0-9_-]+):\s*(.*)$")
"""Matches ``Key: value`` lines in handoff file headers."""


def extract_handoff_headers(text: str) -> dict[str, str]:
    """Extract header field key-value pairs from the top of *text*.

    Scanning stops at the first non-header line (blank line or prose).
    Duplicate keys overwrite — the last occurrence wins.
    """
    fields: dict[str, str] = {}
    for line in text.splitlines():
        match: re.Match[str] | None = HEADER_FIELD_PATTERN.match(line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
        elif fields:
            break
    return fields
