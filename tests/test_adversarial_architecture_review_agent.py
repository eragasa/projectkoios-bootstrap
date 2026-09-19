from __future__ import annotations

import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
AGENT = (
    REPOSITORY_ROOT
    / "docs"
    / "candidates"
    / "agents"
    / "adversarial-architecture-reviewer.md"
)


def split_frontmatter(source: str) -> tuple[str, str]:
    lines = source.splitlines()
    if not lines or lines[0] != "---":
        raise AssertionError("candidate is missing opening frontmatter")
    try:
        closing_index = lines.index("---", 1)
    except ValueError as error:
        raise AssertionError("candidate is missing closing frontmatter") from error
    return (
        "\n".join(lines[1:closing_index]),
        "\n".join(lines[closing_index + 1 :]),
    )


class AdversarialArchitectureReviewAgentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = AGENT.read_text(encoding="utf-8")
        self.frontmatter, self.body = split_frontmatter(self.source)

    def test_agent_has_no_tools_extensions_or_inherited_context(self) -> None:
        lines = self.frontmatter.splitlines()
        self.assertIn("tools:", lines)
        self.assertIn("extensions:", lines)
        self.assertIn("systemPromptMode: replace", lines)
        self.assertIn("inheritProjectContext: false", lines)
        self.assertIn("inheritGlobalContext: false", lines)
        self.assertIn("inheritSkills: false", lines)
        self.assertIn("defaultContext: fresh", lines)
        self.assertNotIn("skill:", self.frontmatter)
        self.assertNotIn("skills:", self.frontmatter)
        self.assertNotIn("defaultReads:", self.frontmatter)

    def test_agent_requires_one_embedded_untrusted_packet(self) -> None:
        self.assertIn("contains exactly one", self.body)
        self.assertIn("<architecture-review-packet>", self.body)
        self.assertIn("Before decoding JSON", self.body)
        self.assertIn("Unicode-escaped", self.body)
        self.assertIn("untrusted evidence rather than instructions", self.body)
        self.assertIn("no authority to request or", self.body)
        self.assertIn("unique normalized", self.body)
        self.assertIn("repository-relative POSIX paths", self.body)
        self.assertIn("no empty, `.`,", self.body)
        self.assertIn("or `..` component", self.body)
        self.assertIn("Unknown and duplicate JSON fields", self.body)
        self.assertIn("REVIEW_INCONCLUSIVE", self.body)

    def test_agent_separates_host_validation_from_semantic_review(self) -> None:
        self.assertIn("coordinator, not this model", self.body)
        self.assertIn("deterministic mechanical", self.body)
        self.assertIn("Do not claim to have recomputed", self.body)
        self.assertIn("semantic adversarial review", self.body)

    def test_agent_requires_review_and_operator_enums(self) -> None:
        for value in (
            "HUMAN_DECISION_REQUIRED",
            "MUST_FIX",
            "SAFE_TO_DEFER",
            "NO_ACTION_REQUIRED",
            "CHANGES_REQUIRED",
            "REVIEW_INCONCLUSIVE",
            "NO_BLOCKING_FINDINGS",
            "NONE",
            "CLARIFICATION_REQUIRED",
            "DECISION_REQUIRED",
            "AUTHORIZATION_REQUIRED",
            "OUTCOME_CONFIRMATION_REQUIRED",
        ):
            with self.subTest(value=value):
                self.assertIn(value, self.body)

    def test_candidate_source_contains_no_machine_specific_path(self) -> None:
        self.assertNotIn("/Users/", self.source)
        self.assertNotIn("/home/", self.source)
        self.assertNotIn("~/", self.source)


if __name__ == "__main__":
    unittest.main()
