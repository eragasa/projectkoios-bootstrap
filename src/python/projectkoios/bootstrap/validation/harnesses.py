from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path, PurePosixPath
import re

from projectkoios.bootstrap.models import HARNESSES


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass(frozen=True)
class Finding:
    severity: Severity
    message: str
    path: str | None = None


@dataclass(frozen=True)
class ValidationResult:
    findings: tuple[Finding, ...]

    def count(self, severity: Severity) -> int:
        return sum(1 for finding in self.findings if finding.severity is severity)

    def exit_code(self, *, strict: bool = False) -> int:
        if self.count(Severity.ERROR) > 0:
            return 1
        if strict and self.count(Severity.WARNING) > 0:
            return 1
        return 0


CANONICAL_FILES: dict[str, tuple[str, ...]] = {
    "AGENTS.md": (
        "## Harnesses",
        "## Meta-harness",
        "## Directions for all harnesses",
        "## Directions for Hermes (pi)",
        "## Directions for Athena (archon)",
        "## Directions for Vulcan (opencode)",
        "## Routing guide",
        "## Artifact handoff",
    ),
    "pi/AGENTS.md": (
        "## Direct capabilities",
        "## Delegation",
        "## Scope",
        "## Reference",
    ),
    "opencode/AGENTS.md": (
        "## Workspace layout",
        "## Rules",
        "## Checklists",
        "## Setup per repo",
        "## Common commands",
        "## Conventions",
    ),
    "goose/AGENT.md": (
        "## Domain",
        "## Maps",
        "## Vault rules",
        "## Handoff support",
    ),
    "doc/meta-harness.md": (
        "## Skill model",
        "## Disagreement handling",
        "## Completion gates",
        "## Escalation rules",
    ),
    "archon/prompts/harness-routing.md": (
        "## Harness definitions",
        "## Rules",
        "## Output requirement",
    ),
}

REFERENCE_ROOTS = (
    "architecture",
    "doc",
    "maps",
    "archon",
    "opencode",
    "goose",
    "pi",
    "agents/global",
    "scripts",
    "src/python",
)

LOCAL_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
INLINE_CODE_PATTERN = re.compile(r"`([^`\n]+)`")
_PATH_ROOT_PATTERN = "|".join(re.escape(r) for r in REFERENCE_ROOTS)
PATH_TOKEN_PATTERN = re.compile(
    r"(?:\.\./|\.\/)?(?:" + _PATH_ROOT_PATTERN + r")/[A-Za-z0-9._<>{}/~*-]+"
)


def validate_harnesses(root: Path, *, strict: bool = False) -> ValidationResult:
    root = root.resolve()
    findings: list[Finding] = []

    _check_canonical_files(root, findings)
    _check_references(root, findings)
    _check_opencode_references(root, findings)
    _check_bootstrap_assumptions(root, findings)
    _check_archon_workflows(root, findings)
    _check_global_examples(root, findings)

    findings.append(
        Finding(
            Severity.INFO,
            f"validated {len(CANONICAL_FILES)} canonical harness document(s)",
        )
    )
    return ValidationResult(tuple(findings))


def _check_canonical_files(root: Path, findings: list[Finding]) -> None:
    for rel_path, required_headings in CANONICAL_FILES.items():
        path = root / rel_path
        if not path.exists():
            findings.append(
                Finding(Severity.ERROR, "missing canonical harness file", rel_path)
            )
            continue

        text = path.read_text(encoding="utf-8")
        for heading in required_headings:
            if heading not in text:
                findings.append(
                    Finding(
                        Severity.ERROR,
                        f"missing required heading {heading!r}",
                        rel_path,
                    )
                )

    if (root / "goose/AGENTS.md").exists():
        findings.append(
            Finding(
                Severity.WARNING,
                "goose uses goose/AGENT.md as its canonical file; "
                "goose/AGENTS.md is not part of the manifest",
                "goose/AGENTS.md",
            )
        )


def _check_references(root: Path, findings: list[Finding]) -> None:
    for rel_path in _in_scope_markdown_files(root):
        path = root / rel_path
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for raw_ref in sorted(_extract_repo_refs(text)):
            resolved = _resolve_reference(root, rel_path, raw_ref)
            if resolved is None:
                continue
            display, target = resolved
            if not target.exists():
                findings.append(
                    Finding(
                        Severity.ERROR,
                        f"broken repo-local reference {display!r}",
                        rel_path,
                    )
                )


def _check_opencode_references(root: Path, findings: list[Finding]) -> None:
    rel_path = "opencode/AGENTS.md"
    path = root / rel_path
    if not path.exists():
        return

    text = path.read_text(encoding="utf-8")
    for ref in sorted(set(re.findall(r"`(rules/[^`]+\.md)`", text))):
        if not (root / "opencode" / ref).exists():
            findings.append(
                Finding(Severity.ERROR, f"missing opencode rule reference {ref!r}", rel_path)
            )
    for ref in sorted(set(re.findall(r"`(checklists/[^`]+\.md)`", text))):
        if not (root / "opencode" / ref).exists():
            findings.append(
                Finding(
                    Severity.ERROR,
                    f"missing opencode checklist reference {ref!r}",
                    rel_path,
                )
            )


