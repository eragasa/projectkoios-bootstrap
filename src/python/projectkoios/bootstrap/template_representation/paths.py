from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from projectkoios.bootstrap.template_representation.models import NamespaceClassification, TemplateNamespace


REPO_ROOT = Path(__file__).resolve().parents[5]
TEMPLATES_DIR = REPO_ROOT / "docs" / "templates"
IMPLEMENTATION_DIR = REPO_ROOT / "docs" / "implementation"
PLANS_DIR = REPO_ROOT / "docs" / "plans"


@dataclass(frozen=True, slots=True)
class TemplateRepresentationPaths:
    """Filesystem paths for bootstrap template representation.

    Args:
        repo_root: Repository root path.
        templates_dir: Canonical template namespace directory.
        implementation_dir: Canonical implementation document namespace directory.
        plans_dir: Canonical plan/brief document namespace directory.
    """

    repo_root: Path = REPO_ROOT
    templates_dir: Path = TEMPLATES_DIR
    implementation_dir: Path = IMPLEMENTATION_DIR
    plans_dir: Path = PLANS_DIR

    def relative_path(self, path: Path) -> str:
        """Return a repository-relative path string.

        Args:
            path: Path to relativize.

        Returns:
            Repository-relative POSIX path.

        Raises:
            ValueError: If path is outside the repository root.
        """

        # Resolved path prevents prefix tricks when enforcing namespace boundaries.
        resolved_path: Path = path.resolve()
        try:
            return resolved_path.relative_to(self.repo_root.resolve()).as_posix()
        except ValueError:
            raise ValueError(f"path is outside repository root: {path}") from None

    def classify(self, path: Path) -> NamespaceClassification:
        """Classify a repository document path.

        Args:
            path: Path to classify.

        Returns:
            Namespace classification for templates, implementation, plans, or other.
        """

        # Relative path is retained for provenance and diagnostics.
        relative: str = self.relative_path(path)
        # Resolved path is compared against canonical namespace directories.
        resolved_path: Path = path.resolve()
        if self.is_relative_to(resolved_path, self.templates_dir):
            return NamespaceClassification(namespace=TemplateNamespace.TEMPLATE, path=relative)
        if self.is_relative_to(resolved_path, self.implementation_dir):
            return NamespaceClassification(namespace=TemplateNamespace.IMPLEMENTATION, path=relative)
        if self.is_relative_to(resolved_path, self.plans_dir):
            return NamespaceClassification(namespace=TemplateNamespace.PLAN, path=relative)
        return NamespaceClassification(namespace=TemplateNamespace.OTHER, path=relative)

    def ensure_template_path(self, path: Path, *, allow_test_fixture: bool = False) -> str:
        """Return repository-relative template path when parsing is allowed.

        Args:
            path: Markdown source path.
            allow_test_fixture: Whether non-template paths are allowed for tests.

        Returns:
            Repository-relative source path.

        Raises:
            ValueError: If path is outside the template namespace and not allowed.
        """

        # Namespace classification enforces the first-slice template-only boundary.
        classification: NamespaceClassification = self.classify(path)
        if classification.namespace is TemplateNamespace.TEMPLATE or allow_test_fixture:
            return classification.path
        raise ValueError(f"template representation only supports docs/templates paths: {classification.path}")

    def template_id(self, source_path: str) -> str:
        """Return a stable template identifier from a source path.

        Args:
            source_path: Repository-relative template path.

        Returns:
            Stable template identifier.
        """

        return Path(source_path).name.removesuffix(".md")

    def is_relative_to(self, path: Path, directory: Path) -> bool:
        """Return whether path is under directory.

        Args:
            path: Candidate path.
            directory: Possible parent directory.

        Returns:
            True when path is under directory.
        """

        return path.is_relative_to(directory.resolve())
