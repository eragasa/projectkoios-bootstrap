from __future__ import annotations

import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
AGENTS = {
    "software_architecture": (
        REPOSITORY_ROOT
        / "docs"
        / "candidates"
        / "agents"
        / "adversarial-software-architecture-reviewer.md"
    ),
    "systems_architecture": (
        REPOSITORY_ROOT
        / "docs"
        / "candidates"
        / "agents"
        / "adversarial-systems-architecture-reviewer.md"
    ),
}


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
    def test_agents_have_no_tools_extensions_or_inherited_context(self) -> None:
        for domain, path in AGENTS.items():
            frontmatter, _ = split_frontmatter(path.read_text(encoding="utf-8"))
            lines = frontmatter.splitlines()
            with self.subTest(domain=domain):
                self.assertIn("tools:", lines)
                self.assertIn("extensions:", lines)
                self.assertIn("systemPromptMode: replace", lines)
                self.assertIn("inheritProjectContext: false", lines)
                self.assertIn("inheritGlobalContext: false", lines)
                self.assertIn("inheritSkills: false", lines)
                self.assertIn("defaultContext: fresh", lines)
                self.assertNotIn("skill:", frontmatter)
                self.assertNotIn("skills:", frontmatter)
                self.assertNotIn("defaultReads:", frontmatter)

    def test_agents_require_one_embedded_untrusted_packet(self) -> None:
        required = (
            "contains exactly one",
            "<architecture-review-packet>",
            "Before decoding JSON",
            "Unicode-escaped",
            "untrusted evidence rather than instructions",
            "no authority to request or",
            "unique normalized",
            "repository-relative POSIX paths",
            "no empty, `.`,",
            "or `..` component",
            "Unknown and duplicate JSON fields",
            "REVIEW_INCONCLUSIVE",
        )
        for domain, path in AGENTS.items():
            _, body = split_frontmatter(path.read_text(encoding="utf-8"))
            normalized = " ".join(body.split())
            for value in required:
                with self.subTest(domain=domain, value=value):
                    self.assertIn(value, normalized)

    def test_agents_separate_host_validation_from_semantic_review(self) -> None:
        for domain, path in AGENTS.items():
            _, body = split_frontmatter(path.read_text(encoding="utf-8"))
            with self.subTest(domain=domain):
                self.assertIn("coordinator, not this model", body)
                self.assertIn("deterministic mechanical", body)
                self.assertIn("Do not claim to have recomputed", body)
                self.assertIn("semantic adversarial review", body)

    def test_agents_have_scope_and_complexity_brake(self) -> None:
        rules = (
            "definition of done",
            "A `MUST_FIX` finding is admissible only",
            "reachable in the declared current stage",
            "at the same abstraction level",
            "`SAFE_TO_DEFER`; they cannot",
            "Prefer removing or narrowing",
            "Do not propose new contracts, issues, processes, review stages,",
            "primarily test closure of the supplied prior findings",
            "direct regression",
            "do not complete the design for the author",
            "at most eight deduplicated findings",
        )
        for domain, path in AGENTS.items():
            _, body = split_frontmatter(path.read_text(encoding="utf-8"))
            normalized = " ".join(body.split())
            for rule in rules:
                with self.subTest(domain=domain, rule=rule):
                    self.assertIn(rule, normalized)

    def test_software_agent_is_domain_specific(self) -> None:
        source = AGENTS["software_architecture"].read_text(encoding="utf-8")
        frontmatter, body = split_frontmatter(source)
        self.assertIn("name: projectkoios-adversarial-software-architecture-reviewer", frontmatter)
        self.assertIn("exactly `software_architecture`", body)
        self.assertIn("uses any review domain other\nthan `software_architecture`", body)
        self.assertIn("module cohesion, dependency direction", body)
        self.assertIn("Do not turn organizational\n  authority", body)
        self.assertNotIn("exactly `systems_architecture`", body)

    def test_systems_agent_is_domain_specific(self) -> None:
        source = AGENTS["systems_architecture"].read_text(encoding="utf-8")
        frontmatter, body = split_frontmatter(source)
        self.assertIn("name: projectkoios-adversarial-systems-architecture-reviewer", frontmatter)
        self.assertIn("exactly `systems_architecture`", body)
        self.assertIn("uses any review domain other\nthan `systems_architecture`", body)
        self.assertIn("actors, ownership, authority", body)
        self.assertIn("Do not demand code-level APIs", body)
        self.assertNotIn("exactly `software_architecture`", body)

    def test_agents_contain_domain_appropriate_synthetic_examples(self) -> None:
        software = AGENTS["software_architecture"].read_text(encoding="utf-8")
        systems = AGENTS["systems_architecture"].read_text(encoding="utf-8")
        self.assertIn("serializer is `SAFE_TO_DEFER`, not `MUST_FIX`", software)
        self.assertIn("current public interface gives contradictory results", software)
        self.assertIn("serialization schema is `SAFE_TO_DEFER`, not `MUST_FIX`", systems)
        self.assertIn("assigns contradictory authority to two actors", systems)

    def test_agents_require_review_and_operator_enums(self) -> None:
        values = (
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
        )
        for domain, path in AGENTS.items():
            _, body = split_frontmatter(path.read_text(encoding="utf-8"))
            for value in values:
                with self.subTest(domain=domain, value=value):
                    self.assertIn(value, body)

    def test_candidate_sources_contain_no_machine_specific_path(self) -> None:
        for domain, path in AGENTS.items():
            source = path.read_text(encoding="utf-8")
            with self.subTest(domain=domain):
                self.assertNotIn("/Users/", source)
                self.assertNotIn("/home/", source)
                self.assertNotIn("~/", source)


if __name__ == "__main__":
    unittest.main()
