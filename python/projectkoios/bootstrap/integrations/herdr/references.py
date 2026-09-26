"""Reviewed Herdr references for the session-continuity integration.

Runtime behavior is intentionally pinned to the Herdr 0.9.1 documentation
baseline. Stable documentation URLs help operators; immutable source URLs make
the exact reviewed semantics inspectable after the upstream site changes.
"""

from __future__ import annotations

from dataclasses import dataclass

HERDR_DOCUMENTATION_BASELINE = "0.9.1"
HERDR_PI_RESTORE_MINIMUM_INTEGRATION_VERSION = 2


@dataclass(frozen=True, slots=True)
class HerdrReference:
    """One official Herdr page and its immutable reviewed source."""

    topic: str
    documentation_url: str
    versioned_source_url: str


HERDR_REFERENCES = (
    HerdrReference(
        topic="agent guide",
        documentation_url="https://herdr.dev/agent-guide.md",
        versioned_source_url=(
            "https://raw.githubusercontent.com/herdrdev/herdr/v0.9.1/"
            "distribution/agent-guide.md"
        ),
    ),
    HerdrReference(
        topic="quick start",
        documentation_url="https://herdr.dev/docs/quick-start/",
        versioned_source_url=(
            "https://raw.githubusercontent.com/herdrdev/herdr/v0.9.1/"
            "docs/next/website/src/content/docs/quick-start.mdx"
        ),
    ),
    HerdrReference(
        topic="persistence and remote access",
        documentation_url="https://herdr.dev/docs/persistence-remote/",
        versioned_source_url=(
            "https://raw.githubusercontent.com/herdrdev/herdr/v0.9.1/"
            "docs/next/website/src/content/docs/persistence-remote.mdx"
        ),
    ),
    HerdrReference(
        topic="session state and restore",
        documentation_url="https://herdr.dev/docs/session-state/",
        versioned_source_url=(
            "https://raw.githubusercontent.com/herdrdev/herdr/v0.9.1/"
            "docs/next/website/src/content/docs/session-state.mdx"
        ),
    ),
    HerdrReference(
        topic="CLI reference",
        documentation_url="https://herdr.dev/docs/cli-reference/",
        versioned_source_url=(
            "https://raw.githubusercontent.com/herdrdev/herdr/v0.9.1/"
            "docs/next/website/src/content/docs/cli-reference.mdx"
        ),
    ),
    HerdrReference(
        topic="integrations",
        documentation_url="https://herdr.dev/docs/integrations/",
        versioned_source_url=(
            "https://raw.githubusercontent.com/herdrdev/herdr/v0.9.1/"
            "docs/next/website/src/content/docs/integrations.mdx"
        ),
    ),
)

__all__ = [
    "HERDR_DOCUMENTATION_BASELINE",
    "HERDR_PI_RESTORE_MINIMUM_INTEGRATION_VERSION",
    "HERDR_REFERENCES",
    "HerdrReference",
]