def _check_bootstrap_assumptions(root: Path, findings: list[Finding]) -> None:
    required_paths = (
        "agents/global",
        "archon/workflows",
        "archon/skills/.archon/config.yaml",
        "agents/global/archon/config.yaml.example",
        "pi/AGENTS.md",
        "src/python/projectkoios/bootstrap/commands/init.py",
        "src/python/projectkoios/bootstrap/commands/install.py",
        "src/python/projectkoios/bootstrap/models.py",
    )
    for rel_path in required_paths:
        if not (root / rel_path).exists():
            findings.append(
                Finding(
                    Severity.ERROR,
                    "missing path assumed by bootstrap CLI code",
                    rel_path,
                )
            )


def _check_archon_workflows(root: Path, findings: list[Finding]) -> None:
    rel_dir = "archon/workflows"
    workflows_dir = root / rel_dir
    if not workflows_dir.exists():
        findings.append(
            Finding(
                Severity.ERROR,
                "missing repo-local Archon workflow directory",
                rel_dir,
            )
        )
        return

    if not any(workflows_dir.glob("*.yaml")):
        findings.append(
            Finding(
                Severity.ERROR,
                "missing repo-local Archon workflow YAML files",
                rel_dir,
            )
        )

    expected_workflows = (
        "archon-piv-loop.yaml",
        "archon-architect.yaml",
        "create-adr.yaml",
        "design-review.yaml",
        "plan-feature.yaml",
    )
    for workflow in expected_workflows:
        rel_path = str(PurePosixPath(rel_dir) / workflow)
        if not (root / rel_path).exists():
            findings.append(
                Finding(Severity.ERROR, "missing repo-local Archon workflow", rel_path)
            )


def _check_global_examples(root: Path, findings: list[Finding]) -> None:
    for harness in HARNESSES:
        harness_dir = root / "agents" / "global" / harness.name
        if not harness_dir.exists():
            findings.append(
                Finding(
                    Severity.ERROR,
                    f"missing global example directory for harness {harness.name!r}",
                    str(PurePosixPath("agents/global") / harness.name),
                )
            )
            continue
        if not any(item.name.endswith(".example") for item in harness_dir.iterdir()):
            findings.append(
                Finding(
                    Severity.ERROR,
                    f"missing .example config coverage for harness {harness.name!r}",
                    str(PurePosixPath("agents/global") / harness.name),
                )
            )
    _check_skills(root, findings)


def _check_skills(root: Path, findings: list[Finding]) -> None:
    for harness in HARNESSES:
        skills_dir = root / "agents" / "global" / harness.name / "skills"
        if not skills_dir.exists():
            continue
        for skill_dir in skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                findings.append(
                    Finding(
                        Severity.WARNING,
                        f"skill {skill_dir.name!r} missing SKILL.md",
                        str(skill_md.relative_to(root)),
                    )
                )


_EXCLUDED_FILES: frozenset[str] = frozenset({
    "opencode/checklists/multi-repo-execution-readiness.md",
})


def _in_scope_markdown_files(root: Path) -> tuple[str, ...]:
    files: set[str] = set(CANONICAL_FILES)
    for pattern in (
        "opencode/rules/*.md",
        "opencode/checklists/*.md",
    ):
        for path in root.glob(pattern):
            rel = path.relative_to(root).as_posix()
            if path.is_file() and rel not in _EXCLUDED_FILES:
                files.add(rel)
    return tuple(sorted(files))


def _extract_repo_refs(text: str) -> set[str]:
    refs: set[str] = set()
    for match in LOCAL_LINK_PATTERN.finditer(text):
        refs.add(_strip_fragment(match.group(1).strip()))
    for match in INLINE_CODE_PATTERN.finditer(text):
        token = match.group(1).strip()
        if _looks_like_path(token):
            refs.add(_strip_fragment(token))
        for path_match in PATH_TOKEN_PATTERN.finditer(token):
            refs.add(_strip_fragment(path_match.group(0)))
    return {ref for ref in refs if _should_validate_reference(ref)}


def _looks_like_path(token: str) -> bool:
    return (
        "/" in token
        and not any(part.isspace() for part in token.split("/"))
        and not token.startswith(("http://", "https://", "~", "$"))
    )


def _should_validate_reference(ref: str) -> bool:
    if not ref:
        return False
    if ref.startswith(("http://", "https://", "mailto:", "#", "~", "$", "<")):
        return False
    if " " in ref or "|" in ref or "\n" in ref:
        return False
    if "<" in ref or ">" in ref:
        return False
    if "*" in ref:
        return False
    if ref.endswith("/"):
        return False
    if ref.startswith("graphify-out/"):
        return False
    return "/" in ref or ref.endswith(".md")


def _strip_fragment(ref: str) -> str:
    return ref.split("#", 1)[0].strip()


def _resolve_reference(
    root: Path, source_rel_path: str, ref: str
) -> tuple[str, Path] | None:
    ref_path = PurePosixPath(ref)
    if ref.startswith("/"):
        return None
    source_dir = (root / source_rel_path).parent

    def _try_resolve(base: Path) -> Path | None:
        try:
            target = (base / ref_path).resolve()
            target.relative_to(root)
            return target
        except (ValueError, OSError):
            return None

    target = _try_resolve(source_dir)
    if target is not None and target.exists():
        return ref, target

    target = _try_resolve(root)
    if target is not None and target.exists():
        return ref, target

    return ref, root / ref_path
