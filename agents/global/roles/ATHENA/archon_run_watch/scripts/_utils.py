"""Shared utilities for archon_run_watch skill scripts."""

from __future__ import annotations

import json
import sys


def write_json(obj, file=sys.stdout, *, default=None) -> None:
    json.dump(obj, file, indent=2, default=default)
    file.write("\n")
