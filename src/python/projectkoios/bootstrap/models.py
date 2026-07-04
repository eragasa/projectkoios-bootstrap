from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Runtime:
    """Harness runtime configuration target.

    Args:
        name: Runtime name used in shared config paths.
        config_dir: Local machine configuration directory for the runtime.
    """

    name: str
    config_dir: Path

    @property
    def skills_dir(self) -> Path:
        """Return the shared example skills directory for this runtime."""
        return GLOBAL_DIR / self.name / "skills"

    @property
    def runtime_skills_dir(self) -> Path:
        """Return the local runtime skills installation directory."""
        if self.name == "pi":
            return Path.home() / ".pi" / "agent" / "skills"
        if self.name == "opencode":
            return Path.home() / ".opencode" / "skills"
        return self.config_dir / "skills"


RUNTIMES: list[Runtime] = [
    Runtime("pi", Path.home() / ".pi"),
    Runtime("archon", Path.home() / ".archon"),
    Runtime("opencode", Path.home() / ".opencode"),
    Runtime("goose", Path.home() / ".local/share/goose"),
]


@dataclass(frozen=True)
class Role:
    """Project Koios role identity metadata.

    Args:
        name: Durable role name.
        short_name: Short display name for the role.
        responsibilities: Summary of role-owned work.
    """

    name: str
    short_name: str
    responsibilities: str


ROLE_TO_RUNTIME: dict[str, str] = {
    "Hermes": "pi",
    "Athena": "archon",
    "Vulcan": "opencode",
    "Koios": "goose",
}


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
GLOBAL_DIR = REPO_ROOT / "agents" / "global"
