from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import os
from pathlib import Path, PurePosixPath
import re

from projectkoios.bootstrap.models import RUNTIMES, Runtime


class Severity(Enum):
    """Classify a validation finding by operational severity."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass(frozen=True)
class Finding:
    """Record one repository validation finding.

    Args:
        severity: Operational severity for the finding.
        message: Human-readable validation message.
        path: Optional repository-relative path associated with the finding.
    """

    severity: Severity
    message: str
    path: str | None = None


@dataclass(frozen=True)
class ValidationResult:
    """Collect repository validation findings and expose status helpers.

    Args:
        findings: Ordered validation findings emitted by the harness checks.
    """

    findings: tuple[Finding, ...]

    def count(self, severity: Severity) -> int:
        """Return the number of findings with a matching severity.

        Args:
            severity: Severity value to count.

        Returns:
            Number of findings whose severity is identical to the requested value.
        """

        return sum(1 for finding in self.findings if finding.severity is severity)

    def exit_code(self, *, strict: bool = False) -> int:
        """Return a process exit code for the validation result.

        Args:
            strict: Treat warnings as failures when true.

        Returns:
            Zero when validation passed under the selected strictness, otherwise one.
        """

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
        "## ADR file convention",
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
    "goose/AGENTS.md": (
        "## Role identity",
        "## Maps",
        "## Vault rules",
        "## Handoff support",
    ),
    "docs/meta-harness.md": (
        "## Purpose",
        "## Skill model",
        "## Anti-patterns",
    ),
    "archon/prompts/harness-routing.md": (
        "## Harness definitions",
        "## Rules",
        "## Output requirement",
    ),
}

REFERENCE_ROOTS: tuple[str, ...] = (
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

LOCAL_LINK_PATTERN: re.Pattern[str] = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
INLINE_CODE_PATTERN: re.Pattern[str] = re.compile(r"`([^`\n]+)`")
PATH_ROOT_PATTERN: str = "|".join(re.escape(reference_root) for reference_root in REFERENCE_ROOTS)
PATH_TOKEN_PATTERN: re.Pattern[str] = re.compile(
    r"(?:\.\./|\./)?(?:" + PATH_ROOT_PATTERN + r")/[A-Za-z0-9._<>{}/~*-]+"
)
EXCLUDED_FILES: frozenset[str] = frozenset({
    "opencode/checklists/multi-repo-execution-readiness.md",
})


def validate_harnesses(root: Path, *, strict: bool = False) -> ValidationResult:
    """Validate repo-local harness files and references.

    Args:
        root: Repository root to validate.
        strict: Reserved strictness flag accepted by callers for interface stability.

    Returns:
        Validation result containing errors, warnings, and informational findings.
    """

    # Normalize the caller-provided root so all checks share one filesystem base.
    resolved_root: Path = root.resolve()
    # Accumulate findings in stable check order before freezing the result object.
    findings: list[Finding] = []

    check_canonical_files(resolved_root, findings)
    check_references(resolved_root, findings)
    check_opencode_references(resolved_root, findings)
    check_bootstrap_assumptions(resolved_root, findings)
    check_archon_workflows(resolved_root, findings)
    check_global_examples(resolved_root, findings)

    findings.append(
        Finding(
            Severity.INFO,
            f"validated {len(CANONICAL_FILES)} canonical harness document(s)",
        )
    )
    return ValidationResult(tuple(findings))


def check_canonical_files(root: Path, findings: list[Finding]) -> None:
    """Append findings for missing canonical files or headings.

    Args:
        root: Repository root containing canonical harness files.
        findings: Mutable finding accumulator updated in place.
    """

    rel_path: str
    required_headings: tuple[str, ...]
    for rel_path, required_headings in CANONICAL_FILES.items():
        # Resolve each canonical document from the fixed repository root.
        path: Path = root / rel_path
        if not path.exists():
            findings.append(
                Finding(Severity.ERROR, "missing canonical harness file", rel_path)
            )
            continue

        # Read the document once so all required heading checks share identical input.
        text: str = path.read_text(encoding="utf-8")
        heading: str
        for heading in required_headings:
            if heading not in text:
                findings.append(
                    Finding(
                        Severity.ERROR,
                        f"missing required heading {heading!r}",
                        rel_path,
                    )
                )


def check_references(root: Path, findings: list[Finding]) -> None:
    """Append findings for broken repository-local Markdown references.

    Args:
        root: Repository root used to resolve references.
        findings: Mutable finding accumulator updated in place.
    """

    rel_path: str
    for rel_path in in_scope_markdown_files(root):
        # Convert the repository-relative Markdown path into an absolute document path.
        path: Path = root / rel_path
        if not path.exists():
            continue
        # Extract references from the current document content only once.
        text: str = path.read_text(encoding="utf-8")
        raw_ref: str
        for raw_ref in sorted(extract_repo_refs(text)):
            # Resolve references relative to the source file first, then repository root.
            resolved: tuple[str, Path] | None = resolve_reference(root, rel_path, raw_ref)
            if resolved is None:
                continue
            # Display keeps the original reference text for review-friendly errors.
            display: str = resolved[0]
            # Target is the filesystem location that must exist for the reference to pass.
            target: Path = resolved[1]
            if not target.exists():
                findings.append(
                    Finding(
                        Severity.ERROR,
                        f"broken repo-local reference {display!r}",
                        rel_path,
                    )
                )


def check_opencode_references(root: Path, findings: list[Finding]) -> None:
    """Append findings for missing opencode rule and checklist references.

    Args:
        root: Repository root containing the opencode workspace files.
        findings: Mutable finding accumulator updated in place.
    """

    # Keep this check scoped to the opencode harness instruction file.
    rel_path: str = "opencode/AGENTS.md"
    # Resolve the opencode instruction file from the repository root.
    path: Path = root / rel_path
    if not path.exists():
        return

    # Read the instruction file once for both rule and checklist reference scans.
    text: str = path.read_text(encoding="utf-8")
    rule_ref: str
    for rule_ref in sorted(set(re.findall(r"`(rules/[^`]+\.md)`", text))):
        if not (root / "opencode" / rule_ref).exists():
            findings.append(
                Finding(Severity.ERROR, f"missing opencode rule reference {rule_ref!r}", rel_path)
            )
    checklist_ref: str
    for checklist_ref in sorted(set(re.findall(r"`(checklists/[^`]+\.md)`", text))):
        if not (root / "opencode" / checklist_ref).exists():
            findings.append(
                Finding(
                    Severity.ERROR,
                    f"missing opencode checklist reference {checklist_ref!r}",
                    rel_path,
                )
            )


def check_bootstrap_assumptions(root: Path, findings: list[Finding]) -> None:
    """Append findings for paths assumed by bootstrap CLI behavior.

    Args:
        root: Repository root containing bootstrap source and config examples.
        findings: Mutable finding accumulator updated in place.
    """

    # Required paths mirror assumptions made by bootstrap commands and installation docs.
    required_paths: tuple[str, ...] = (
        "agents/global",
        "archon/workflows",
        "archon/skills/.archon/config.yaml",
        "agents/global/archon/config.yaml.example",
        "pi/AGENTS.md",
        "src/python/projectkoios/bootstrap/commands/init.py",
        "src/python/projectkoios/bootstrap/commands/install.py",
        "src/python/projectkoios/bootstrap/models.py",
    )
    rel_path: str
    for rel_path in required_paths:
        if not (root / rel_path).exists():
            findings.append(
                Finding(
                    Severity.ERROR,
                    "missing path assumed by bootstrap CLI code",
                    rel_path,
                )
            )


def check_archon_workflows(root: Path, findings: list[Finding]) -> None:
    """Append findings for missing repo-local Archon workflow files.

    Args:
        root: Repository root containing the Archon workflow directory.
        findings: Mutable finding accumulator updated in place.
    """

    # Workflow directory path is reported relative to the repository root.
    rel_dir: str = "archon/workflows"
    # Workflows directory is inspected for both presence and expected YAML members.
    workflows_dir: Path = root / rel_dir
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

    # Expected workflows are the stable bootstrap workflow files referenced by docs.
    expected_workflows: tuple[str, ...] = (
        "archon-piv-loop.yaml",
        "archon-architect.yaml",
        "create-adr.yaml",
        "design-review.yaml",
        "plan-feature.yaml",
    )
    workflow: str
    for workflow in expected_workflows:
        # Report missing workflow paths in repository-relative POSIX form.
        rel_path: str = str(PurePosixPath(rel_dir) / workflow)
        if not (root / rel_path).exists():
            findings.append(
                Finding(Severity.ERROR, "missing repo-local Archon workflow", rel_path)
            )


def check_global_examples(root: Path, findings: list[Finding]) -> None:
    """Append findings for missing runtime global example configs.

    Args:
        root: Repository root containing shared global harness examples.
        findings: Mutable finding accumulator updated in place.
    """

    runtime: Runtime
    for runtime in RUNTIMES:
        # Runtime example directory must exist for each configured harness runtime.
        runtime_dir: Path = root / "agents" / "global" / runtime.name
        if not runtime_dir.exists():
            findings.append(
                Finding(
                    Severity.ERROR,
                    f"missing global example directory for runtime {runtime.name!r}",
                    str(PurePosixPath("agents/global") / runtime.name),
                )
            )
            continue
        if not any(item.name.endswith(".example") for item in runtime_dir.iterdir()):
            findings.append(
                Finding(
                    Severity.ERROR,
                    f"missing .example config coverage for runtime {runtime.name!r}",
                    str(PurePosixPath("agents/global") / runtime.name),
                )
            )
    check_skills(root, findings)


def check_skills(root: Path, findings: list[Finding]) -> None:
    """Append findings for malformed shared skill example directories.

    Args:
        root: Repository root containing shared global harness examples.
        findings: Mutable finding accumulator updated in place.
    """

    runtime: Runtime
    for runtime in RUNTIMES:
        # Runtime skills directory is optional, but present skill directories need SKILL.md.
        skills_dir: Path = root / "agents" / "global" / runtime.name / "skills"
        if not skills_dir.exists():
            continue
        skill_dir: Path
        for skill_dir in skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            # Each skill directory must expose the Pi-compatible skill metadata file.
            skill_md: Path = skill_dir / "SKILL.md"
            if not skill_md.exists():
                findings.append(
                    Finding(
                        Severity.WARNING,
                        f"skill {skill_dir.name!r} missing SKILL.md",
                        str(skill_md.relative_to(root)),
                    )
                )


def in_scope_markdown_files(root: Path) -> tuple[str, ...]:
    """Return Markdown files included in harness reference validation.

    Args:
        root: Repository root used for glob expansion.

    Returns:
        Sorted repository-relative Markdown paths selected for validation.
    """

    # Start with canonical files so each required document participates in reference checks.
    files: set[str] = set(CANONICAL_FILES)
    # Additional patterns cover subordinate opencode policy surfaces.
    patterns: tuple[str, ...] = (
        "opencode/rules/*.md",
        "opencode/checklists/*.md",
    )
    pattern: str
    for pattern in patterns:
        path: Path
        for path in root.glob(pattern):
            # Store paths as POSIX strings to keep findings stable across platforms.
            rel: str = path.relative_to(root).as_posix()
            if path.is_file() and rel not in EXCLUDED_FILES:
                files.add(rel)
    return tuple(sorted(files))


def extract_repo_refs(text: str) -> set[str]:
    """Extract repository-local reference candidates from Markdown text.

    Args:
        text: Markdown text to scan.

    Returns:
        Repository-local reference strings after fragment stripping and filtering.
    """

    # Collect references from both Markdown links and inline-code path mentions.
    refs: set[str] = set()
    local_match: re.Match[str]
    for local_match in LOCAL_LINK_PATTERN.finditer(text):
        refs.add(strip_fragment(local_match.group(1).strip()))
    inline_match: re.Match[str]
    for inline_match in INLINE_CODE_PATTERN.finditer(text):
        # Token is the complete inline-code content that may be a path or contain paths.
        token: str = inline_match.group(1).strip()
        if looks_like_path(token):
            refs.add(strip_fragment(token))
        path_match: re.Match[str]
        for path_match in PATH_TOKEN_PATTERN.finditer(token):
            refs.add(strip_fragment(path_match.group(0)))
    return {ref for ref in refs if should_validate_reference(ref)}


def looks_like_path(token: str) -> bool:
    """Return whether an inline-code token resembles a local filesystem path.

    Args:
        token: Inline-code token to classify.

    Returns:
        True when the token has path separators and no obvious non-path markers.
    """

    return (
        "/" in token
        and not any(part.isspace() for part in token.split("/"))
        and not token.startswith(("http://", "https://", "~", "$"))
    )


def should_validate_reference(ref: str) -> bool:
    """Return whether a reference should be checked as repository-local.

    Args:
        ref: Candidate reference extracted from Markdown.

    Returns:
        True when the reference is local, concrete, and likely path-like.
    """

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


def strip_fragment(ref: str) -> str:
    """Return a reference without any Markdown anchor fragment.

    Args:
        ref: Reference string that may include a hash fragment.

    Returns:
        Reference content before the first hash character, with outer whitespace removed.
    """

    return ref.split("#", 1)[0].strip()


def try_resolve_reference_base(root: Path, ref_path: PurePosixPath, base: Path) -> Path | None:
    """Resolve a reference path against one base when it stays inside the repository.

    Args:
        root: Repository root that bounds valid reference targets.
        ref_path: POSIX reference path from Markdown.
        base: Base directory used for relative resolution.

    Returns:
        Resolved target path when it remains inside the repository, otherwise None.
    """

    # Normalize dot segments without requiring the target to exist yet.
    target: Path = Path(os.path.abspath(base / ref_path))
    if target.is_relative_to(root):
        return target
    return None


def resolve_reference(
    root: Path, source_rel_path: str, ref: str
) -> tuple[str, Path] | None:
    """Resolve a repository-local reference from source-relative or root-relative bases.

    Args:
        root: Repository root that bounds valid reference targets.
        source_rel_path: Repository-relative path to the source Markdown file.
        ref: Reference text extracted from Markdown.

    Returns:
        Pair of display reference and target path, or None for absolute references.
    """

    # Convert the textual Markdown reference into a POSIX path representation.
    ref_path: PurePosixPath = PurePosixPath(ref)
    if ref.startswith("/"):
        return None
    # Source directory provides the first resolution base for relative links.
    source_dir: Path = (root / source_rel_path).parent

    # Source-relative target wins when it already exists.
    source_target: Path | None = try_resolve_reference_base(root, ref_path, source_dir)
    if source_target is not None and source_target.exists():
        return ref, source_target

    # Repository-root target is the fallback for root-relative references in docs.
    root_target: Path | None = try_resolve_reference_base(root, ref_path, root)
    if root_target is not None and root_target.exists():
        return ref, root_target

    return ref, root / ref_path
